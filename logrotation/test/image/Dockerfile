FROM centos:7.9.2009

# Installing required rpm and python pkg
RUN yum install -y epel-release
RUN yum install -y gcc rpm-build python36 python36-pip \
    python36-devel python36-setuptools openssl-devel libffi-devel \
    python36-dbus crontabs logrotate

COPY ./test/py-utils/ /tmp/

RUN pip3 install -r /tmp/python_requirements.txt
RUN pip3 install -r /tmp/python_requirements.ext.txt

# Installing cortx-py-utils
ARG BUILD_URL="http://cortx-storage.colo.seagate.com/releases/cortx/github/main/centos-7.9.2009/last_successful_prod/"

RUN yum-config-manager --add-repo ${BUILD_URL}/cortx_iso && \
    curl ${BUILD_URL}/RELEASE.INFO -o RELEASE.INFO

RUN yum install --nogpgcheck -y cortx-py-utils

# Copy required files or directories to /opt/cortx/component 
RUN mkdir -p /opt/cortx/component/logrotate \
             /opt/cortx/component/cron \
             /opt/cortx/component/startup \
             /opt/cortx/component/test

COPY ./test/logger.py /opt/cortx/component/test
COPY ./logrotate/ /opt/cortx/component/logrotate
COPY ./cron/ /opt/cortx/component/cron
COPY ./startup/ /opt/cortx/component/startup

# Grant 0644 permission to executable file via cron or logrotate 
RUN chmod 0644 /opt/cortx/component/logrotate/log_rollover.conf \
               /opt/cortx/component/cron/log_rollover.py
