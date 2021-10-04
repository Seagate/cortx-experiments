#! /bin/bash

# Method can be either `cronjob` or `logrotate`.
# NOTE: The config url should be like "yaml://opt/cortx/component/config.yaml" 
#       kept it as file dir since cortx-utils is not installed.
/usr/bin/python3 /opt/cortx/component/startup/logrotate_setup.py \
--config /opt/cortx/component/config.yaml \
--method cronjob

# start the crond service
/usr/sbin/crond start

# call to the original entrypoint of a component, logger in this case.
/usr/bin/python3 /opt/cortx/component/logger.py
