# /usr/bin/python3

import argparse
import sys
# from cortx.utils.conf_store import Conf
# NOTE: used pyyaml since cortx-utils is not installed on the container
import yaml
import shutil
import os


def get_local(config_url):
    # Conf.load('Config', config_url)
    # return Conf.get('Config', 'cortx>common>storage>log')

    # NOTE: using pyyaml since cortx.utils is not installed.
    log_dir = None
    with open(config_url) as f:
        conf = yaml.load(f, Loader=yaml.loader.SafeLoader)
        log_dir = (conf["cortx"]["common"]["storage"]["log"])
    return log_dir


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
    setup_logrotate_job(local)
    print(local)
