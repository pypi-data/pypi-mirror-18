#!/usr/bin/python
# Original Author: Mirantis, Inc
# Substantial additions by SSCC(R&D Center,YouMingyang)
# Description: Base class for openstack service status collect plugin
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import sys
import datetime
import dateutil.parser
import dateutil.tz
import ConfigParser

from functools import wraps
import requests
import simplejson as json

# By default, query OpenStack API endpoints every 50 seconds. We choose a value
# less than the default group by interval (which is 60 seconds) to avoid gaps
# in the Grafana graphs.
INTERVAL = 50


class OSClient(object):
    """ Base class for querying the OpenStack API endpoints.

    It uses the Keystone service catalog to discover the API endpoints.
    """
    EXPIRATION_TOKEN_DELTA = datetime.timedelta(0, 30)

    def __init__(self, username, password, tenant, keystone_url, timeout,
                 max_retries):
        self.username = username
        self.password = password
        self.tenant_name = tenant
        self.keystone_url = keystone_url
        self.service_catalog = []
        self.tenant_id = None
        self.timeout = timeout
        self.token = None
        self.valid_until = None

        # Note: prior to urllib3 v1.9, retries are made on failed connections
        # but not on timeout and backoff time is not supported.
        # (at this time we ship requests 2.2.1 and urllib3 1.6.1 or 1.7.1)
        self.session = requests.Session()
        self.session.mount('http://', requests.adapters.HTTPAdapter(max_retries=max_retries))
        self.session.mount('https://', requests.adapters.HTTPAdapter(max_retries=max_retries))

        self.get_token()

    def is_valid_token(self):
        now = datetime.datetime.now(tz=dateutil.tz.tzutc())
        return self.token and self.valid_until and self.valid_until > now

    def clear_token(self):
        self.token = None
        self.valid_until = None

    def get_token(self):
        self.clear_token()
        data = json.dumps({
            "auth":
            {
                'tenantName': self.tenant_name,
                'passwordCredentials':
                {
                    'username': self.username,
                    'password': self.password
                    }
                }
            }
        )
        sys.stderr.write("Trying to get token from '%s'" % self.keystone_url)
        r = self.make_request('post',
                              '%s/tokens' % self.keystone_url, data=data,
                              token_required=False)
        if not r:
            sys.stderr.write("Cannot get a valid token from %s" %
                              self.keystone_url)
            return

        if r.status_code < 200 or r.status_code > 299:
            sys.stderr.write("%s responded with code %d" %
                              (self.keystone_url, r.status_code))
            return

        data = r.json()
       	sys.stderr.write("Got response from Keystone: '%s'" % data)
        self.token = data['access']['token']['id']
        self.tenant_id = data['access']['token']['tenant']['id']
        self.valid_until = dateutil.parser.parse(
            data['access']['token']['expires']) - self.EXPIRATION_TOKEN_DELTA
        self.service_catalog = []
        for item in data['access']['serviceCatalog']:
            endpoint = item['endpoints'][0]
            self.service_catalog.append({
                'name': item['name'],
                'region': endpoint['region'],
                'service_type': item['type'],
                'url': endpoint['internalURL'],
                'admin_url': endpoint['adminURL'],
            })

        sys.stderr.write("Got token '%s'" % self.token)
        return self.token

    def make_request(self, verb, url, data=None, token_required=True):
        kwargs = {
            'url': url,
            'timeout': self.timeout,
            'headers': {'Content-type': 'application/json'}
        }
        if token_required and not self.is_valid_token() and \
           not self.get_token():
            sys.stderr.write("Aborting request, no valid token")
            return
        elif token_required:
            kwargs['headers']['X-Auth-Token'] = self.token

        if data is not None:
            kwargs['data'] = data

        func = getattr(self.session, verb.lower())

        try:
            r = func(**kwargs)
        except Exception as e:
            sys.stderr.write("Got exception for '%s': '%s'" %
                              (kwargs['url'], e))
            return

        sys.stderr.write("%s responded with status code %d" %
                         (kwargs['url'], r.status_code))
        if r.status_code == 401:
            # Clear token in case it is revoked or invalid
            self.clear_token()

        return r


