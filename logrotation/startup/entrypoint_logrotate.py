# /usr/bin/python3

import argparse
import sys
from cortx.utils.conf_store import Conf
from cortx.utils.process import SimpleProcess
import shutil
import os

sys.path.append('/opt/cortx/component/test')
from logger import start_logging


def setup_logrotate_job(local):
    """Configure & move logrotate config file to appropriate location."""
    rotate_conf_file = \
        "/opt/cortx/component/logrotate/log_rollover.conf"
    component_logpath = "component"
    log_path = os.path.join(local, component_logpath)
    update_log_dir(rotate_conf_file, log_path)
    shutil.move(rotate_conf_file, "/etc/logrotate.d/")
    shutil.move("/etc/cron.daily/logrotate", "/etc/cron.hourly/")


def update_log_dir(rotate_config, log_path):
    """Replce the template log path with log_path passed as arg."""
    lines = []
    with open(rotate_config, "r") as f:
        lines = f.readlines()
        if "<COMPONENT_LOG_PATH>" in lines[0]:
            lines[0] = lines[0].replace("<COMPONENT_LOG_PATH>", log_path)
    with open(rotate_config, "w") as f:
        f.truncate()
        f.writelines(lines)


def start_crond_service():
    cmd = "/usr/sbin/crond start"
    _, err, retcode = SimpleProcess(cmd).run()
    if retcode != 0:
        sys.stderr.write(f"Error while starting crond service: {err}")
        exit(1)
    sys.stdout.write("Started crond service successfully.")


def usage():
    """Print the usage instructions."""
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

    # Step 0: Parse & Validate config url
    args = argParser.parse_args()
    if not args.config:
        usage()
        exit(1)

    # Step 1: get local log dir from the cofig url.
    Conf.load('Config', args.config)
    local = Conf.get('Config', 'cortx>common>storage>log')

    # Step 2: Configure log path in logratate config &
    #         move the file to /etc/logrotate.d
    setup_logrotate_job(local)

    # Step 3: Start the crond service.
    start_crond_service()

    # Step 4: Run the component logic. (using simple logger for testing)
    start_logging(local)
