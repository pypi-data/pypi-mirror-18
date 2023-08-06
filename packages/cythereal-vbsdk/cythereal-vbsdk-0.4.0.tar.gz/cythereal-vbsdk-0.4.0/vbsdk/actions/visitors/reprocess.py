import os
import sys
from vbsdk.vbBase import VBVisitor,SubmitJob

class ReprocessVisitor (VBVisitor):
    def __init__ (self, options):
        self.options = options
    def visit (self, objID, result):
        SubmitJob(self.options).reprocess(objID)
