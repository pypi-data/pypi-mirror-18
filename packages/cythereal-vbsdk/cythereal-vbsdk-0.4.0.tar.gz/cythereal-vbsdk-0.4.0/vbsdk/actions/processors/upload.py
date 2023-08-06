import os
import sys
import logging
from vbsdk.vbBase import SubmitJob

logger=logging.getLogger('vbsdk.py')

class SubmitProcessor (object):
    def __init__ (self, visitor, options):
        self.visitor = visitor
        self.recursive = options.recursive
        self.test = options.test

    def main (self, path):
        #self.visitor.open()
        path = os.path.abspath(path)
        if os.path.isfile(path):
            self.submitFile(path)
        elif os.path.isdir (path):
            if self.recursive:
                self.submitDirectoryRecursive(path)
            else:
                self.submitDirectoryOneLevel(path)
        #self.visitor.close()
    def submitFile (self, filename):
        logger.debug("Visiting file: %s", filename)
        if not self.test:
            self.visitor.uploadFile (filename)

    def submitDirectoryOneLevel (self, path):
        logger.debug("Traversing directory -- ONE LEVEL: %s", path)
        files = os.listdir(path)
        # make full path
        files = map(lambda x: os.path.join(path, x), files)
        # Keep only files (not directory)
        files = filter(os.path.isfile, files)
        for filepath in files:
            self.submitFile (filepath)

    def submitDirectoryRecursive (self, path):
        logger.debug("Traversing directory Recursively: %s", path)
        for root, dirs, files in os.walk(path):
            relative_path = root # os.path.relpath(root, path)
            for filename in files:
                filepath = os.path.join(relative_path, filename)
                self.submitFile(filepath)
