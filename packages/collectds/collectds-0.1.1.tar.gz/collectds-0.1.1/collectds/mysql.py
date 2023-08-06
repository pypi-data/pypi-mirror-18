#!/usr/bin/env python
# Original Author: Mirantis, Inc
# Substantial additions by SSCC(R&D Center,YouMingyang)
# Description: Collect the status of MySQL
#import pydevd
import sys

import dbi

PLUGIN_NAME = 'mysql' 

class MySQLStats(dbi.ServiceStatus):
    def read_sql(self, conf, service_name):
	return [
		conf.get('mysql', 'wsrep_ready'),
		conf.get('mysql', 'wsrep_cluster_status'),
		conf.get('mysql', 'wsrep_cluster')
		]
    
    def print_metric(self, host, status):
	for stats in status:
	    metric_name = 'mysql_' + '_'.join(stats[0].split('.'))
	    print('%s mysql[%s] %d' % (host, metric_name, int(stats[1])))

if __name__ == "__main__":
#    pydevd.settrace('192.168.22.148', port=9901, stdoutToServer=True,
#       stderrToServer=True)  
    if len(sys.argv) > 1:
        host = sys.argv[1]
        service = MySQLStats(PLUGIN_NAME)
        service.itermetrics(host)
    else:
        print('Usage:./%s host' % sys.argv[0])		
