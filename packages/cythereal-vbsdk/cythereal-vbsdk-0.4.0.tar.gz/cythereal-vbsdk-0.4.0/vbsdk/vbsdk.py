#! /usr/bin/env python

import os
import sys
import traceback
import json
import logging
import re
import progress
import actions
import vbBase

logger = logging.getLogger(__name__)

def getMyUploads (options):
    results = vbBase.Retrieve(options).myuploads()
    results = json.loads(results.text)
    if results['status'] == "success":
        results = results['answer']
    else:
        results = []
    vbBase.ensure_dir(options.outdir)
    uploadfile = os.path.join(options.outdir, "uploads.txt")
    uploadfile = vbBase.makeNewFile (uploadfile)
    with open(uploadfile, "w") as fp:
        for r in results:
            fp.write("%s\n"% r['_id'])

    print "Output is in file: %s" % uploadfile

action_list="upload,reprocess,query,query2file,download,map,status,show,search,matches,myuploads,query+download".split(",")
actions_that_write_to_outdir="query2file,download,map,matches,myuploads,query+download".split(",")
default_action=None
default_outdir="./Results"
validArgs    = "force,password,verbose".split(",")
default_listfile = "UploadedHashes.txt"
default_poolsize=0 #upload queue size 0 = no-wait
default_search_level=3

loglevels = {"info": logging.INFO, "debug": logging.DEBUG, "warn": logging.WARN, "error": logging.ERROR}

default_loglevel = "warn"
default_uploadfile = None

