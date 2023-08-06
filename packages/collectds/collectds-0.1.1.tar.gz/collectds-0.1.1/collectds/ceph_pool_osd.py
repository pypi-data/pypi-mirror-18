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

# Funtion Collect Ceph pool metrics and OSD daemons state
# Modified by: You
import base
import sys

class CephPoolPlugin(base.Base):

    def __init__(self, *args, **kwargs):
        super(CephPoolPlugin, self).__init__(*args, **kwargs)
        self.plugin = 'ceph_pool'

    def itermetrics(self, host):
        df = self.execute_to_json('ceph df --format json')
        if not df:
            return

        objects_count = 0
        for pool in df['pools']:
            objects_count += pool['stats'].get('objects', 0)
            for m in ('bytes_used', 'max_avail', 'objects'):
                print('%s ceph[pool_%s_%s] %d' % 
                    (host, m, pool['name'],pool['stats'].get(m, 0)))

        print('%s ceph[objects_count] %d' % (host, objects_count))
        print('%s ceph[pool_count] %d' % (host, len(df['pools'])))

        if 'total_bytes' in df['stats']:
            # compatibility with 0.84+
            total = df['stats']['total_bytes']
            used = df['stats']['total_used_bytes']
            avail = df['stats']['total_avail_bytes']
        else:
            # compatibility with <0.84
            total = df['stats']['total_space'] * 1024
            used = df['stats']['total_used'] * 1024
            avail = df['stats']['total_avail'] * 1024

        print('%s ceph[pool_total_bytes_used] %d' % (host, used))
        print('%s ceph[pool_total_bytes_avail] %d' % (host, avail))
        print('%s ceph[pool_total_bytes_total] %d' % (host, total))
        print('%s ceph[pool_total_percent_used] %f' % 
            (host, (100.0 * used / total)))
        print('%s ceph[pool_total_percent_free] %f' % 
            (host, (100.0 * avail / total)))

        stats = self.execute_to_json('ceph osd pool stats --format json')
        if not stats:
            return

        for pool in stats:
            client_io_rate = pool.get('client_io_rate', {})
            print('%s ceph[pool_bytes_rate_read_bytes_sec_%s] %d' %
                (host, pool['pool_name'], client_io_rate.get('read_bytes_sec', 0)))
            print('%s ceph[pool_bytes_rate_write_bytes_sec_%s] %d' %
                (host, pool['pool_name'], client_io_rate.get('write_bytes_sec', 0)))
            print('%s ceph[pool_ops_rate_op_per_sec_%s] %d' %
                (host, pool['pool_name'], client_io_rate.get('op_per_sec', 0)))

        osd = self.execute_to_json('ceph osd dump --format json')
        if not osd:
            return

        for pool in osd['pools']:
            for name in ('size', 'pg_num', 'pg_placement_num'):
                print('%s ceph[pool_%s_%s] %d' % 
                    (host, name, pool['pool_name'], pool[name]))

        _up, _down, _in, _out = (0, 0, 0, 0)
        for osd in osd['osds']:
            if osd['up'] == 1:
                _up += 1
            else:
                _down += 1
            if osd['in'] == 1:
                _in += 1
            else:
                _out += 1

        print('%s ceph[osd_count_up] %d' %  (host, _up))
        print('%s ceph[osd_count_down] %d' %  (host, _down))
        print('%s ceph[osd_count_in] %d'  % (host, _in))
        print('%s ceph[osd_count_out] %d' % (host, _out))

if __name__ == "__main__":
#    pydevd.settrace('192.168.22.148', port=9901, stdoutToServer=True, stderrToServer=True)
    if len(sys.argv) > 1:
        host = sys.argv[1]
        plugin = CephPoolPlugin()
        plugin.itermetrics(host)
    else:
        print('Usage:./%s host' % sys.argv[0])
