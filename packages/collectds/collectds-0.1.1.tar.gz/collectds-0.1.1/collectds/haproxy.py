#!/usr/bin/env python
# haproxy-collectd-plugin - haproxy.py
# 
# Original Author: Michael Leinartas
# Substantial additions by Mirantis, SSCC(R&D Center,YouMingyang)
# Description: This is a collectd plugin which runs under the Python plugin to
# collect metrics from haproxy.
# Plugin structure and logging func taken from https://github.com/phrawzty/rabbitmq-collectd-plugin

# Copyright (c) 2011 Michael Leinartas
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import sys
#import pydevd
import socket
import csv
import re

NAME = 'haproxy'
RECV_SIZE = 1024
METRIC_TYPES = {
  'bin': ('bytes_in', 'gauge'),
  'bout': ('bytes_out', 'gauge'),
  'chkfail': ('failed_checks', 'gauge'),
  'CurrConns': ('connections', 'gauge'),
  'CurrSslConns': ('ssl_connections', 'gauge'),
  'downtime': ('downtime', 'gauge'),
  'dresp': ('denied_responses', 'gauge'),
  'dreq': ('denied_requests', 'gauge'),
  'econ': ('error_connection', 'gauge'),
  'ereq': ('error_requests', 'gauge'),
  'eresp': ('error_responses', 'gauge'),
  'hrsp_1xx': ('response_1xx', 'gauge'),
  'hrsp_2xx': ('response_2xx', 'gauge'),
  'hrsp_3xx': ('response_3xx', 'gauge'),
  'hrsp_4xx': ('response_4xx', 'gauge'),
  'hrsp_5xx': ('response_5xx', 'gauge'),
  'hrsp_other': ('response_other', 'gauge'),
  'PipesUsed': ('pipes_used', 'gauge'),
  'PipesFree': ('pipes_free', 'gauge'),
  'qcur': ('queue_current', 'gauge'),
  'Tasks': ('tasks', 'gauge'),
  'Run_queue': ('run_queue', 'gauge'),
  'stot': ('session_total', 'gauge'),
  'scur': ('session_current', 'gauge'),
  'wredis': ('redistributed', 'gauge'),
  'wretr': ('retries', 'gauge'),
  'status': ('status', 'gauge'),
  'Uptime_sec': ('uptime', 'gauge'),
  'up': ('up', 'gauge'),
  'down': ('down', 'gauge'),
}

STATUS_MAP = {
    'DOWN': 0,
    'UP': 1,
}

FRONTEND_TYPE = '0'
BACKEND_TYPE = '1'
BACKEND_SERVER_TYPE = '2'

METRIC_AGGREGATED = ['bin', 'bout', 'qcur','scur','eresp',
                     'hrsp_1xx','hrsp_2xx', 'hrsp_3xx', 'hrsp_4xx', 'hrsp_5xx',
                     'hrsp_other', 'wretr']


METRIC_DELIM = '.' # for the frontend/backend stats

DEFAULT_SOCKET = '/var/lib/haproxy/stats'
DEFAULT_PROXY_MONITORS = [ 'server', 'frontend', 'backend', 'backend_server' ]


class HAProxySocket(object):
  def __init__(self, socket_file=DEFAULT_SOCKET):
    self.socket_file = socket_file

  def connect(self):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect(self.socket_file)
    return s

  def communicate(self, command):
    ''' Send a single command to the socket and return a single response (raw string) '''
    s = self.connect()
    if not command.endswith('\n'): command += '\n'
    s.send(command)
    result = ''
    buf = ''
    buf = s.recv(RECV_SIZE)
    while buf:
      result += buf
      buf = s.recv(RECV_SIZE)
    s.close()
    return result

  def get_server_info(self):
    result = {}
    output = self.communicate('show info')
    for line in output.splitlines():
      try:
        key,val = line.split(':')
      except ValueError, e:
        continue
      result[key.strip()] = val.strip()
    return result

  def get_server_stats(self):
    output = self.communicate('show stat')
    #sanitize and make a list of lines
    output = output.lstrip('# ').strip()
    output = [ l.strip(',') for l in output.splitlines() ]
    csvreader = csv.DictReader(output)
    result = [ d.copy() for d in csvreader ]
    return result