class CollectdPlugin(object):

    def __init__(self):
	conf = ConfigParser.ConfigParser()
        conf.read('/usr/local/etc/zabbix_agentd.d/scripts/openstack.conf')
	self.os_client = OSClient(
	    conf.get('openstack', 'Username'),
	    conf.get('openstack', 'Password'),
	    conf.get('openstack', 'Tenant'),
	    conf.get('openstack', 'KeystoneUrl'),
	    int(conf.get('openstack', 'Timeout')),
	    3
	)
	self.depends_on_resource = conf.get('openstack', 'DependsOnResource')
	self.extra_config = {}

    def _build_url(self, service, resource):
        s = (self.get_service(service) or {})
        # the adminURL must be used to access resources with Keystone API v2
        if service == 'keystone' and \
                (resource in ['tenants', 'users'] or 'OS-KS' in resource):
            url = s.get('admin_url')
        else:
            url = s.get('url')

        if url:
            if url[-1] != '/':
                url += '/'
            url = "%s%s" % (url, resource)
        else:
            sys.stderr.write("Service '%s' not found in catalog" % service)
        return url

    def raw_get(self, url, token_required=False):
        return self.os_client.make_request('get', url,
                                           token_required=token_required)

    def get(self, service, resource):
        url = self._build_url(service, resource)
        if not url:
            return
        sys.stderr.write("GET '%s'" % url)
        return self.os_client.make_request('get', url)

    @property
    def service_catalog(self):
        if not self.os_client.service_catalog:
            # In case the service catalog is empty (eg Keystone was down when
            # collectd started), we should try to get a new token
            self.os_client.get_token()
        return self.os_client.service_catalog

    def get_service(self, service_name):
        return next((x for x in self.service_catalog
                    if x['name'] == service_name), None)

    def notification_callback(self, notification):
        if not self.depends_on_resource:
            return

        try:
            data = json.loads(notification.message)
        except ValueError:
            return

        if 'value' not in data:
            sys.stderr.write(
                "%s: missing 'value' in notification" %
                self.__class__.__name__)
        elif 'resource' not in data:
            sys.stderr.write(
                "%s: missing 'resource' in notification" %
                self.__class__.__name__)
        elif data['resource'] == self.depends_on_resource:
            do_collect_data = data['value'] > 0
            if self.do_collect_data != do_collect_data:
                # log only the transitions
                sys.stderr.write("%s: do_collect_data=%s" %
                                   (self.__class__.__name__, do_collect_data))
            self.do_collect_data = do_collect_data

    def get_objects(self, project, object_name, api_version='',
                    params='all_tenants=1'):
        """ Return a list of OpenStack objects

            See get_objects_details()
        """
        return self._get_objects(project, object_name, api_version, params,
                                 False)

    def get_objects_details(self, project, object_name, api_version='',
                            params='all_tenants=1'):
        """ Return a list of details about OpenStack objects

            The API version is not always included in the URL endpoint
            registered in Keystone (eg Glance). In this case, use the
            api_version parameter to specify which version should be used.
        """
        return self._get_objects(project, object_name, api_version, params,
                                 True)

    def _get_objects(self, project, object_name, api_version, params, detail):
        if api_version:
            resource = '%s/%s' % (api_version, object_name)
        else:
            resource = '%s' % (object_name)
        if detail:
            resource = '%s/detail' % (resource)
        if params:
            resource = '%s?%s' % (resource, params)
        # TODO(scroiset): use pagination to handle large collection
        r = self.get(project, resource)
        if not r or object_name not in r.json():
            sys.stderr.write('Could not find %s %s' % (project,
                                                          object_name))
            return []
        return r.json().get(object_name)

    def count_objects_group_by(self,
                               list_object,
                               group_by_func,
                               count_func=None):

        """ Dispatch values of object number grouped by criteria."""

        status = {}
        for obj in list_object:
            s = group_by_func(obj)
            if s in status:
                status[s] += count_func(obj) if count_func else 1
            else:
                status[s] = count_func(obj) if count_func else 1
        return status
