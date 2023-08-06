#!/usr/bin/env python
# Original Author: Mirantis, Inc
# Substantial additions by SSCC(R&D Center,YouMingyang)
# Description: plugin for getting resource statistics from Glance
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import sys
import re
#import pydevd

import openstack

PLUGIN_NAME = 'glance'


class GlanceStatsPlugin(openstack.CollectdPlugin):
    """ Class to report the statistics on Glance service.

        number of image broken down by state
        total size of images usable and in error state
    """

    def itermetrics(self, host):

        def is_snap(d):
            return d.get('properties', {}).get('image_type') == 'snapshot'

        def groupby(d):
            p = 'public' if d.get('is_public', True) else 'private'
            status = d.get('status', 'unknown').lower()
            if is_snap(d):
                return 'snapshots.%s.%s' % (p, status)
            return 'images.%s.%s' % (p, status)

        images_details = self.get_objects_details('glance', 'images',
                                                  api_version='v1',
                                                  params='is_public=None')
        status = self.count_objects_group_by(images_details,
                                             group_by_func=groupby)
	
	def print_metric(name, value):
	    resource, visibility, state = re.findall('^([^.]+)\.([^.]+)\.(.+)$', 
		name)[0]
	    metric_name = 'openstack_glance_' + resource.replace('.', '_')
	    print('%s glance[%s|state=%s|visibility=%s] %d' %
		(host, metric_name, state, visibility, value))

        for s, nb in status.iteritems():
	    print_metric(s, nb)

        # sizes
        def count_size_bytes(d):
            return d.get('size', 0)

        def groupby_size(d):
            p = 'public' if d.get('is_public', True) else 'private'
            status = d.get('status', 'unknown').lower()
            if is_snap(d):
                return 'snapshots_size.%s.%s' % (p, status)
            return 'images_size.%s.%s' % (p, status)

        sizes = self.count_objects_group_by(images_details,
                                            group_by_func=groupby_size,
                                            count_func=count_size_bytes)
        for s, nb in sizes.iteritems():
	    print_metric(s, nb)

if __name__ == "__main__":
#    pydevd.settrace('192.168.22.148', port=9901, stdoutToServer=True, stderrToServer=True)
    if len(sys.argv) > 1:
        host = sys.argv[1]
        plugin = GlanceStatsPlugin()
        plugin.itermetrics(host)
    else:
        print('Usage:./%s host' % sys.argv[0])
