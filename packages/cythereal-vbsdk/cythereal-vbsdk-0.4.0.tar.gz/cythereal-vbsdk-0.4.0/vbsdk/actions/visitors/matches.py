import os
import sys
import traceback
import json
import logging
import re
import ast


from vbsdk.vbBase import VBVisitor,Retrieve, ensure_dir, makeNewFile
import pprint
pp = pprint.PrettyPrinter(indent=4)

def mypp(x):
    return  pp.pformat(x).replace("u'", "'").replace("'", '"')

def mypp(x):
    return json.dumps(x, indent=4, sort_keys=True)

logger=logging.getLogger('vbsdk.py')

class MatchVisitor (VBVisitor):
    def __init__ (self, options):
        self.options = options
        ensure_dir(self.options.outdir)
        self.csv_filename = makeNewFile(os.path.join(options.outdir, "similarity" + ".csv"))
        self.json_filename = makeNewFile(os.path.join(options.outdir, "similarity" + ".json"))
        self.public_json_filename = makeNewFile(os.path.join(options.outdir, "similarity_public" + ".json"))
        self.visited = {}
        self.use_matches_cache = True if options.use_matches_cache else False
        self.matches_cache = {}
        self.similarity_cache_threshold = 0.999999999999999
        if options.similarity_cache_threshold is not None:
            self.similarity_cache_threshold = ast.literal_eval(options.similarity_cache_threshold)

    def json_write(self, x):
        if type(x) == dict:
            s = mypp(x)
            self.json_fp.write(s)
            x.pop('zzdebug_info', None)
            s = mypp(x)
            self.public_fp.write(s)
        else:
            self.json_fp.write(x)
            self.public_fp.write(x)

    def open (self):
        self.csv_fp = open(self.csv_filename,"w")
        self.json_fp = open(self.json_filename,"w")
        self.public_fp = open(self.public_json_filename,"w")
        self.csv_fp.write("binary1,binary2,similarity\n")
        self.json_write("[\n")
        self.counter = 0
        #self.json_sep = "# %d\n" % self.counter
        self.json_sep = "\n"
    def write(self, match):
        queryID = match['queryID']
        for m in match.get('matches',[]):
            try:
                match_id = m['fileHash']
            except:
                match_id = m['_id']
            self.csv_fp.write("%s,%s,%s\n" %(queryID, match_id, m['similarity']))
        if 'same_as' in match:
            self.csv_fp.write("%s,%s,%s\n" %(queryID, 'same_as', match['same_as']))

        self.json_write(self.json_sep)
        match['_id'] = match.pop('queryID', None)
        self.json_write(match)
        self.counter +=1
        #self.json_sep = ",\n# %d\n" % self.counter
        self.json_sep = ",\n"

    def close (self):
        self.json_write("\n]")
        self.csv_fp.close()
        self.json_fp.close()

    def getMatches_cached (self, objID):
        if objID in self.matches_cache:
            return self.matches_cache[objID]
        # get results,
        results = self.getMatches_uncached (objID)
        # and cache the high similarity data
        for m in results.get('matches', []):
            other_obj = m['fileHash']
            similarity = m['similarity']
            if similarity >= self.similarity_cache_threshold:
                self.matches_cache[other_obj] = {'queryID': other_obj, 'same_as': objID, 'message': 'Using cached data'}
        return results

    def getMatches_uncached (self,objID):
        try:
            results = Retrieve(self.options).matches(objID)
            results = json.loads(results.text)
        except:
            # a placeholder, in case we want to catch ^C interrupt here
            raise
        else:
            if results['status'] == "success":
                results = results['answer']
                results['queryID'] = objID
                for m in results['matches']:
                    m.pop('_id', None)
            else:
                # create a dummy result, so rest of the processing takes place
                results = {'queryID':objID, 'matches':[], 'message':"No match found"}
        return results

    def visit (self, objID, result):
        # ignore dot and json files
        object_class = result.get('object_class', 'unknown')
        if re.match(r'(dot|json).*', object_class): return
        # and don't visit the sha again
        if self.visited.get(objID, False):  return

        if re.match(r'binary.*', object_class):
            if self.use_matches_cache:
                matches = self.getMatches_cached(objID)
            else:
                matches = self.getMatches_uncached(objID)
        else:
            # must be archive
            matches = {'queryID': objID}
            matches['children'] = []
            for child in result['children']:
                if child.get('status', 'fail') == 'success':
                    matches['children'].append(child['child'])

        matches['object_class'] = object_class
        parents = result.get('parents',[])
        if len(parents) > 0:
            matches['parents'] = parents

        # transfer certain fields if they exist
        for f in ['origFilepath', 'uploadDate', 'length']:
            if f in result:
                matches[f] = result[f]

        self.write(matches)
        self.visited[objID] = 1

    def __enter__ (self):
        self.open()
        return self
    def __exit__(self, type, value, tracebackObj):
        self.close()
        if value:
            #log error
            exc_type, value, exc_traceback =sys.exc_info()
            tb= repr(traceback.extract_tb(exc_traceback))
            logger.error('Error type: %s\nError Value: %s\nTraceback:%s'%(str(exc_type),str(repr(value)),str(tb)))

