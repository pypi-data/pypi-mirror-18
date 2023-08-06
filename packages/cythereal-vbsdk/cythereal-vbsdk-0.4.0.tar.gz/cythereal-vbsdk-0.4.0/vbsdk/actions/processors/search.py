import os
import sys
import traceback
import logging
from vbsdk import virusbattle
from vbsdk.vbBase import Retrieve, vbSuccess

logger=logging.getLogger('vbsdk.py')

class SimQueryProcessor (object):
    def __init__ (self, visitor, options):
        self.options = options
        self.visitor = visitor
        self.retriever = Retrieve(options)

    def filter(self, answer):
        if self.options.limit=='High':
                        #keep semantically equivalent procedures only
            answer.pop('similar_procedures',None)
        elif self.options.limit=='Low':
                        #keep semantically similar procedures only
            answer.pop('semantically_equivalent_procedures',None)
        pass

    def main(self, objID):
        if objID is None:
            return
        if self.options.action == "show":
            # show juice results for a binary or procedure
            response =self.retriever.juice(objID)
        elif self.options.action == "search":
            # if objID is for proc, go about the business
            if not objID.find('/') == -1:
                #for procedure search
                response = self.retriever.simInfo(objID)
                answer = response.get('answer',dict())
                # clean up the answer
                remove_key = []
                for rec in answer:
                    if len(answer[rec]) == 0:
                        remove_key.append(rec)
                for key in remove_key: answer.pop(key)
                if self.options.limit is not None:
                    #filter out responses...
                    self.filter(answer)
                #filtered
                if len(answer.keys()) ==0:
                    # for this procedure, it has no match at all
                    # skip visitor.visit
                    return
                answer['proc_id'] = objID
                response['answer'] = answer
            else:
                # get the juice, get procs from juice
                response = self.retriever.juice(objID)
                rva_list = response.get('answer',dict()).keys()

                for i,rva in enumerate(rva_list):
                    # ignore uninteresting procedures
                    # ignore procedures with null gen_semantics
                    genSemantics = response['answer'][rva]['gen_semantics']
                    count_genSemantics = sum(map(len, genSemantics))
                    if count_genSemantics < 10:
                        logger.debug("skipping uninteresting procedure at rva: %s" %(rva))
                        continue

                    procID = objID + "/" + rva
                    self.main(procID)
                return
        try:
            if not vbSuccess(response):
                logger.error("[%s] Request failed: %s" % (objID, response['message']))
            else:
                logger.debug("[%s] Response is %s" % (objID, repr(response)))
                answer = response['answer']
                self.visitor.visit (objID, answer)
        except virusbattle.VBVersionError as e:
            print repr(e)
            pass
        except Exception as e:
            logger.error("[%s] Query failed: server response : %s" % (objID, str(response)))
            exc_type, value, exc_traceback =sys.exc_info()
            tb= repr(traceback.extract_tb(exc_traceback))
            logger.error('Error type: %s\nError Value: %s\nTraceback:%s'%(str(exc_type),str(repr(value)),str(tb)))
