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

# Function: Collect per OSD stats about store size and commit latency
# Modified by: You
import base
import sys

class CephOSDStatsPlugin(base.Base):

    def __init__(self, *args, **kwargs):
        super(CephOSDStatsPlugin, self).__init__(*args, **kwargs)
        self.plugin = 'ceph_osd'

    def itermetrics(self, host):
        osd_stats = self.execute_to_json('ceph pg dump osds --format json')
        if not osd_stats:
            return

        for osd in osd_stats:
            osd_id = osd['osd']

            print("%s ceph[osd_%d_space_kb_used] %d" % 
                (host, osd_id, osd['kb_used'] * 1000))
            print("%s ceph[osd_%d_space_kb_total] %d" % 
                (host, osd_id, osd['kb'] * 1000))
            print("%s ceph[osd_%d_apply_latency_ms] %d" % 
                (host, osd_id, osd['fs_perf_stat']['apply_latency_ms']))
            print("%s ceph[osd_%d_commit_latency_ms] %d" % 
                (host, osd_id, osd['fs_perf_stat']['commit_latency_ms']))

if __name__ == "__main__":
#    pydevd.settrace('192.168.22.148', port=9901, stdoutToServer=True, stderrToServer=True)
    if len(sys.argv) > 1:
        host = sys.argv[1]
        plugin = CephOSDStatsPlugin()
        plugin.itermetrics(host)
    else:
        print('Usage:./%s host' % sys.argv[0])
