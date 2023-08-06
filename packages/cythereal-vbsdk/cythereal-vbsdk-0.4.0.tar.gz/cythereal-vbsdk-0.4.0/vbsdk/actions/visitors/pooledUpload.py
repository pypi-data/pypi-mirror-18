import os
import sys
import traceback
import logging
from vbsdk.vbBase import VBVisitor, SubmitJob, is_binary_class, Retrieve
import vbsdk.virusbattle
logger=logging.getLogger('vbsdk.py')

from multiprocessing import Process, Queue
import time

def upload(id,queue,options):
    while True:
        try:
            filepath=queue.get(False)
        except:
            time.sleep(1)
            logger.debug("[Pool Worker-%d] No jobs in queue..sleeping"%(id))
            continue
        #have a job..do it
        filehash=SubmitJob(options).uploadFile(filepath)
        if filehash:
            logger.info("[Pool Worker-%d] Submitted file %s"%(id,filepath))
            while not task_done(filehash,options): #wait for task to finish
                time.sleep(15)
        else:
            logger.error("[Pool Worker-%d] Unable to Submit file %s"%(id,filepath))

def task_done(filehash,options):
    #return true if processing for file with filehash is complete, else return false
    return Status(options).visit(filehash)

class PooledUploadVisitor(SubmitJob):
    def __init__(self,options):
        SubmitJob.__init__(self,options)
        self.queue = Queue()
        self.poolQuota=int(options.poolSize)
        self.upload_fn=upload
    def open(self):
        self.workers = [Process(target=self.upload_fn,args=(i,self.queue,self.options)) for i in xrange(self.poolQuota)]
        for w in self.workers:
            w.start()
    def close(self):
        if self.queue.qsize()==0:
            for w in self.workers:
                w.terminate()
        else:
            time.sleep(1)
            self.close()
    def uploadFile(self,filepath):
        #addToQueue
        self.queue.put(filepath)
    def __exit__(self,type,value,tracebackObj):
        if value:
            #log error
            exc_type, value, exc_traceback =sys.exc_info()
            tb= repr(traceback.extract_tb(exc_traceback))
            logger.error('Error type: %s\nError Value: %s\nTraceback:%s'%(str(exc_type),str(repr(value)),str(tb)))
        self.close()


class Status (VBVisitor):
    def __init__ (self, options):
        self.options = options
        self.service_list = virusbattle.service_list()
        self.retriever = Retrieve(options)
    def __exit__(self,type,value,tracebackObj):
        if value:
            #log error
            exc_type, value, exc_traceback =sys.exc_info()
            tb= repr(traceback.extract_tb(exc_traceback))
            logger.error('Error type: %s\nError Value: %s\nTraceback:%s'%(str(exc_type),str(repr(value)),str(tb)))
    def default_status (self, object_class):
        progress = {}
        for x in self.service_list: progress[x] = "Pending"
        if object_class == "binary.unpacked":
            progress['srlUnpacker'] = 'n/a'
        return progress
    def visit (self, objID):
        response=self.retriever.info(objID)
        result=response['answer']
        logger.debug('[%s] Visiting with result %r' % (objID, result))
        object_class = result.get('object_class','unavailable')
        if object_class=='unavailable':
            return False
        if is_binary_class(object_class):
            progress = self.default_status(object_class)
            children = result.get('children', [])
            for child in children:
                service_name = str(child['service_name'])
                progress[service_name]=child['status']
            logger.debug("%s,%r"%(objID,repr(progress)))
            if progress['srlUnpacker']=='Pending':
                return False
            if progress['srlJuice']=='Pending':
                return False
            if progress['srlJuice']=='failure':
                return True
            if progress['srlStatic']=='Pending':
                return False
            if progress['srlSimService']=='Pending':
                return False
            else:
                return True
        return True
