#! /usr/bin/python3

import os
import shutil
import argparse
import sys

config_file = "/opt/cortx/component/config.yaml"
max_file_count = 4


def usage():
    """ Print usage instructions """
    sys.stderr.write(
        "usage:  python3 log_rollover.py --logpath <path>\n"
        "where:\n"
        "path Parent log dir path\n")


if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument(
        '-l', '--logpath',
        help="Parent log dir path"
    )
    args = argParser.parse_args()
    if not args.logpath:
        usage()
        exit(1)
    log_dir = args.logpath
    max_i = 0
    log_file = os.path.join(log_dir, "component.log")
    if os.stat(log_file).st_size == 0:
        exit(0)
    for root, dirs, files in os.walk(log_dir):
        for file in files:
            if file[-1].isdigit() and int(file[-1]) > max_i:
                max_i = int(file[-1])
        print(max_i)
        # copy truncates the log file.
        shutil.copyfile(log_file, f"{log_file}.{max_i+1}")
        with open(log_file, 'w') as logf:
            logf.truncate()
        # rollover is not implemented.
