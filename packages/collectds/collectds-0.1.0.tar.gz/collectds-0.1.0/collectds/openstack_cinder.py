#!/usr/bin/env python
# Original Author: Mirantis, Inc
# Substantial additions by SSCC(R&D Center,YouMingyang)
# Description: plugin for getting statistics from Cinder
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

PLUGIN_NAME = 'cinder'


class CinderStatsPlugin(openstack.CollectdPlugin):
    """ Class to report the statistics on Cinder service.

        number of volumes broken down by state
        total size of volumes usable and in error state
    """

    def itermetrics(self, host):
        volumes_details = self.get_objects_details('cinder', 'volumes')

        def groupby(d):
            return d.get('status', 'unknown').lower()

        def count_size_bytes(d):
            return d.get('size', 0) * 10**9

        status = self.count_objects_group_by(volumes_details,
                                             group_by_func=groupby)
	
	def print_metric(plugin_instance, name, value):
	    metric_name = 'openstack_cinder_' + plugin_instance.replace('.', '_')
	    print('%s cinder[%s|state=%s] %d' % (host, metric_name, name, value))

        for s, nb in status.iteritems():
	    print_metric('volumes', s, nb)

        sizes = self.count_objects_group_by(volumes_details,
                                            group_by_func=groupby,
                                            count_func=count_size_bytes)
        for n, size in sizes.iteritems():
	    print_metric('volumes_size', n, size)

        snaps_details = self.get_objects_details('cinder', 'snapshots')
        status_snaps = self.count_objects_group_by(snaps_details,
                                                   group_by_func=groupby)
        for s, nb in status_snaps.iteritems():
	    print_metric('snapshots', s, nb)

        sizes = self.count_objects_group_by(snaps_details,
                                            group_by_func=groupby,
                                            count_func=count_size_bytes)
        for n, size in sizes.iteritems():
            print_metric('snapshots_size', n, size)

class CinderServiceStats(dbi.ServiceStatus):
    def read_sql(self, conf, service_name):
	return [conf.get('cinder', 'services_down'),
		conf.get('cinder', 'services_up'),
		conf.get('cinder', 'services_disable')]

    def print_metric(self, host, status):
	for stats in status:
	    service, state = re.findall(r'^services\.(.+)\.([^.]+)$', stats[0])[0]
	    
	    print('%s cinder[openstack_cinder_services|service=%s|state=%s] %d' %
		(host, service, state, stats[1]))

if __name__ == "__main__":
#    pydevd.settrace('192.168.22.148', port=9901, stdoutToServer=True, stderrToServer=True)
    if len(sys.argv) > 1:
        host = sys.argv[1]
	service = CinderServiceStats(PLUGIN_NAME)
	service.itermetrics(host)
        plugin = CinderStatsPlugin()
        plugin.itermetrics(host)
    else:
        print('Usage:./%s host' % sys.argv[0])
