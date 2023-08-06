#!/usr/bin/python
# Original Author: Mirantis, Inc
# Substantial additions by SSCC(R&D Center,YouMingyang)
# Description: plugin for getting statistics from Nova
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
import dbi

PLUGIN_NAME = 'nova'


class NovaStatsPlugin(openstack.CollectdPlugin):
    """ Class to report the statistics on Nova service.

        number of instances broken down by state
    """

    def itermetrics(self, host):
        servers_details = self.get_objects_details('nova', 'servers')

        def groupby(d):
            return d.get('status', 'unknown').lower()
        status = self.count_objects_group_by(servers_details,
                                             group_by_func=groupby)
        for s, nb in status.iteritems():
            print('%s nova[openstack_nova_instances|state=%s] %d' % 
		(host, s, nb))


class NovaServiceStats(dbi.ServiceStatus):
    def read_sql(self, conf, service_name):
	return [
	    conf.get('nova', 'services_down'),
	    conf.get('nova', 'services_up'),
	    conf.get('nova', 'services_disable')
	]
    
    def print_metric(self, host, status):
	for stats in status:
	    service, state = re.findall(r'^services\.(.+)\.([^.]+)$', 
		stats[0])[0]   
	    print('%s nova[openstack_nova_services|service=%s|state=%s] %d' %
	        (host, service, state, stats[1]))

if __name__ == "__main__":
#    pydevd.settrace('192.168.22.148', port=9901, stdoutToServer=True, 
#	stderrToServer=True)
    if len(sys.argv) > 1:
        host = sys.argv[1]
	service = NovaServiceStats(PLUGIN_NAME)
	service.itermetrics(host)
	plugin = NovaStatsPlugin()
        plugin.itermetrics(host)
    else:
        print('Usage:./%s host' % sys.argv[0])
