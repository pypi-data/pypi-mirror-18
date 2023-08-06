import os
import sys
import traceback
import logging
from vbsdk import virusbattle
from vbsdk.vbBase import VBVisitor, ensure_dir
import re

logger=logging.getLogger('vbsdk.py')

class ProgressMonitorVisitor (VBVisitor):
    """
     Produces CSV files containing progress indications
     Format: PE-Sha1,Unpacker_Status,Juice_Status
    """
    def __init__ (self, options):
        self.options = options
        self.service_list = virusbattle.service_list()
        self.service_header = ["sha1sum","object_class","uploadDate"]
        self.service_header.extend([re.match("srl(.*)", x).group(1)+"Status" for x in self.service_list])
        print(",".join(self.service_header))

    def __enter__(self):
        # create output directory, if it doesn't exists
        self.outdir = self.options.outdir
        ensure_dir (self.outdir)
        self.open_progress ()
        return self

    def open_progress (self):
        filename = os.path.join(self.outdir, 'vb-'+"progress"+'.csv')
        #logger.warn("Writing status check to %s" % filename)
        #self.outfp = open(filename, 'w')
        self.write_progress(",".join("PE-sha1,object_class,uploadDate".split(",")+self.service_header))

    def write_progress (self, message):
        print message
        #self.outfp.write("%s\n"% message)

    def close_progress (self):
        #self.outfp.close ()
        pass

    def __exit__(self,type,value,tracebackObj):
        if value:
            #log error
            exc_type, value, exc_traceback =sys.exc_info()
            tb= repr(traceback.extract_tb(exc_traceback))
            logger.error('Error type: %s\nError Value: %s\nTraceback:%s'%(str(exc_type),str(repr(value)),str(tb)))
        self.close_progress()

    def default_status (self, object_class):
        progress = {}
        for x in self.service_list: progress[x] = "Pending"
        if object_class in ["unhandled file type" , "unknown"]:
            for x in self.service_list: progress[x] = "n/a"
        if object_class == "binary.unpacked":
            progress['srlUnpacker'] = 'n/a'
        return progress

    def visit (self, objID, result):
        logger.debug('[%s] Visiting with result %r' % (objID, result))
        object_class = result.get('object_class', 'unknown')
        upload_date = result.get('uploadDate', 'unknown')
        if object_class in ['binary.pe32', 'binary.unpacked', "unhandled file type", 'unknown']:
            progress = self.default_status(object_class)
            children = result.get('children', [])
            for child in children:
                service_name = str(child['service_name'])
                progress[service_name]=child['status']
            logger.debug("%s,%r"%(objID,repr(progress)))
            self.write_progress(",".join( [objID, object_class, upload_date]+  [progress[x] for x in self.service_list]))
            #return progress