def get_stats():
  stats = dict()
  haproxy = HAProxySocket(HAPROXY_SOCKET)

  try:
    server_info = haproxy.get_server_info()
    server_stats = haproxy.get_server_stats()
  except socket.error, e:
    sys.stderr.write("status err Unable to connect to HAProxy socket at %s" % HAPROXY_SOCKET)
    return stats

  if 'server' in PROXY_MONITORS:
    for key,val in server_info.items():
      try:
        stats[key] = int(val)
      except (TypeError, ValueError), e:
        pass

  for statdict in server_stats:
    if not (statdict['svname'].lower() in PROXY_MONITORS or
            statdict['pxname'].lower() in PROXY_MONITORS or
            ('backend_server' in PROXY_MONITORS and
             statdict['type'] == BACKEND_SERVER_TYPE)):
      continue

    if statdict['pxname'] in PROXY_IGNORE:
      continue

    pxname = statdict['pxname']
    # Translate to meaningful names
    if pxname in NAMES_MAPPING:
        pxname = NAMES_MAPPING.get(pxname)
    else:
      sys.stderr.write('Mapping missing for "%s"' % pxname)

    if statdict['type'] == BACKEND_SERVER_TYPE:
      # Count the number of servers per backend and per status
      for status_val in STATUS_MAP.keys():
        # Initialize all possible metric keys to zero
        metricname = METRIC_DELIM.join(['backend', pxname, 'servers', status_val.lower()])
        if metricname not in stats:
          stats[metricname] = 0
        if statdict['status'] == status_val:
          stats[metricname] += 1
      continue

    for key, val in statdict.items():
      metricname = METRIC_DELIM.join([statdict['svname'].lower(), pxname, key])
      try:
        if key == 'status' and statdict['type'] == BACKEND_TYPE:
          if val in STATUS_MAP:
            val = STATUS_MAP[val]
          else:
            continue
        stats[metricname] = int(val)
        if key in METRIC_AGGREGATED:
          agg_metricname = METRIC_DELIM.join([statdict['svname'].lower(), key])
          if agg_metricname not in stats:
            stats[agg_metricname] = 0
          stats[agg_metricname] += int(val)
      except (TypeError, ValueError), e:
        pass
  return stats

# configure global variables.
# values reference /etc/collectd/conf.d/openstack.conf#haproxy
def config():
  global PROXY_MONITORS, PROXY_IGNORE, HAPROXY_SOCKET, NAMES_MAPPING
  PROXY_MONITORS = [ ]
  PROXY_IGNORE = [ ]
  HAPROXY_SOCKET = DEFAULT_SOCKET
 

  proxyIgnore = ['Stats', 'lma', 'stats']
  PROXY_IGNORE.extend(proxyIgnore)
  HAPROXY_SOCKET = '/var/lib/haproxy/stats'
  NAMES_MAPPING = {
    'cinder-api' : 'cinder-api',
    'glance-api' : 'glance-api',
    'glance-registry' : 'glance-registry-api',
    'heat-api' : 'heat-api',
    'heat-api-cfn' : 'heat-cfn-api',
    'heat-api-cloudwatch' : 'heat-cloudwatch-api',
    'horizon' : 'horizon-web',
    'horizon-ssl' : 'horizon-https',
    'keystone-1' : 'keystone-public-api',
    'keystone-2' : 'keystone-admin-api',
    'murano' : 'murano-api',
    'mysqld' : 'mysqld-tcp',
    'neutron' : 'neutron-api',
    'nova-api-1' : 'nova-ec2-api',
    'nova-api-2' : 'nova-api',
    'nova-metadata-api' : 'nova-metadata-api',
    'nova-novncproxy' : 'nova-novncproxy-websocket',
    'sahara' : 'sahara-api',
    'swift' : 'swift-api',
  }

  PROXY_MONITORS += DEFAULT_PROXY_MONITORS
  PROXY_MONITORS = [ p.lower() for p in PROXY_MONITORS ]

# print the metrics collect from haproxy
def itermetrics(host):
  info = get_stats()

  if not info:
    sys.stderr.write("%s: No data received" % NAME)
    return
  
  for key,value in info.items():
    key_prefix = ''
    key_root = key
    if not value in METRIC_TYPES:
      try:
        key_prefix, key_root = key.rsplit(METRIC_DELIM,1)
      except ValueError, e:
        pass
    if not key_root in METRIC_TYPES:
      continue

    key_root, val_type = METRIC_TYPES[key_root]
    key_name = METRIC_DELIM.join([ n for n in [key_prefix, key_root] if n ])
    metric_name, side, name, m, state = '', None, '', '', None

    if not re.match(r'^(frontend|backend)', key_name):
      metric_name = NAME + '_' + key_name
    else:
      match = re.findall(r'([^.]+)', key_name)
      lens = len(match)

      if lens == 4:
	side, name, m, state = match
      elif lens == 3:
	side, name, m = match
      else:
	sys.stderr.write("%s: Data droped" % key_name)
	continue

      metric_name = NAME + '_' + side + '_' + m
    
    if state:
      print('%s haproxy[%s|%s=%s|state=%s] %d' % (host, metric_name, side, name, state,value))	
    elif side:
      print('%s haproxy[%s|%s=%s] %d' % (host, metric_name, side, name, value))
    else:
      print('%s haproxy[%s] %d' % (host, metric_name, value))

if __name__ == "__main__":
#    pydevd.settrace('192.168.22.148', port=9901, stdoutToServer=True, stderrToServer=True)
  if len(sys.argv) > 1:
    host = sys.argv[1]
    config()
    itermetrics(host)
  else:
    print('Usage:./%s host' % sys.argv[0])
