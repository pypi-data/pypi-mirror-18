import os
from collections import OrderedDict

def ensure_dir(path):
    try: 
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise

def readHashes (filename, skip_count=0):
    if os.path.exists(filename):
        with open(filename, 'r') as fp:
            # should remove duplicate hashes
            result =  list(OrderedDict.fromkeys(map(lambda x: x.strip('\n\t\r'),fp.readlines())))
            # skip hashes, if requested
            return result[skip_count:]

    return []



def makeNewFile (filepath):

    import os, re
    # file does not exist, use this name
    if not os.path.isfile(filepath):
        return filepath

    # file exists, create a new name

    dirpart, filename = os.path.split(filepath)

    def testFileName(fileNumberInt, fileBase, fileExtension):
        fileNumber = '%03d' % (fileNumberInt)
        fileName = os.path.join(dirpart, fileBase+fileNumber+fileExtension)
        if not os.path.isfile(fileName):
            return fileName
        else:
            return testFileName(fileNumberInt + 1, fileBase,  fileExtension)

    def getSplit(fileName):
        m  = re.match('([A-Za-z_-]*)([0-9]*)(.[a-z0-9]*)', fileName)
        fileBase = m.group(1)
        fileNumber = m.group(2)
        if fileNumber == "":
            fileNumber = "000"
        try:
            fileNumberInt = int(fileNumber[0])
        except:
            fileNumberInt = 1
        fileExtension = m.group(3)
        answer = fileBase, fileNumberInt, fileExtension
        return answer

    fileBase, fileNumberInt, fileExt = getSplit(filename)
    return testFileName(fileNumberInt, fileBase, fileExt)


