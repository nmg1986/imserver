#!/usr/bin/env python2.7

from optparse import OptionParser

parser=OptionParser()
parser.add_option(
		  "-d",
		  "--debug",
                  help="run in debug mode",
                  action="store_true",
		  dest="DEBUG"
		 )

(options,args)=parser.parse_args()

if __name__=='__main__':
    print options.DEBUG