def main(args=None):
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option ("-f", "--force", dest="force", default=False, action="store_true",
               help="Force resubmission, if the file already exists")
    parser.add_option ("-p", "--password", dest="password", default=None,
               help="Password for Zip and 7z encrypted archives")
    parser.add_option ("-a", "--action", dest="action", default=default_action,
               help="Action to perform. One of %s. Default is: %r" % (", ".join(action_list), default_action))
    parser.add_option ("-l", "--limit", dest="limit", default=None,
               help="limit similarity search results to semantically equilvalent (High) or similar procedures (Low) only.")
    parser.add_option ("--myUploadsOnly", dest="myUploads", default=False, action="store_true", help="Use this option to limit procedure search space to your uploads only.")
    parser.add_option ("-o", "--outdir", dest="outdir", default=default_outdir,
               help="Directory to save downloaded files. Default is: %s" % (default_outdir))
    parser.add_option("--norecursive",
                      action="store_false", dest="recursive", default=True,
                      help="Do not recursively visit children.")
    parser.add_option("--fullmatrix",
                      action="store_false", dest="upperhalf", default=True,
                      help="Get full matrix search; default upperhalf only")
    parser.add_option("--searchLevel",
                      dest="searchLevel", default=default_search_level,
                      help="Specify similarity search level between 1 and 5. Higher level-->Higher Cost and Deeper search. Default is :%d" %(default_search_level))
    parser.add_option("--filterbin",
                      action="store_true", dest="filterbin", default=False,
                      help="In search level 3 through 5, filter binaries from search that are unlikely to match. Speeds up the search")
    parser.add_option("--threshold",
                      dest="threshold", default=None,
                      help="Threshold for similarity matching")
    parser.add_option("--similarity_cache_threshold",
                      dest="similarity_cache_threshold", default=None,
                      help="Threshold similartiy for caching matches when using -a matches for bulk searching")
    parser.add_option("--use_matches_cache",
                      action="store_true",
                      dest="use_matches_cache", default=False,
                      help="Cache matches found for one sha1, and use those as answers for other sha1s, but only if the match is about --match_cache_threshold")
    parser.add_option("--xl", "--noLibrary",
                      action="store_true", dest="nolibproc", default=False,
                      help="eXclude Library functions from juice and similarity responses")
    parser.add_option("--skip", dest="skip_count", default="0",
                      help="Number of hashes to skip for any process that works on hashes, default=0")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="Verbose output")
    parser.add_option("--test",
                      action="store_true", dest="test", default=False,
                      help="Do a test run, don't actually upload")
    parser.add_option("--uploadfile", dest="uploadfile", default=default_uploadfile,
              help="List of filess and directories to upload. Default is: %s" % default_uploadfile)
    parser.add_option("--lf", "--list-file", dest="listfile", default=default_listfile,
              help="File to keep list of filehashes that are uploaded. Default is: %s" % default_listfile)
    parser.add_option("--loglevel", dest="loglevel", default=default_loglevel,
                      help="Select log level. One of: %s. Default is: %s" % (", ".join(loglevels.keys()), default_loglevel))
    parser.add_option("--downloadall", dest="downloadall", default=False, action="store_true",
                      help="Download all files. By default only unpacked files are downloaded")
    parser.add_option("--zipbinary", dest="zipBinaryFiles", default=False, action="store_true",
                      help="Download binary files as zip. Default as .exe file")
    parser.add_option("--enable_malware_download", dest="disable_malware_download",default=True, action="store_false",
                      help="Download Malware files. Malware download is disabled by default.")


    (options, args) = parser.parse_args()

    # setup log output level
    if options.verbose:
        options.loglevel = "debug"
    if not options.loglevel in loglevels.keys():
        print "ERROR - in correct log level %s, use -h to get help" % options.loglevel
        sys.exit (101)
    logging.basicConfig(format='%(asctime)s %(message)s', level=loglevels[options.loglevel])
    logger=logging.getLogger(__name__)

    options.skip_count = int(options.skip_count)
    # ensure there is something asked to do

    if options.action is None:
        print >>sys.stderr, "Please select an action to perform. The choices are: %s" % ", ".join(action_list)
        print >>sys.stderr, " Use --help for details."
        sys.exit(102)

    if not options.action in action_list:
        print  >>sys.stderr, "ERROR - Unknown action %s,  use -h to get help" % options.action
        sys.exit (103)

    if len(args) == 0 and options.action == "upload" and options.uploadfile is not None:
        # for upload command, this will read filenames from the upload file
        if not os.path.exists(options.uploadfile):
            print  >>sys.stderr, "ERROR - File %s does not exist" % options.uploadfile
            sys.exit (201)
        else:
            args = vbBase.readHashes (options.uploadfile, skip_count=options.skip_count)
            if len(args) == 0:
                print >> sys.stderr, "WARNING: Upload file list in %s is empty" % options.uploadfile
                sys.exit (202)

    elif len(args) == 0 and not options.action in ["upload", "myuploads"] and options.listfile is not None:
        # for other commands, not upload. this will read hashes from the file
        if not os.path.exists(options.listfile):
            print  >>sys.stderr, "ERROR - No arguments provided and listfile %s does not exist" % options.listfile
            sys.exit (301)
        else:
            args = vbBase.readHashes (options.listfile, skip_count = options.skip_count)
            if len (args) == 0:
                print >> sys.stderr, "WARNING: List file in %s is empty" % options.listfile
                sys.exit (302)
    if len(args) == 0 and options.action not in ["myuploads"]:
        print >> sys.stderr, "No arguments provided and list file '%s' is empty.\nPlease see help using --help." % options.listfile
        sys.exit(401)

    if options.action in actions_that_write_to_outdir:
        vbBase.ensure_dir(options.outdir)

    # by default, do not show progress
    # it may be set to 1 for expected long running tasks
    # .... be careful though, those tasks should not output to the stdout
    # .... since the progress monitor also writes to the stdout
    progress_verbosity = 0
    progress_increment = 1
    # perform work based on -a (action) requested
    if options.action == "upload":
        # upload binary for processing
        visitor = vbBase.SubmitJob(options)
        processor = actions.processors.SubmitProcessor(visitor, options)
    elif options.action == "query":
        # query results for a binary
        visitor = actions.visitors.QueryVisitor (options)
        processor = actions.processors.QueryProcessor (visitor, options)
    elif options.action == "query2file":
        # query results for a binary
        visitor = actions.visitors.Query2FileVisitor (options)
        processor = actions.processors.QueryProcessor (visitor, options)
        progress_verbosity = 1
    elif options.action == "download":
        # download unpacked binary, binary, or juice
        visitor = actions.visitors.DownloadVisitor (options)
        processor = actions.processors.QueryProcessor (visitor, options)
    elif options.action == "query+download":
        query_visitor = actions.visitors.Query2FileVisitor (options)
        download_visitor = actions.visitors.DownloadVisitor (options)
        visitor = vbBase.VBMultipleVisitors ()
        visitor.attach (query_visitor)
        visitor.attach (download_visitor)
        processor = actions.processors.QueryProcessor (visitor, options)
        progress_verbosity = 1
        progress_increment = 10
    elif options.action == "reprocess":
        # perform analysis of a binary again (without uploading)
        visitor = actions.visitors.ReprocessVisitor (options)
        # Do not recurse, for re-processing is automatically recursive
        options.recursive = False
        processor = actions.processors.QueryProcessor (visitor, options)
    elif options.action == "map":
        # query mappings for a binary
        visitor = actions.visitors.MapVisitor (options)
        processor = actions.processors.QueryProcessor (visitor, options)
    elif options.action == "status":
        # check status for a binary
        visitor = actions.visitors.ProgressMonitorVisitor (options)
        processor = actions.processors.QueryProcessor (visitor, options)
    elif options.action in ["show", "search"]:
        # show juice results for a binary or procedure
        visitor = actions.visitors.QueryVisitor (options)
        processor = actions.processors.SimQueryProcessor (visitor, options)
    elif options.action == "matches":
        # search for related binaries for a binary or related procedures for a procedure
        visitor = actions.visitors.MatchVisitor (options)
        processor = actions.processors.QueryProcessor (visitor, options)
        progress_verbosity = 1
    elif options.action == "myuploads":
        getMyUploads(options)
        sys.exit(1)
    else:
        print "Invalid action %s, nothing to do" % options.action
        sys.exit (1)

    if visitor is not None:
        progress_monitor = progress.ProgressMonitor(verbosity=progress_verbosity)
        progress_monitor.start_next_stage(options.action)
        progress_monitor.track_task(len(args), options.action, increment=progress_increment)
        visitor.open()
        for arg in args:
            try:
                processor.main (arg)
            except KeyboardInterrupt:
                from datetime import datetime
                print str(datetime.now()), "Interrupted, skipping"
                sys.stdout.flush()
            progress_monitor.bump_task()
        visitor.close()
        progress_monitor.done_task()
        progress_monitor.done("Completed")

    sys.exit(0)


if __name__ == "__main__":
    main()
