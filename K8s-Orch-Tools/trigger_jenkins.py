#!/usr/bin/python3 -u

########################################################
# trigger_jenkins.py
#
# This script triggers the jenkins job setup-cortx-cluster-solution-input,
# which is a simple sanity test that is useful to run prior to merging
# changes.  This job collects logs and artifacts that may be useful in
# updating your Jira issue.
#
# The job runs on your own Kubernetes cluster.  It assumes
# that it is ready for CORTX deployment, which means that
# "prereq-deploy-cortx-cloud.sh" has already been run and
# CORTX is not currently running.
#
#
#
# Usage:  trigger_jenkins.py <options>
#
#  -s <solution.yaml>  The solution.yaml file that describes your cluster.
#                    This file will be uploaded to the Jenkins job, which
#                    copies it to /var/tmp/solution.yaml on the first node
#                    listed.  This file determines which cortx-all package
#                    will be used.
#
#  -t <tag>  This is the git changeset of the seagate/cortx-k8s repo to use.
#                    This can be a tag (like v0.0.21) or a sha.
#
#  Jenkins token
#  -------------
#  Your Jenkins token must be provided to run the Jenkins job.  The Jenkins user
#  and token must be in the format <user>:<token>.  These may be specified via
#  command line as -u <user>:<token>, or through the environment variable
#  JENKINS_USER_TOKEN.
#
#  Node access
#  -----------
#  The Jenkins job accesses the nodes via ssh.  This script assumes that the
#  username and password are identical for all nodes.  You specify the password
#  via command line as -p <password>, or throught the environment variable
#  NODE_PASSWORD.
#
#  By default the username is "root", but this can be overridden via the command
#  line as "--node-user <username>".
#
#
# Script Output
# =============
# After the Job has been run, the artifacts created by the job, the
# console output, and a summary suitable for pasting into a report
# are created in ./setup-cortx-cluster-solution-input_<build-number>.
#
#
########################################################



import argparse
import datetime
import re
import os
import sys
import tempfile
import time

from yaml import load, Loader
import requests

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


JENKINS_JOB = "https://eos-jenkins.colo.seagate.com/job/Cortx-Kubernetes/job/setup-cortx-cluster-solution-input"

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--solution', dest='solution_file', required=True)
parser.add_argument('-t', '--tag', dest='cortx_k8s_tag', required=True)
parser.add_argument('--node-user', dest='node_user', default='root')
parser.add_argument('-p', '--node-password', dest='node_password')
parser.add_argument('-u', '--user-token', dest='user_token')
#Note: For --debug-skip-trigger, the arg shuld be the build url
#      For example:  "http://eos-jenkins.colo.seagate.com/job/Cortx-kubernetes/job/setup-cortx-cluster-solution-input/341/"
parser.add_argument('--debug-skip-trigger', dest='debug_skip_trigger')

args = parser.parse_args()

if not args.user_token:
    args.user_token = os.environ.get('JENKINS_USER_TOKEN')
    if not args.user_token:
        print("No Jenkins user token specified.", file=sys.stderr)
        print('  Specify with -u/--user-token or with', file=sys.stderr)
        print('  the environment variable "JENKINS_USER_TOKEN"', file=sys.stderr)
        sys.exit(1)

if not re.match('\w+:\w+', args.user_token):
    print(f"Invalid Jenkins user token specified ({args.user_token}).", file=sys.stderr)
    print("The user token should have the form \"<jenkins-username>:<jenkins-token>\".", file=sys.stderr)
    sys.exit(1)

username, password = args.user_token.split(':')

if not args.node_password:
    args.node_password = os.environ.get('NODE_PASSWORD')
    if not args.node_password:
        print('No password for cortx nodes specified.', file=sys.stderr)
        print('  Specify with -p/--node-password or with', file=sys.stderr)
        print('  the environment variable "NODE_PASSWORD"', file=sys.stderr)
        sys.exit(1)

#
# Read hostnames from solution.yaml
#
if not os.path.exists(args.solution_file):
    print("File {args.solution_file} does not exist.", file=sys.stderr)
    sys.exit(1)

solution_content = load(open(args.solution_file), Loader=Loader)
nodes = solution_content['solution']['nodes']
hosts = [f"hostname={n['name']},user={args.node_user},password={args.node_password}" for n in nodes.values()]

jenkins_build_url = JENKINS_JOB+'/buildWithParameters'

