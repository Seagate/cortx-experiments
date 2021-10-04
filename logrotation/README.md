# Enable Log Rotation for Components

Log rotation options for components
  - linux cron job
  - logrotate

## Linux Cron Job
  - At the entry point,
    - Run a startup script.\
    Input to the script is config url.\
    The script will add a crontab entry to periodically schedule the logrotate script.
    - Start the crond service.
    - Run the component entrypoint script.

  - Logrotate script
    - will be scheduled at fixed interval as configured in crontab entry.
    - log path will the input to the script.
    - will rotate the logs when run by the cron

## Logrotate
  - At the entry point,
    - Run a startup script.\
    Input to the script is config url.\
    The script will fetch the local from config and update the log path accordingly in logrotate configuration file
    & move the config file to the location /etc/logrotate.d  
    _**NOTE**: Logrotate applies the config Daily by default, can be forced to Hourly by moving the logrotate script from cron.daily to cron.hourly.\
    If we want to schedule it more frequently then we need to add a cron job which runs logrotate config with -f flag._
    - start the crond service.
    - Run the component entrypoint script.

  - Logrotate Config
    - will have configurations for log rotation.
    - will have a template log_path that should be updated during the startup phase.
    - if config has "_hourly_" as scheduled frequency then please refer the NOTE from entry point stage.
