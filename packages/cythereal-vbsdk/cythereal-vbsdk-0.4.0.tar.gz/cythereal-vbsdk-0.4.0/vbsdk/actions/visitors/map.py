import os
import sys
import traceback
import logging
from vbsdk.vbBase import VBVisitor, ensure_dir

logger=logging.getLogger('vbsdk.py')

class MapVisitor (VBVisitor):
    """
     Produces CSV map files containing parent-child relationships
    """
    def __init__ (self, options):
        self.options = options
        self.outdir = self.options.outdir
        ensure_dir (self.outdir)
    def __enter__(self):
        # create output directory, if it doesn't exists
        return self
    def __exit__(self,type,value,tracebackObj):
        if value:
            #log error
            exc_type, value, exc_traceback =sys.exc_info()
            tb= repr(traceback.extract_tb(exc_traceback))
            logger.error('Error type: %s\nError Value: %s\nTraceback:%s'%(str(exc_type),str(repr(value)),str(tb)))

    def get_csv_file(self, service_name):
        return os.path.join(self.outdir, 'vb-'+service_name+'.map')

    def visit (self, objID, result):
        logger.debug('[%s] Visiting with result %r' % (objID, result))
        children = result.get('children', [])
        for child in children:
            service_name = str(child['service_name'])
            childID = child['child']
            # skip, if childID is none
            if childID is None: continue
            # append the pair (objID and childID) in appropriate cs csvfile
            filename = self.get_csv_file (service_name)
            with open(filename, 'a') as out:
                logger.debug("[%s] Child: %s, type: %s" %(objID, childID, service_name) )
                out.write("%s,%s\n" %(objID, childID))
