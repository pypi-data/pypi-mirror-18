#!  /usr/bin/env python

import json
import os
import sys
import traceback
import logging
import requests
import re

logger = logging
from optparse import OptionParser
import virusbattle


class User (object):
        def __init__ (self):
		pass

        def register (self, useremail, name):
		url =  virusbattle.make_vburl("register", usekey=False, email=useremail, name=name)
		print url
		results = requests.get(url)
		return results


error_flag = False
def record_error (msg):
	global error_flag
	print "[ERROR]" + msg
	error_flag = True

def assert_noerror ():
	if error_flag: sys.exit(1)

def process (args, options):
	if options.email is None:
		record_error ("Must provide email using --email")
	if options.name is None:
		record_error ("Must provide name using --name")

	assert_noerror ()
	try:
		result = User().register (options.email, name=options.name)
		return result
	except Exception as e:
		print 'An internal error was encountered: %s' % repr(e)


loglevels = {"info": logging.INFO, "debug": logging.DEBUG, "warn": logging.WARN, "error": logging.ERROR}

default_loglevel = "info"

if __name__ == "__main__":
        parser = OptionParser()
        parser.add_option("--email", dest="email", 
                          help="Provide email address for registration")
        parser.add_option("--name", dest="name", 
                          help="Provide name for registration")

	parser.add_option("--loglevel", dest="loglevel", default=default_loglevel,
			  help="Select log level. One of: %s. Default is: %s" % (", ".join(loglevels.keys()), default_loglevel)) 

        (options, args) = parser.parse_args()

	if not options.loglevel in loglevels.keys():
		print "ERROR - in correct log level %s, use -h to get help" % options.loglevel
		sys.exit (1)

	logging.basicConfig(format='%(asctime)s %(message)s', level=loglevels[options.loglevel])

        results = process (args, options)
	logger.info("Server returned: %s"%(results.content))

