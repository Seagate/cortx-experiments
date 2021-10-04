# /usr/bin/python3

import yaml
import os
import time

config_file = "/opt/cortx/component/config.yaml"
log_dir = ""


def read_log_location():
    with open(config_file) as f:
        conf = yaml.load(f, Loader=yaml.loader.SafeLoader)
        log_dir = (conf["cortx"]["common"]["storage"]["log"])
    return log_dir


def keep_logging_to_file():
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


if __name__ == "__main__":
    local = read_log_location()
    log_dir = os.path.join(local, "component")
    os.makedirs(log_dir, exist_ok=True)
    print(log_dir)
    print("______________________")
    keep_logging_to_file()
