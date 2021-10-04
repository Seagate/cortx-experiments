# /usr/bin/python3

import argparse
import sys
# from cortx.utils.conf_store import Conf
# from cortx.utils.process import SimpleProcess
# NOTE: used pyyaml and subprocess since cortx-utils is
#       not installed on the container.
import yaml
import subprocess
import os


def get_local(config_url):
    # Conf.load('Config', config_url)
    # return Conf.get('Config', 'cortx>common>storage>log')

    # NOTE: using pyyaml since cortx-utils is not installed on the container.
    log_dir = None
    with open(config_url) as f:
        conf = yaml.load(f, Loader=yaml.loader.SafeLoader)
        log_dir = (conf["cortx"]["common"]["storage"]["log"])
    return log_dir


def run_command(command):
    """Run the command and get the response and error returned"""
    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    response, error = process.communicate()
    return response.decode().rstrip('\n'), error.decode().rstrip('\n')


def setup_cron_job(local):
    cron_shedule = "* * * * *"  # every minute
    rollover_script_cmd = \
        "/usr/bin/python3 /opt/cortx/component/logrotate/cron/log_rollover.py"
    log_dir = os.path.join(local, "component")
    with open("/etc/cron.d/cron_entries", 'a') as f:
        f.write(f"{cron_shedule} {rollover_script_cmd} --logpath {log_dir}\n")
    # _, err, retcode = SimpleProcess("crontab /etc/cron.d/cron_entries").run()
    # NOTE: using run_command since cortx-utils is not installed on the container.
    _, err = run_command("crontab /etc/cron.d/cron_entries")
    if err:
        sys.stderr.write(err)
        exit(1)


def usage():
    """ Print usage instructions """
    sys.stderr.write(
        "usage:  python3 startup.py --config <url>\n"
        "where:\n"
        "url   Config URL\n")


if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument(
        '-c', '--config',
        help="Config url to read configurations values."
    )
    args = argParser.parse_args()
    if not args.config:
        usage()
        exit(1)
    local = get_local(args.config)
    setup_cron_job(local)
