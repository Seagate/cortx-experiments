# /usr/bin/python3

import argparse
import sys
# from cortx.utils.conf_store import Conf
# from cortx.utils.process import SimpleProcess
# NOTE: used pyyaml and subprocess since cortx-utils is
#       not installed on the container.
import yaml
import subprocess
import shutil
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


# Section start: Functions for setup using Logrotate.
def setup_logrotate_job(local):
    rotate_conf_file = \
        "/opt/cortx/component/logrotate/config/log_rollover.conf"
    component_logpath = "component"
    log_path = os.path.join(local, component_logpath)
    update_log_dir(rotate_conf_file, log_path)
    shutil.move(rotate_conf_file, "/etc/logrotate.d/")
    shutil.move("/etc/cron.daily/logrotate", "/etc/cron.hourly/")


def update_log_dir(rotate_config, log_path):
    lines = []
    with open(rotate_config, "r") as f:
        lines = f.readlines()
        if "<COMPONENT_LOG_PATH>" in lines[0]:
            lines[0] = lines[0].replace("<COMPONENT_LOG_PATH>", log_path)
    with open(rotate_config, "w") as f:
        f.truncate()
        f.writelines(lines)
# Section end.


# Section start: Functions for setup using cron job.
def run_command(command):
    """Run the command and get the response and error returned."""
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
    # NOTE: using run_command since cortx-utils is
    #       not installed on the container.
    _, err = run_command("crontab /etc/cron.d/cron_entries")
    if err:
        sys.stderr.write(err)
        exit(1)
# Section end.


def usage():
    """Print usage instructions."""
    sys.stderr.write(
        "usage:  python3 startup.py --config <url> --method <method>\n"
        "where:\n"
        "url   Config URL\n"
        "method   Log Rotation method, `cronjob` or `logrotate`\n")


if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument(
        '-c', '--config',
        help="Config url to read configurations values."
    )
    argParser.add_argument(
        '-m', '--method',
        help="Method of logrotation, `cronjob` or `logrotate`."
    )
    args = argParser.parse_args()
    if not args.config or not args.method:
        usage()
        exit(1)
    local = get_local(args.config)
    if args.method == "logrotate":
        setup_logrotate_job(local)
    elif args.method == "cronjob":
        setup_cron_job(local)
    else:
        usage()
        exit(1)
