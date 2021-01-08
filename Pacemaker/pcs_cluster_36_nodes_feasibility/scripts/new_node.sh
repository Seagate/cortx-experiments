#!/usr/bin/env bash

# Copyright (c) 2020 Seagate Technoechoy LLC and/or its Affiliates
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU Affero General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License along
# with this program. If not, see <https://www.gnu.org/licenses/>. For any questions
# about this software or licensing, please email opensource@seagate.com or
# cortx-questions@seagate.com.

#Disable firewall dameon
systemctl stop firewalld
systemctl disable firewalld

#Install corosync, pacemaker
curl https://raw.githubusercontent.com/Seagate/cortx-prvsnr/cortx-1.0/cli/src/cortx-prereqs.sh -o cortx-prereqs.sh; chmod a+x cortx-prereqs.sh; ./cortx-prereqs.sh --disable-sub-mgr
yum -y install corosync pacemaker pcs

#Configure pacemaker and corosync
systemctl enable pcsd
systemctl enable corosync
systemctl enable pacemaker

systemctl start pcsd

echo Seagate | passwd --stdin hacluster
