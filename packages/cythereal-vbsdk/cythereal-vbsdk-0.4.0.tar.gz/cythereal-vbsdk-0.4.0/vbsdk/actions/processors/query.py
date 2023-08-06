import os
import sys
import traceback
import logging

from vbsdk import virusbattle
from vbsdk.vbBase import Retrieve, vbSuccess

logger=logging.getLogger('vbsdk.py')
import requests

# get the correct exception name, it is different based on version of 'requests'
global requests_exceptions_timeout
try:
    requests_exceptions_timeout = requests.exceptions.ReadTimeout
except:
    requests_exceptions_timeout = requests.exceptions.Timeout


class QueryProcessor (object):
    def __init__ (self, visitor, options):
        self.options = options
        self.visitor = visitor
        self.retriever = Retrieve(options)

    def filterServices(self,answer):
        # visit all the children, and keep only the services needed
        answer['children']=[c for c in answer.get('children',[]) if not c['service_name'] in virusbattle.serviceFilterList]

    def main(self, objID):
        if objID is None or objID == '':
            return
        if not self.visitor.okToProcess (objID):
            logging.info("[%s] Skipping processing" % objID)
            return
        logging.debug("[%r] QueryProcessor.main" % objID)
        response = self.retriever.info(objID)
        try:
            processing_stack = [objID]
            if not vbSuccess(response):
                logging.error("[%s] Query failed: %s" % (objID, response['message']))
            else:
                logging.debug("[%s] Response is %s" % (objID, repr(response)))
                answer = response['answer']
                #filter out experimental services' responses...
                self.filterServices(answer)
                self.visitor.visit (objID, answer)
                if self.options.recursive:
                    children = answer.get('children',[])
                    for c in children:
                        if (c.get('status',"failure")=='success'):
                            childID = c.get("child", "")
                            logging.debug("[%s] Visiting child %r" % (objID,childID))
                            processing_stack = [objID, childID]
                            self.main(childID)
                        else:
                            logging.info("[%s] service %s reported failure. Service_Data: %s"%(objID,c['service_name'],repr(c['service_data'])))
        except virusbattle.VBVersionError as e:
            print repr(e)
            pass
        except requests_exceptions_timeout as e:
            logging.error("[%s] QUERY TIMED OUT, processing %s" % (objID, "->".join(processing_stack)))
        except Exception as e:
            logging.error("[%s] Query failed: processing  %s" % (objID, "->".join(processing_stack)))
            exc_type, value, exc_traceback =sys.exc_info()
            tb= repr(traceback.extract_tb(exc_traceback))
            logger.error('Error type: %s\nError Value: %s\nTraceback:%s'%(str(exc_type),str(repr(value)),str(tb)))
