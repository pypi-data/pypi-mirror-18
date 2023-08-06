import os
import sys
import traceback
from vbsdk import virusbattle
import json
import requests
import logging
logger=logging.getLogger('vbsdk.py')

class VBVisitor (object):
    def open (self):
        pass
    def close (self):
        pass
    def visit (self, objID, result):
        #override this function to do the task!
        pass
    def okToProcess (self, objID):
        return True
    def __enter__(self):
        return self
    def __exit__(self,type,value,tracebackObj):
        if value:
            #log error
            exc_type, value, exc_traceback =sys.exc_info()
            tb= repr(traceback.extract_tb(exc_traceback))
            logger.error('Error type: %s\nError Value: %s\nTraceback:%s'%(str(exc_type),str(repr(value)),str(tb)))



class VBMultipleVisitors (VBVisitor):
    def __init__ (self):
        self.visitors = []

    def attach (self, visitor):
        self.visitors.append (visitor)

    def open (self):
        for x in self.visitors:
            x.open ()

    def close (self):
        for x in self.visitors:
            x.close ()

    def visit (self, objID, result):
        for x in self.visitors:
            x.visit (objID, result)

    def okToProcess (self, objID):
        res = True
        for x in self.visitors:
            res = res and x.okToProcess (objID)
        return res


class SubmitJob (object):
    def __init__ (self, options):
        self.options = options
        if  not options.force:
            logger.debug("The switch -f (--force) was not used, a file will be processed only if its not already in the database")
        # open file to save the filehashes uploaded
        self.listfp = open(options.listfile, "a")
    def open(self):
        pass

    def close(self):
        pass

    def uploadFile (self, filepath):
        filename=os.path.basename(filepath)
        url =  virusbattle.make_vburl("upload")
        logger.info("[%s] Uploading file %s" % (filename,filepath))
        try:
            myFile = {'filedata': open(filepath, 'rb')}
            params={}
            # whether or not to force re-analysis, if already in the system
            # Use force carefully, and only if really necessary
            if self.options.force: params['force']='1'
            params['origFilepath'] = filepath
            # Password for decrypting zip file
            if self.options.password is not None:
                params['password'] = self.options.password
            try:
                params['unpackerConfig']=os.environ['VIRUSBATTLE_UNPACKER_CONFIG']#for customized configurations
            except:
                pass # use default config
            logger.debug('[%s] URL %s' %(filename, url))
            results = requests.post(url, files=myFile, params=params)
            logger.debug("[%s] Server returned: %s"%(filename,results.content))
            result=json.loads(results.text)
            status = result.pop('status')
            filehash = result.pop('hash')
            if(status=="success"):
                logger.info("[%s] [%s] %s\n" % (filename,status, repr(result)))
                self.listfp.write(str(filehash)+"\n")
                return filehash
            else:
                logger.info("[%s] [%s] %s\n" % (filename, status, repr(result)))
        except Exception as e:
            logger.error("[Client-Error] [%s] unable to upload %s \n" % (sys.exc_info(),os.path.basename(filepath)))
            logger.error(repr(e)+"\n")
        return False

    def reprocess (self, objID):
        params = {}
        url =  virusbattle.make_vburl("reprocess", objID, **params)
        logger.debug("[%s] reprocessing using URL %s " % (objID, url))
        results = requests.get(url)
        return json.loads(results.text)
    def __enter__(self):
        return self
    def __exit__(self,type,value,tracebackObj):
        if value:
            #log error
            exc_type, value, exc_traceback =sys.exc_info()
            tb= repr(traceback.extract_tb(exc_traceback))
            logger.error('Error type: %s\nError Value: %s\nTraceback:%s'%(str(exc_type),str(repr(value)),str(tb)))

class Retrieve (object):
    def __init__ (self, options):
        self.options  = options
        self.threshold = options.threshold
    def file (self, objID):
        url = virusbattle.make_vburl("download", objID)
        logger.debug("[%s] Downloading using URL %s " % (objID, url))
        params={}
        if self.options.zipBinaryFiles:
            params['zipBinary']=1
        results = requests.get(url,params=params)
        return results
    def info (self, objID):
        url = virusbattle.make_vburl("query", objID)
        return self.getData(url, objID)

    def myuploads (self):
        url = virusbattle.make_vburl("query")
        results = requests.get(url)
        return results
    def matches (self, objID,timeout=30*60):
        params = {}
        params['upperhalf'] = self.options.upperhalf
        if self.threshold:
            params['threshold'] = self.threshold
        params['filterbin'] = self.options.filterbin
        params['level']=self.options.searchLevel
        url = virusbattle.make_vburl("search/binary", objID)
        kwargs={'params':params, 'timeout':timeout}
        results = requests.get(url, **kwargs)
        return results

    def juice (self, objID):
        #objID here is the BinaryID or ProcedureID
        #ProcedureID is of the form BinaryID/0x<rva>
        url=''
        params=dict()
        if self.options.nolibproc:
            params['noLibProc']=True
        if objID.find('/') == -1:
            #binaryID
            url = virusbattle.make_vburl("show/binary", objID)
        else:
            #procID
            url = virusbattle.make_vburl("show/proc",objID)
        return self.getData(url, objID,params)

    def simInfo (self, objID):
        #objID here is the BinaryID or ProcedureID
        #ProcedureID is of the form BinaryID/0x<rva>
        url=''
        params=dict()
        if self.options.nolibproc:
            params['noLibProc']=True
        if objID.find('/') == -1:
            #binaryID
            url = virusbattle.make_vburl("search/procs",objID)
        else:
            #procID
            params['searchType']=3
            params['myUploads']=self.options.myUploads
            if self.options.limit=='High':
                params['searchType']=1
            elif self.options.limit=='Low':
                params['searchType']=2
            url = virusbattle.make_vburl("search/procs",objID)
        return self.getData(url, objID,params)

    def getData (self, url, objID,params=None):
        try:
            logger.debug("[%s] Querying info using URL %s " % (objID, url))
            results = requests.get(url,params=params)
            logger.debug("[%s] Server returned: %s"%(objID,results.content))
            results = json.loads(results.text)
            return virusbattle.check_version(results)
        except virusbattle.VBVersionError as e:
            print repr(e)
            sys.exit (1)
        except Exception as e:
            logger.exception("[Client-Error] [%s] unable to retrieve %s \n" % (sys.exc_info(),objID))
            return ''

    def __enter__(self):
        return self
    def __exit__(self,type,value,tracebackObj):
        if value:
            #log error
            exc_type, value, exc_traceback =sys.exc_info()
            tb= repr(traceback.extract_tb(exc_traceback))
            logger.error('Error type: %s\nError Value: %s\nTraceback:%s'%(str(exc_type),str(repr(value)),str(tb)))

def vbSuccess (response):
    return response is not None and response.get('status', None) == 'success'
def vbFailure (response):
    assert('status' in response)
    return response['status'] == 'failed'
def vbError (response):
    return response is None or response.get('status', 'error') == 'error'
