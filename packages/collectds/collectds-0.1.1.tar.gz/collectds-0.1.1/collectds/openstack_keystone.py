#!/usr/bin/python
# Original Author: Mirantis, Inc
# Substantial additions by SSCC(R&D Center,YouMingyang)
# Description: plugin for getting statistics from Keystone
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
import re
#import pydevd

import openstack

PLUGIN_NAME = 'keystone'


class KeystoneStatsPlugin(openstack.CollectdPlugin):
    """ Class to report the statistics on Keystone service.

        number of tenants, users broken down by state
        number of roles
    """
	
    def itermetrics(self, host):
        def groupby(d):
            return 'enabled' if d.get('enabled') else 'disabled'

        # tenants
        r = self.get('keystone', 'tenants')
        if not r:
            sys.stderr.write('Could not find Keystone tenants')
            return
        tenants_details = r.json().get('tenants', [])
        status = self.count_objects_group_by(tenants_details,
                                             group_by_func=groupby)
        def print_metric(name, value):
	    if name == 'roles':
		print('%s keystone[openstack_keystone_roles] %d' % 
		    (host, value))
	    else:
		resource, state = re.findall('^([^.]+)\.(.+)$', name)[0]
		metric_name = 'openstack_keystone_' + resource.replace('.', '_')
		print('%s keystone[%s|state=%s] %d' %
		    (host, metric_name, state, value))
	for s, nb in status.iteritems():
	    print_metric('tenants.' + s, nb)

        # users
        r = self.get('keystone', 'users')
        if not r:
            sys.stderr.write('Could not find Keystone users')
            return
        users_details = r.json().get('users', [])
        status = self.count_objects_group_by(users_details,
                                             group_by_func=groupby)
        for s, nb in status.iteritems():
	    print_metric('users.' + s, nb)

        # roles
        r = self.get('keystone', 'OS-KSADM/roles')
        if not r:
            sys.stderr.write('Could not find Keystone roles')
            return
        roles = r.json().get('roles', [])
	print_metric('roles', len(roles))

if __name__ == "__main__":
#    pydevd.settrace('192.168.22.148', port=9901, stdoutToServer=True, stderrToServer=True)
    if len(sys.argv) > 1:
        host = sys.argv[1]
        plugin = KeystoneStatsPlugin()
        plugin.itermetrics(host)
    else:
        print('Usage:./%s host' % sys.argv[0])
