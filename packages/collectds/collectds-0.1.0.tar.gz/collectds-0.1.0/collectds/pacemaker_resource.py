#!/usr/bin/env python
# Original Author: Mirantis, Inc
# Substantial additions by SSCC(R&D Center,YouMingyang)
# Description: plugin for collect status of pacemaker resource
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
import ConfigParser
#import pydevd
import socket

import base

NAME = 'pacemaker_resource'
CRM_RESOURCE_BIN = '/usr/sbin/crm_resource'


class PacemakerResourcePlugin(base.Base):

    def __init__(self, *args, **kwargs):
        super(PacemakerResourcePlugin, self).__init__(*args, **kwargs)
        self.plugin = NAME
        self.crm_resource_bin = CRM_RESOURCE_BIN
        self.hostname = socket.getfqdn()
	self.config()

    def config(self):
	config_path = '/usr/local/etc/zabbix_agentd.d/scripts/openstack.conf' # config file path
        conf = ConfigParser.ConfigParser()
        conf.read(config_path)
	self.resources = conf.get('pacemaker_resource', 'resources').split(',')

    def itermetrics(self, host):
        for resource in self.resources:
            out, err = self.execute([self.crm_resource_bin, '--locate',
                                     '--quiet', '--resource', resource],
                                    shell=False)
            if not out:
                sys.stderr.write("%s: Failed to get the status for '%s'" %
                                  (self.plugin, resource))

            else:
                value = 0
                if self.hostname == out.lstrip("\n"):
                    value = 1
                print('%s pacemaker[pacemaker_local_resource_active|resource=%s] %d' %
		    (host, resource, value))


if __name__ == "__main__":
#    pydevd.settrace('192.168.22.148', port=9901, stdoutToServer=True, stderrToServer=True)
    if len(sys.argv) > 1:
        host = sys.argv[1]
        plugin = PacemakerResourcePlugin()
        plugin.itermetrics(host)
    else:
        print('Usage:./%s host' % sys.argv[0])
