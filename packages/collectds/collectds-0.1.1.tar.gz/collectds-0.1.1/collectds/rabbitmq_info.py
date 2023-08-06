#!/usr/bin/env python
# Name: rabbitmq-collectd-plugin - rabbitmq_info.py
# Originnal Author: https://github.com/phrawzty/rabbitmq-collectd-plugin
# /commits/master
# Substantial additions by SSCC(R&D Center,YouMingyang)
# Description: This plugin uses Collectd's Python plugin to obtain RabbitMQ
# metrics.
#
# Copyright 2012 Daniel Maher
# Copyright 2015 Mirantis, Inc.
# Copyright 2016 SSCC, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
#import pydevd
import re

import base


NAME = 'rabbitmq_info'
# Override in config by specifying 'RmqcBin'.
RABBITMQCTL_BIN = '/usr/sbin/rabbitmqctl'
# Override in config by specifying 'PmapBin'
PMAP_BIN = '/usr/bin/pmap'
# Override in config by specifying 'Vhost'.
VHOST = "/"

# Used to find disk nodes and running nodes.
CLUSTER_STATUS = re.compile('.*disc,\[([^\]]+)\].*running_nodes,\[([^\]]+)\]',
                            re.S)


class RabbitMqPlugin(base.Base):

    # we need to substract the length of the longest prefix (eg '.consumers')
    MAX_QUEUE_IDENTIFIER_LENGTH = 53

    def __init__(self, *args, **kwargs):
        super(RabbitMqPlugin, self).__init__(*args, **kwargs)
        self.plugin = NAME
        self.rabbitmqctl_bin = RABBITMQCTL_BIN
        self.pidfile = None
        self.pmap_bin = PMAP_BIN
        self.vhost = VHOST

    def itermetrics(self, host):
        stats = {}
        stats['messages'] = 0
        stats['memory'] = 0
        stats['consumers'] = 0
        stats['queues'] = 0
        stats['unmirrored_queues'] = 0
        stats['pmap_mapped'] = 0
        stats['pmap_used'] = 0
        stats['pmap_shared'] = 0

        out, err = self.execute([self.rabbitmqctl_bin, '-q', 'status'],
                                shell=False)
        if not out:
            sys.stderr.write('%s: Failed to get the status' %
                              self.rabbitmqctl_bin)
            return

        for v in ('vm_memory_limit', 'disk_free_limit', 'disk_free'):
            try:
                stats[v] = int(re.findall('{%s,([0-9]+)}' % v, out)[0])
            except:
                sys.stderr.write('%s: Failed to get %s' %
                                  (self.rabbitmqctl_bin, v))

        mem_str = re.findall('{memory,\s+\[([^\]]+)\]\}', out)
        # We are only interested by the total of memory used
        # TODO: Get all informations about memory usage from mem_str
        try:
            stats['used_memory'] = int(re.findall('total,([0-9]+)',
                                                  mem_str[0])[0])
        except:
            sys.stderr.write('%s: Failed to get the memory used by rabbitmq' %
                              self.rabbitmqctl_bin)

        if 'vm_memory_limit' in stats and 'used_memory' in stats:
            stats['remaining_memory'] = stats['vm_memory_limit'] - stats['used_memory']
        if 'disk_free' in stats and 'disk_free_limit' in stats:
            stats['remaining_disk'] = stats['disk_free'] - stats['disk_free_limit']

        out, err = self.execute([self.rabbitmqctl_bin, '-q', 'cluster_status'],
                                shell=False)
        if not out:
            sys.stderr.write('%s: Failed to get the cluster status' %
                              self.rabbitmqctl_bin)
            return

        # TODO: Need to be modified in case we are using RAM nodes.
        status = CLUSTER_STATUS.findall(out)
        if len(status) == 0:
            sys.stderr.write('%s: Failed to parse (%s)' %
                              (self.rabbitmqctl_bin, out))
        else:
            stats['total_nodes'] = len(status[0][0].split(","))
            stats['running_nodes'] = len(status[0][1].split(","))

        out, err = self.execute([self.rabbitmqctl_bin, '-q',
                                 'list_connections'], shell=False)
        if not out:
            sys.stderr.write('%s: Failed to get the number of connections' %
                              self.rabbitmqctl_bin)
            return
        stats['connections'] = len(out.split('\n'))

        out, err = self.execute([self.rabbitmqctl_bin, '-q', 'list_exchanges'],
                                shell=False)
        if not out:
            sys.stderr.write('%s: Failed to get the number of exchanges' %
                              self.rabbitmqctl_bin)
            return
        stats['exchanges'] = len(out.split('\n'))

        out, err = self.execute([self.rabbitmqctl_bin, '-q', '-p', self.vhost,
                                 'list_queues', 'name', 'messages', 'memory',
                                 'consumers', 'slave_pids',
                                 'synchronised_slave_pids'], shell=False)
        if not out:
            sys.stderr.write('%s: Failed to get the list of queues' %
                              self.rabbitmqctl_bin)
            return

        for line in out.split('\n'):
            ctl_stats = line.split('\t')
            try:
                ctl_stats[1] = int(ctl_stats[1])
                ctl_stats[2] = int(ctl_stats[2])
                ctl_stats[3] = int(ctl_stats[3])
            except:
                continue
            queue_name = ctl_stats[0][:self.MAX_QUEUE_IDENTIFIER_LENGTH]
            stats['queues'] += 1
            stats['messages'] += ctl_stats[1]
            stats['memory'] += ctl_stats[2]
            stats['consumers'] += ctl_stats[3]
            stats['%s.messages' % queue_name] = ctl_stats[1]
            stats['%s.memory' % queue_name] = ctl_stats[2]
            stats['%s.consumers' % queue_name] = ctl_stats[3]
            # we need to check if the list of synchronised slaves is
            # equal to the list of slaves.
            try:
                slaves = re.findall('<([a-zA-Z@\-.0-9]+)>', ctl_stats[4])
                for s in slaves:
                    if s not in ctl_stats[5]:
                        stats['unmirrored_queues'] += 1
                        break
            except IndexError:
                pass

        if not stats['memory'] > 0:
            sys.stderr.write(
                '%s reports 0 memory usage. This is probably incorrect.' %
                self.rabbitmqctl_bin)

        # pmap metrics are only collected if the location of the pid file is
        # explicitly configured
        if self.pidfile:
            try:
                with open(self.pidfile, 'r') as f:
                    pid = f.read().strip()
            except:
                sys.stderr.write('Unable to read %s' % self.pidfile)
                return

            # use pmap to get proper memory stats
            out, err = self.execute([self.pmap_bin, '-d', pid], shell=False)
            if not out:
                sys.stderr.write('Failed to run %s' % self.pmap_bin)
                return

            out = out.split('\n')[-1]
            if re.match('mapped', out):
                m = re.match(r"\D+(\d+)\D+(\d+)\D+(\d+)", out)
                stats['pmap_mapped'] = int(m.group(1))
                stats['pmap_used'] = int(m.group(2))
                stats['pmap_shared'] = int(m.group(3))
            else:
                sys.stderr.write('%s returned something strange.' %
                                    self.pmap_bin)

        # TODO(pasquier-s): define and use own types instead of the generic
        # GAUGE type
        for k, v in stats.iteritems():
	    if (k not in ['consumers', 'messages', 'memory', 'used_memory',
		'unmirrored_queues', 'vm_memory_limit', 'disk_free_limit',
		'disk_free', 'remaining_memory', 'remaining_disk']) and (re.match('.+\.consumers$', k) or re.match('.+\.messages$', k) or re.match('.+\.memory$', k )):
		q, m = re.findall('^(.+)\.([^.]+)$', k)[0]
		metric_name = 'rabbitmq_queue_' + m
		print('%s rabbitmq[%s|queue=%s] %d' % (host, metric_name, q, v))
	    else:
		print('%s rabbitmq[rabbitmq_%s] %d' % (host, k, v))


if __name__ == "__main__":
#    pydevd.settrace('192.168.22.148', port=9901, stdoutToServer=True, stderrToServer=True)
    if len(sys.argv) > 1:
        host = sys.argv[1]
        plugin = RabbitMqPlugin()
        plugin.itermetrics(host)
    else:
        print('Usage:./%s host' % sys.argv[0])
