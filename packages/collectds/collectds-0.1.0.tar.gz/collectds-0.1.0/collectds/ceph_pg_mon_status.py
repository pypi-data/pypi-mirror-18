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

# Function: Collect states and information about ceph cluster and placement groups
# Modified by: You
import base
import sys

class CephMonPlugin(base.Base):

    def __init__(self, *args, **kwargs):
        super(CephMonPlugin, self).__init__(*args, **kwargs)
        self.plugin = 'ceph_mon'

    def itermetrics(self, host):
        status = self.execute_to_json('ceph -s --format json')
        if not status:
            return

        HEALTH_MAP = {
            'HEALTH_OK': 1,
            'HEALTH_WARN': 2,
            'HEALTH_ERR': 3
        }
	
	ceph_status = HEALTH_MAP[status['health']['overall_status']]

	# if status is HEAD_WARN but noout flag is set, then set status ok
	if ceph_status == 2:
		flag = status['health']['summary'][0]['summary']
		if flag.find('noout') != -1:
			ceph_status = 1
	
        print('%s ceph[health] %d' % (host, ceph_status))

        if 'mons' in status['monmap']:
            monitor_nb = len(status['monmap']['mons'])
        else:
            monitor_nb = 0

        print('%s ceph[monitor_count] %d' % (host, monitor_nb))
        print('%s ceph[quorum_count] %d' % (host, len(status.get('quorum', []))))

        pgmap = status['pgmap']
        
        print('%s ceph[pg_bytes_bytes_used] %d' % (host, pgmap['bytes_used']))
        print('%s ceph[pg_bytes_bytes_avail] %d' % (host, pgmap['bytes_avail']))
        print('%s ceph[pg_bytes_bytes_total] %d' % (host, pgmap['bytes_total']))
        print('%s ceph[pg_data_bytes] %d' % (host, pgmap['data_bytes']))
        print('%s ceph[pg_count] %d' % (host, pgmap['num_pgs']))


        for state in pgmap['pgs_by_state']:
            print('%s ceph[pg_state_count_%s] %d' % (host, state['state_name'], state['count']))

if __name__ == "__main__":
#    pydevd.settrace('192.168.22.148', port=9901, stdoutToServer=True, stderrToServer=True)
    if len(sys.argv) > 1:
        host = sys.argv[1]
        plugin = CephMonPlugin()
        plugin.itermetrics(host)
    else:
        print('Usage:./%s host' % sys.argv[0])
