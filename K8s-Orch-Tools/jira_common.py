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
        querystring = '&'.join([f'{k}={v}' for k,v in list(querydict.items())]) + '&'


    url = f"https://jts.seagate.com/rest/api/2/search?{querystring}jql={jql}"

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
            print(f"Exception caught: {e}.  Retrying ({retry_count}).")

    if r.status_code != 200:
        raise FailedJqlException(r.text)

    return json.loads(r.text)

def query_all(jql, querydict=None, verbose=True):
    # Take care of pagination of all queries.  Return a list of issues.

    result = []
    start_at = 0
    max_results = 100
    while True:
        if not querydict:
            querydict = {}
        querydict.update({'startAt': start_at, 'maxResults': max_results})
        qout = query(jql, querydict=querydict)
        with open("qout.debut", "w") as f:
            f.write(json.dumps(qout))

        result += qout['issues']
        if verbose:
            print("Got {len(result)} issues so far", file=sys.stderr)
        if start_at + len(qout['issues']) >= qout['total']:
            break
        start_at += len(qout['issues'])
    return result
