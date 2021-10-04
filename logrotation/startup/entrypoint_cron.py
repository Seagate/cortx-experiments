# /usr/bin/python3

import argparse
import sys
from cortx.utils.conf_store import Conf
from cortx.utils.process import SimpleProcess
import os

sys.path.append('/opt/cortx/component/test')
from logger import start_logging


def get_local(config_url):
    """Get local log path from the config url."""
    Conf.load('Config', config_url)
    return Conf.get('Config', 'cortx>common>storage>log')


def setup_cron_job(local):
    """Add a crontab entry."""
    cron_shedule = "* * * * *"  # every minute
    rollover_script_cmd = \
        "/usr/bin/python3 /opt/cortx/component/cron/log_rollover.py"
    log_dir = os.path.join(local, "component")
    with open("/etc/cron.d/cron_entries", 'a') as f:
        f.write(f"{cron_shedule} {rollover_script_cmd} --logpath {log_dir}\n")
    _, err, retcode = SimpleProcess("crontab /etc/cron.d/cron_entries").run()
    if retcode != 0:
        sys.stderr.write(err)
        exit(1)


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
    local = get_local(args.config)

    # Setp 2: Add cron job in crontab.
    setup_cron_job(local)

    # Step 3: Start the crond service.
    start_crond_service()

    # Step 4: Run the component logic. (using simple logger for testing)
    start_logging(local)
