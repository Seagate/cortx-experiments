#!/usr/bin/python3

import requests
import json
import sys
import os
import time


username = os.environ['JIRA_USERNAME']
password = os.environ['JIRA_PASSWORD']

IMGURL = '/static/img'


def userauth():
    return (username, password)

class FailedJqlException(Exception):
    def __init__(self, message):
        '''Helper exception'''
        super().__init__(message)


def query(jql, querydict=None):

    querystring = ''
    if querydict:
        querystring = '&'.join(['%s=%s'%(k,v) for k,v in list(querydict.items())]) + '&'


    url = "https://jts.seagate.com/rest/api/2/search?%sjql=%s" % (querystring, jql)
    #url = "https://jts.seagate.com/rest/api/2/search?%sjql=%s&expand=changelog" % (querystring, jql)

    auth = userauth()
    headers = {
       "Accept": "application/json",
       "Content-Type": "application/json",
    }

    retry_count = 0
    while True:
        try:
            print(f"{time.ctime()} GET {url}", file=sys.stderr)
            r = requests.get(url, auth=auth, headers=headers)
            break
        except Exception as e:
            retry_count += 1
            print("Exception caught: %s.  Retrying (%d)." % (str(e), retry_count))

    if r.status_code != 200:
        raise FailedJqlException(r.text)

    return json.loads(r.text)

def query_all(jql, querydict=None, verbose=True):
    # Take care of pagination of all queries.  Return a list of issues.

    result = []
    startAt = 0
    maxResults = 100
    while True:
        if not querydict:
            querydict = {}
        querydict.update({'startAt': startAt, 'maxResults': maxResults})
        qout = query(jql, querydict=querydict)
        f = open("qout.debug", "w")
        f.write(json.dumps(qout))
        f.close()

        result += qout['issues']
        if verbose:
            print("Got %d issues so far" % len(result), file=sys.stderr)
        if startAt + len(qout['issues']) >= qout['total']:
            break
        startAt += len(qout['issues'])
    return result
