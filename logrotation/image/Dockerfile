FROM centos:7.9.2009

RUN yum install -y python3 crontabs logrotate

RUN pip3 install pyyaml

RUN mkdir -p /opt/cortx/component/logrotate /opt/cortx/component/startup

COPY ./logger.py ./config.yaml /opt/cortx/component/

ADD ./logrotate /opt/cortx/component/logrotate/

ADD ./startup /opt/cortx/component/startup/

RUN chmod 0644 /opt/cortx/component/logrotate/config/log_rollover.conf /opt/cortx/component/logrotate/cron/log_rollover.py

CMD ["/bin/bash", "/opt/cortx/component/startup/entrypoint.sh"]
