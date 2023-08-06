import os
import sys
import traceback
import json
import logging
from vbsdk.vbBase import VBVisitor

logger=logging.getLogger('vbsdk.py')

class QueryVisitor (VBVisitor):
    def __init__ (self, options):
        self.options = options
        self.sep = ""
    def __enter__(self):
        print '['
        self.sep=""
        return self
    def __exit__(self,type,value,tracebackObj):
        print ']'
        if value:
            #log error
            exc_type, value, exc_traceback =sys.exc_info()
            tb= repr(traceback.extract_tb(exc_traceback))
            logger.error('Error type: %s\nError Value: %s\nTraceback:%s'%(str(exc_type),str(repr(value)),str(tb)))

    def visit (self, objID, result):
        print self.sep+json.dumps(result, indent=2)
        self.sep=",\n"
