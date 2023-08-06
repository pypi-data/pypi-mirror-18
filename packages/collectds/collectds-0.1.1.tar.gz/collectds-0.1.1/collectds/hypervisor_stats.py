#!/usr/bin/env python
# Copyright 2015 Mirantis, Inc.
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
#
# Collectd plugin for getting hypervisor statistics from Nova
import sys
import re
#import pydevd

import openstack

PLUGIN_NAME = 'hypervisor_stats'


class HypervisorStatsPlugin(openstack.CollectdPlugin):
    """ Class to report the statistics on Nova hypervisors.
    """
    VALUE_MAP = {
        'current_workload': 'total_running_tasks',
        'running_vms': 'total_running_instances',
        'local_gb_used': 'total_used_disk_GB',
        'free_disk_gb': 'total_free_disk_GB',
        'memory_mb_used': 'total_used_ram_MB',
        'free_ram_mb': 'total_free_ram_MB',
        'vcpus_used': 'total_used_vcpus',
    }

    def config(self):
        self.extra_config['cpu_ratio'] = 8.0

    def itermetrics(self, host):
        r = self.get('nova', 'os-hypervisors/statistics')
        if not r:
            sys.stderr.write("Could not get hypervisor statistics")
            return

        stats = r.json().get('hypervisor_statistics', {})
	
	def print_metric(type_instance, value):
	    match = re.findall('^(.+)_(.B)$', type_instance)
	    if len(match) == 1:
		name, unit = match[0]
                metric_name = 'openstack_nova_' + name
                print('%s hypervisor[%s|unit=%s] %d' % 
		    (host, metric_name, unit, value))
            else:
                metric_name = 'openstack_nova_' + type_instance
                print('%s hypervisor[%s] %d' % (host, metric_name, value))

        for k, v in self.VALUE_MAP.iteritems():
	    print_metric(v, stats.get(k, 0))
        if 'cpu_ratio' in self.extra_config:
            vcpus = int(self.extra_config['cpu_ratio'] * stats.get('vcpus', 0))
            print_metric('total_free_vcpus', vcpus - stats.get('vcpus_used', 0))


if __name__ == "__main__":
#    pydevd.settrace('192.168.22.148', port=9901, stdoutToServer=True, stderrToServer=True)
    if len(sys.argv) > 1:
        host = sys.argv[1]
        plugin = HypervisorStatsPlugin()
	plugin.config()
        plugin.itermetrics(host)
    else:
        print('Usage:./%s host' % sys.argv[0])
