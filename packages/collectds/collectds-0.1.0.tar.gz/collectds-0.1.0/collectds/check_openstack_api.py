#!/usr/bin/python
# Original Author: Mirantis, Inc
# Substantial additions by SSCC(R&D Center,YouMingyang)
# Description:Collectd plugin for checking the status of OpenStack API 
# services
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
#
import sys
from urlparse import urlparse
#pydevd

import openstack

PLUGIN_NAME = 'check_openstack_api'

class APICheckPlugin(openstack.CollectdPlugin):
    """ Class to check the status of OpenStack API services.
    """
    FAIL = 0
    OK = 1
    UNKNOWN = 2

    # TODO: sahara, murano
    CHECK_MAP = {
        'keystone': {
            'path': '/', 'expect': 300, 'name': 'keystone-public-api'},
        'heat': {'path': '/', 'expect': 300, 'name': 'heat-api'},
        'heat-cfn': {'path': '/', 'expect': 300, 'name': 'heat-cfn-api'},
        'glance': {'path': '/', 'expect': 300, 'name': 'glance-api'},
        'cinder': {'path': '/', 'expect': 200, 'name': 'cinder-api'},
        'cinderv2': {'path': '/', 'expect': 200, 'name': 'cinder-v2-api'},
        'neutron': {'path': '/', 'expect': 200, 'name': 'neutron-api'},
        'nova': {'path': '/', 'expect': 200, 'name': 'nova-api'},
        # Ceilometer requires authentication for all paths
        'ceilometer': {
            'path': 'v2/capabilities', 'expect': 200, 'auth': True,
            'name': 'ceilometer-api'},
        'swift': {'path': 'healthcheck', 'expect': 200, 'name': 'swift-api'},
        'swift_s3': {
            'path': 'healthcheck', 'expect': 200, 'name': 'swift-s3-api'},
    }

    def _service_url(self, endpoint, path):
        url = urlparse(endpoint)
        u = '%s://%s' % (url.scheme, url.netloc)
        if path != '/':
            u = '%s/%s' % (u, path)
        return u

    def check_api(self):
        """ Check the status of all the API services.

            Yields a list of dict items with 'service', 'status' (either OK,
            FAIL or UNKNOWN) and 'region' keys.
        """
        catalog = self.service_catalog
        for service in catalog:
            name = service['name']
            if name not in self.CHECK_MAP:
                sys.stderr.write("No check found for service '%s', skipping it" % name)
                status = self.UNKNOWN
            else:
                check = self.CHECK_MAP[name]
                url = self._service_url(service['url'], check['path'])
                r = self.raw_get(url, token_required=check.get('auth', False))

                if r is None or r.status_code != check['expect']:
                    def _status(ret):
                        return 'N/A' if r is None else r.status_code

                    sys.stderr.write(
                        "Service %s check failed "
                        "(returned '%s' but expected '%s')" % (
                            name, _status(r), check['expect'])
                    )
                    status = self.FAIL
                else:
                    status = self.OK

            yield {
                'service': check.get('name', name),
                'status': status,
                'region': service['region']
            }

    def itermetrics(self, host):
        for item in self.check_api():
            if item['status'] == self.UNKNOWN:
                # skip if status is UNKNOWN
                continue
		
	    print('%s endpoint[openstack_check_api|service=%s] %d' % 
               (host, item['service'], item['status']))


if __name__ == "__main__":
#    pydevd.settrace('192.168.22.148', port=9901, stdoutToServer=True, stderrToServer=True)
    if len(sys.argv) > 1:
        host = sys.argv[1]
        plugin = APICheckPlugin()
        plugin.itermetrics(host)
    else:
        print('Usage:./%s host' % sys.argv[0])
