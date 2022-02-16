#!/usr/bin/python3 -u

############################################################
#
# Note: This is a work in progress.
#
############################################################

import argparse
import requests
import os
from pprint import pprint

import jira_common


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-j', '--jira-issue', required=True)
    parser.add_argument('-r', '--jenkins-result', required=True)
    args = parser.parse_args()

    url = f"https://jts.seagate.com/rest/api/2/issue/{args.jira_issue}/attachments"
    print(url)

    auth = jira_common.userauth()
    headers = {
       "X-Atlassian-Token": "nocheck"
    }

    zipfile = args.jenkins_result + '.zip'
    zipfile_base = os.path.basename(zipfile)
    ziptarget = os.path.basename(args.jenkins_result)
    zip_working_dir = os.path.dirname(zipfile)
    print(f"Zipping result into {zipfile}:")
    cmd = f'cd {zip_working_dir}; zip -r {zipfile_base} {ziptarget}'
    print(cmd)
    os.system(f'cd {zip_working_dir}; zip -r {zipfile} {args.jenkins_result}')

    print(f"Posting file {zipfile} to {url}")
    r = requests.post(url, auth=auth, headers=headers, files={'file': open(zipfile, 'rb')})
    data = r.json()
    pprint(data)
    attachment_url = data[0]['content']

    os.unlink(zipfile)


    #
    # Upload test comment
    #
    # TODO: remove this hardcoded file, replace with args.jenkins_Result
    filesummary = "/tmp/setup-cortx-cluster-solution-input_357/summary.txt"
    headers = {"Content-Type": "application/json"}

    # For the content of the summary file, I want to print the first three
    # lines as plain text, and the remaining lines as a code block.

    file_content = open(filesummary).read()
    file1, file2 = file_content.split('\n\n')

    content = '*Code tested*\n\n'
    content += file1 + '\n'
    content += '{code}\n'
    content += file2 + '\n'
    content += '{code}\n'
    content += f'\n[See attached logs|{attachment_url}]\n'

    print("content ---------------------------------")
    print(content)
    print("------------------------------------------")

    data = {
             "update": {
               "comment": [
                 {
                   "add": {
                     "body": content
                   }
                 }
               ]
             }
           }

    url = f"https://jts.seagate.com/rest/api/2/issue/{args.jira_issue}"
    r = requests.put(url, auth=auth, headers=headers, json=data)
    print(r.status_code)

