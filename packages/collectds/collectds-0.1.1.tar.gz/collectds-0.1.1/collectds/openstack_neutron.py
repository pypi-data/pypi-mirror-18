#!/usr/bin/python
# Original Author: Mirantis, Inc
# Substantial additions by SSCC(R&D Center,YouMingyang)
# Description: plugin for getting resource statistics from Neutron
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

PLUGIN_NAME = 'neutron'


class NeutronStatsPlugin(openstack.CollectdPlugin):
    """ Class to report the statistics on Neutron service.

        number of networks broken down by status
        number of subnets
        number of ports broken down by owner and status
        number of routers broken down by status
        number of floating IP addresses broken down by free/associated
    """

    def itermetrics(self, host):
        def groupby_network(x):
            return "networks.%s" % x.get('status', 'unknown').lower()

        def groupby_router(x):
            return "routers.%s" % x.get('status', 'unknown').lower()

        def groupby_port(x):
            owner = x.get('device_owner', 'unknown')
            if owner.startswith('network:'):
                owner = owner.replace('network:', '')
            elif owner.startswith('compute:'):
                # The part after 'compute:' is the name of the Nova AZ
                owner = 'compute'
            status = x.get('status', 'unknown').lower()
            return "ports.%s.%s" % (owner, status)

        def groupby_floating(x):
            if x.get('port_id', None):
                status = 'associated'
            else:
                status = 'free'
            return "floatingips.%s" % status
	
	def print_metric(name, value):
	     if name in ['networks', 'ports', 'routers', 'floatingips']:
		pass
	     elif name == 'subnets':
		print('%s neutron[openstack_neutron_subnets] %d' %
		    (host, value))
	     elif re.match('^ports', name):
		resource, owner, state = re.findall('^([^.]+)\.([^.]+)\.(.+)$', 
		    name)[0]
		metric_name = 'openstack_neutron_' + resource.replace('.', '_')
		print('%s neutron[%s|owner=%s|state=%s] %d' %
		    (host, metric_name, owner, state, value))
	     else:
		resource, state = re.findall('^([^.]+)\.(.+)$', name)[0]
		metric_name = 'openstack_neutron_' + resource.replace('.', '_')
		print('%s neutron[%s|state=%s] %d' % 
		    (host, metric_name, state, value))
	
        # Networks
        networks = self.get_objects('neutron', 'networks', api_version='v2.0')
        status = self.count_objects_group_by(networks,
                                             group_by_func=groupby_network)
        for s, nb in status.iteritems():
            print_metric(s, nb)
        print_metric('networks', len(networks))

        # Subnets
        subnets = self.get_objects('neutron', 'subnets', api_version='v2.0')
        print_metric('subnets', len(subnets))

        # Ports
        ports = self.get_objects('neutron', 'ports', api_version='v2.0')
        status = self.count_objects_group_by(ports,
                                             group_by_func=groupby_port)
        for s, nb in status.iteritems():
            print_metric(s, nb)
        print_metric('ports', len(ports))

        # Routers
        routers = self.get_objects('neutron', 'routers', api_version='v2.0')
        status = self.count_objects_group_by(routers,
                                             group_by_func=groupby_router)
        for s, nb in status.iteritems():
            print_metric(s, nb)
        print_metric('routers', len(routers))

        # Floating IP addresses
        floatingips = self.get_objects('neutron', 'floatingips',
                                       api_version='v2.0')
        status = self.count_objects_group_by(floatingips,
                                             group_by_func=groupby_floating)
        for s, nb in status.iteritems():
            print_metric(s, nb)
        print_metric('floatingips', len(floatingips))
	
class NeutronServiceStats(dbi.ServiceStatus):
    def read_sql(self, conf, service_name):
	return [conf.get('neutron', 'agents_down'),
		conf.get('neutron', 'agents_up'),
		conf.get('neutron', 'agents_disable')]

    def print_metric(self, host, status):
	for stats in status:
	    service, state = re.findall(r'^agents\.(.+)\.([^.]+)$',stats[0])[0]
	    print('%s neutron[openstack_neutron_agents|service=%s|state=%s] %d' %
		(host, service, state, stats[1]))	

if __name__ == "__main__":
#    pydevd.settrace('192.168.22.148', port=9901, stdoutToServer=True, stderrToServer=True)
    if len(sys.argv) > 1:
        host = sys.argv[1]
	service = NeutronServiceStats(PLUGIN_NAME)
	service.itermetrics(host)
        plugin = NeutronStatsPlugin()
        plugin.itermetrics(host)
    else:
        print('Usage:./%s host' % sys.argv[0])  
