#!/bin/bash

IP="192.168.49.38"
REMOTE_NAME="remote1"

# Modify /etc/hosts file to enable communication from cluster
# node to remote node on port 3121
echo "$IP $REMOTE_NAME" >> /etc/hosts

# Verify cluster communication on port 3121
ssh -p 3121 $REMOTE_NAME

# Allow cluster-related services through the local firewall
sudo firewall-cmd --permanent --add-service=high-availability
sudo firewall-cmd --reload

# Install corosync, pacemaker services
sudo yum install -y corosync pacemaker pcs

# Enable and start pcs daemon service
sudo systemctl enable pcsd
sudo systemctl start pcsd

# Create a location for the shared authentication key
sudo mkdir -p --mode=0750 /etc/pacemaker
sudo chgrp haclient /etc/pacemaker

# create the cluster
sudo passwd hacluster


