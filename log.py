#!/usr/bin/env python

from colorlog.colorlog import ColoredFormatter
import os
from config import DEBUG,LOGFILE
import logging 
import sys

def initlog(file):
	logger=logging.getLogger()
        if file == 'STDOUT':
	    hdlr=logging.StreamHandler(sys.stdout)
	else:
	    hdlr=logging.FileHandler(file)
	formatter=logging.Formatter('%(asctime)s %(levelname)s %(message)s','%Y-%m-%d %H:%M:%S')
	hdlr.setFormatter(formatter)
	logger.addHandler(hdlr)
        if DEBUG is True:
	    logger.setLevel(logging.NOTSET)
        else:
	    logger.setLevel(logging.INFO)


	return logger

logger=initlog(LOGFILE)

if __name__ == '__main__':
	print(DEBUG)
	print(LOGFILE)