hosts0 = hosts[0]
hosts_other = '\n'.join(['                       '+h for h in hosts[1:]])
dashboard_header = f"""command = {' '.join(sys.argv)}
                user = {username}
CORTX_SCRIPTS_BRANCH = {args.cortx_k8s_tag}
 input/solution.yaml = {args.solution_file}
               hosts = {hosts[0]}
{hosts_other}"""

print("*********************************************")
print(f"Triggering Jenkins: {jenkins_build_url}")
print()
print(dashboard_header)
print("*********************************************")


if not args.debug_skip_trigger:

    r = requests.post(jenkins_build_url, auth=(username, password),
                      verify=False,
                      data={'CORTX_SCRIPTS_BRANCH': args.cortx_k8s_tag,
                            'hosts': ' '.join(hosts)},
                      files={'input/solution.yaml': open(args.solution_file, "rb")})

    queue_item_url = r.headers['Location']

    #
    # Wait for job to execute
    #


    print(f"Job triggered.  Jenkins queue item: {queue_item_url}")
    print("Waiting for job to start.")

    queue_item_url += 'api/json'
    while True:
        r = requests.get(queue_item_url, verify=False)
        if r.status_code == 200:
            build_data = r.json()
            if 'executable' in build_data:
                break
        time.sleep(1)


    build_url = build_data['executable']['url']
else:
    build_url = args.debug_skip_trigger

build_url = build_url.replace('http:', 'https:')

r = requests.get(build_url+'/api/json', verify=False)

print("\n\nJob started.  Waiting for job to complete")
print(f"Jenkins url: {build_url}\n")


jobstarted = datetime.datetime.now()
job_started_str = jobstarted.strftime("%Y-%m-%d/%H:%M:%S")
datetimer = 0
dateprinttime = 60  #every minute
while True:
    nowtime = time.time()
    now = datetime.datetime.now()
    if nowtime - datetimer > dateprinttime:
        now_str = datetime.datetime.now().strftime("%Y-%m-%d/%H:%M:%S")
        elapsed = (now - jobstarted).seconds
        elapsed_str = f"{elapsed//60}m {elapsed%60}s"
        print(f"Job running:   started: {job_started_str}    now: {now_str}     elapsed: {elapsed_str}")
        datetimer = nowtime

    r = requests.get(build_url+'/api/json', verify=False)
    if r.status_code != 200:
        print(f"Error: Could not contact Jenkins server at {build_url+'/api/json'}")
        continue


    builddata = r.json()
    result = builddata['result']
    if result:
        now_str = datetime.datetime.now().strftime("%Y-%m-%d/%H:%M:%S")
        elapsed = (now - jobstarted).seconds
        elapsed_str = f"{elapsed//60}m {elapsed%60}s"
        print(f"Job completed: started: {job_started_str}    now: {now_str}     elapsed: {elapsed_str}")
        break

    time.sleep(5)


if result == 'SUCCESS':
    print("\n\nJob Succeeded! \n\n")

else:
    print(f"\n\nJob did not pass: {result}\n\n")

#
# Download all artifacts
#
m = re.search(r'.+/([\w\-]+)/(\d+)/$', builddata['url'])
artifactdir = f"{m.group(1)}_{m.group(2)}"

if not os.path.isdir(artifactdir):
    os.mkdir(artifactdir)

for artifact in builddata['artifacts']:
    print(f"Downloading artifact: {artifactdir}/{artifact['fileName']}")
    r = requests.get(build_url+f"artifact/{artifact['relativePath']}", verify=False)
    f = open(os.path.join(artifactdir, artifact['fileName']), 'wb')
    f.write(r.content)
    f.close()

logname = 'console.log'
print(f"Downloading log: {artifactdir}/{logname}")

log_url = f"{builddata['url']}timestamps/?time=HH:mm:ss&timeZone=GMT-8&appendLog&locale=en"
r = requests.get(log_url, verify=False)
f = open(os.path.join(artifactdir, logname), 'wb')
f.write(r.content)
f.close()

summary_filename = 'summary.txt'
print(f"Writing summary: {artifactdir}/{summary_filename}")
f = open(os.path.join(artifactdir, summary_filename), 'w')
print(f"Build: {build_url}", file=f)
print(f"Completed at {time.ctime()}", file=f)
print(f"Result = {result}", file=f)
print('', file=f)
summary_hidden_pw = re.sub(r'password=[^\s]+', 'password=<hidden>', dashboard_header)
print(summary_hidden_pw, file=f)
f.close()

print("\nDone! \n")

if result == 'SUCCESS':
    sys.exit(0)
else:
    sys.exit(1)
