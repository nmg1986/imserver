import ConfigParser
import constant
import os
import getoptions
import sys

if os.path.isfile(constant.DEFAULT_CONFIG_FILE):
	parser=ConfigParser.SafeConfigParser()
	parser.read("C:\hbimserver.ini")
	
	SERVER_PORT=parser.get("main","SERVER_PORT")
	
	DB_HOST=parser.get("database","DB_HOST")
	DB_PORT=parser.get("database","DB_PORT")
	DB_NAME=parser.get("database","DB_NAME")
	DB_USER=parser.get("database","DB_USER")
	DB_PASSWD=parser.get("database","DB_PASSWD")
	
	if getoptions.options.DEBUG:
	    DEBUG=True
	    LOGFILE='STDOUT'
	else:
	    DEBUG=parser.get("log","DEBUG")
	    LOGFILE=parser.get("log","LOGFILE")
else:
	SERVER_PORT=6800
	DB_HOST='localhost'
	DB_PORT='3306'
	DB_NAME='imserver'
	DB_USER='root'
	DB_PASSWD='P@ssw0rd'

	if getoptions.options.DEBUG:
	    DEBUG=True
	    LOGFILE='STDOUT'
	else:
	    DEBUG=False
	    LOGFILE='/var/log/imserver.log'
