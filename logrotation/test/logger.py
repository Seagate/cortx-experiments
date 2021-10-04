# /usr/bin/python3

import os
import time
import sys


def keep_logging_to_file(log_dir):
    print("writing infinitely to log file ", end="")
    log_file = os.path.join(log_dir, "component.log")
    i = 0
    while True:
        try:
            with open(log_file, 'a') as logf:
                logf.write(f"Logging the Count: {i}\n")
            i += 1
            print(".", end="")
            time.sleep(5)
        except KeyboardInterrupt:
            print()
            exit(0)
        except Exception as err:
            print(err)
            exit(1)


def start_logging(local):
    log_dir = os.path.join(local, "component")
    os.makedirs(log_dir, exist_ok=True)
    sys.stdout.write(log_dir)
    print("______________________")
    keep_logging_to_file(log_dir)
