# Enable Log Rotation for Components

## cortx-re requirements:
- Following RPMs need to be added to cortx-all image:
  - crontabs
  - logrotate

- Refer to [Dockerfile](test/image/Dockerfile) for any further additions required in cortx-all image.

## Options for Log Rotation

### Custom Log Rollover Script with Cron Job
- At container entry point:
  - Run a [startup script](startup/entrypoint_cron.py) (Input to the script is config url).\
  This script will add a crontab entry to periodically schedule the custom log_rollover script.

  - Start the crond service.
  - Continue with further entry-point implementation.

- Custom log_rollover script:
  - Will be scheduled at fixed interval as configured in crontab entry.
  - Log path will the input to the script.
  - Will rotate the logs when run by the cron

### `Logrorate` Utility with Cron Job
- At container entry point:
  - Run a [startup script](startup/entrypoint_logrotate.py) (Input to the script is config url).\
  This script will fetch the local from config and update the log path accordingly in logrotate configuration file & move the config file to the location `/etc/logrotate.d`

  - Start the crond service.
  - Continue with further entry-point implementation.

  **NOTE**: Logrotate applies the config daily by default, can be forced to Hourly by moving the logrotate script from cron.daily to cron.hourly.\
  If we want to schedule it more frequently then we need to add a cron job which runs logrotate config with -f flag.

- Logrotate config:
  - Will have configurations for log rotation.
  - Will have a template `log_path` that should be updated during the startup phase.
  - If config has "_hourly_" as scheduled frequency then please refer the NOTE from entry point stage.

### Python Logger from cortx-py-utils
- Cortx utils has logger with RotatingFileHandler.
- It automatically rotates the logs as per file size and backup files count specified during object creation.
- example usecase is given at ./python/logger_with_rotation.py
