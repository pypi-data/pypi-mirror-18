#!/usr/bin/env python
# Author: SSCC(R&D Center, YouMingyang)
# Description: This is a base class for query the status of OpenStack
# Nova, Cinder And Neutron.
import MySQLdb
import sys
import ConfigParser

class DBI(object):
    """
    class for using MySQL to query the status of OpenStack 
    services
    """
    def __init__(self, db_config):
	try:
	    self._conn = MySQLdb.connect(
		host = db_config['host'],
		user = db_config['user'],
		passwd = db_config['passwd'],
		db = db_config['dbname'],
		charset = 'utf8')
	except MySQLdb.Error, e:
	    raise Exception(e.args[0] + ":" + e.args[1])
	self._cur = self._conn.cursor()
    
    def query(self, sqlStr):
	try:
	    result = self._cur.execute(sqlStr)
	    return self._cur.fetchall()
	except MySQLdb.Error, e:
	    raise Exception(e.args[0] + ":" + e.args[1])

    def close(self):
	try:
	    self._cur.close()
	    self._conn.close()
	except:
	   pass

class ServiceStatus(object):
    """
    Read the OpenStack MySQL configuration for database nova, cinder 
    and neutron. References: /etc/collectd/conf.d/dbi_[nova|cinder|
    neutron]_[services|agents].conf
    """
    def __init__(self, service_name):
    	self.config_path = '/usr/local/etc/zabbix_agentd.d/scripts/openstack.conf' # config file path
	conf = ConfigParser.ConfigParser()
        conf.read(self.config_path)
    	self.db_config = self.read_config(conf, service_name)
	self.sql = self.read_sql(conf, service_name)
	
    def read_config(self, conf, service_name):
	return {
	    'host' : conf.get(service_name, 'host'),
	    'user' : conf.get(service_name, 'username'),
	    'passwd' : conf.get(service_name, 'password'),
            'dbname' : conf.get(service_name, 'dbname')
    	}
	
    def read_sql(self, conf, service_name):
	#read query sql statements
	raise NotImplemented("Must be implemented by the subclass!")
    
    def print_metric(self, host, status):
	raise NotImplemented("Must be implemented by the subclass!")

    # query service status 
    def itermetrics(self, host):
	dbi = DBI(self.db_config)
	
	for sqlStr in self.sql:
            self.print_metric(host, dbi.query(sqlStr))
	
	dbi.close()
