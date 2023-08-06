import os
import sys
import traceback
import logging
from vbsdk.vbBase import VBVisitor,Retrieve,is_malware_class,is_original_class, objectClassFileType, ensure_dir

logger=logging.getLogger('vbsdk.py')

def filePatternExists (filepattern):
    """
    CAUTION: This is unsafe. It should be used with care. It runs a shell script with filepattern as argument/
    CAUTION: This is also Linux specific.
    filepattern: a string with regular expression, expected to be a path in the file system.
    The function returns true, if there is some file matching the pattern, and false otherwise
    """
    status = os.system("ls %s 2>1 > /dev/null" % filepattern)
    # status = 0, if pattern matches any file
    # status = 512, otherwise
    return status == 0

class DownloadVisitor (VBVisitor):
    def __init__ (self, options):
        self.retriever = Retrieve (options)
        self.options = options
        self.outdir = options.outdir
        ensure_dir (self.outdir)

    def okToProcess (self, objID):
        # check if the file already exists (and so has been downloaded)
        # do not process if in such case
        filepattern = os.path.join(self.outdir, objID+'*')
        if filePatternExists(filepattern):
            logger.info("[%s] file exists %s, skipping" % (objID, filepattern))
            return False
        return True
    def visit (self, objID, result):
        object_class = result.get("object_class", None)
        logger.info("[%s] downloading %s" % (objID, str(object_class)))

        if self.options.disable_malware_download and is_malware_class (str(object_class)):
            # do not download files that may contain malware, unless explicitly asked
            logger.debug("[%s] --enable_malware_download is not set. Ignoring download, object of class %s may contain malware." % (objID, str(object_class)))
            return

        if (not self.options.downloadall) and is_original_class (str(object_class)) :
            # do not download original files, unless explicitly asked
            logger.debug("[%s] --downloadall is not set. Ignoring download. It's of class %s. Binary" % (objID, str(object_class)))
            return

        filename = os.path.join(self.outdir, objID)
        filext = None
        if not object_class is None:
            # get file ext for the class. If there is none use the class itself as an extension
            filext = objectClassFileType.get(object_class, None)
            if (self.options.zipBinaryFiles) and ('binary' in object_class):
                filext='zip'
        if filext is not None:
            filename = filename + "." + filext

        logger.info ("[%s] Downloading to %s" % (objID, filename))
        with open(filename, "w") as ofp:
            ifp = self.retriever.file(objID)
            for chunk in ifp.__iter__():
                ofp.write (chunk)

