import os
import sys
import traceback
import json
import logging

logger=logging.getLogger('vbsdk.py')

from vbsdk import virusbattle
import requests

def avscan_retrieve (objID,**params):
    url =  virusbattle.make_vburl("other/avscans", objID, **params)
    logger.debug("[%s] retrieve avscans using URL %s " % (objID, url))
    results = requests.get(url)
    results = json.loads(results.text)
    if results['status'] == "success":
        if 'answer' in results and 'scans' in results['answer']:
            return results['answer']['scans']
    return None
