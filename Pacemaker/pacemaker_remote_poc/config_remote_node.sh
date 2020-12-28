#!/bin/bash

# Allow cluster-related services through the local firewall
sudo firewall-cmd --permanent --add-service=high-availability
sudo firewall-cmd --reload

# Install pacemaker-remote daemon on remote node
sudo yum install -y pacemaker-remote resource-agents

# Create a location for the shared authentication key
sudo mkdir -p --mode=0750 /etc/pacemaker
sudo chgrp haclient /etc/pacemaker

# Create a new authentication key for communication if not created already
# NOTE: copy the same key on all the nodes(cluster and remote) for successful
# communication
sudo dd if=/dev/urandom of=/etc/pacemaker/authkey bs=4096 count=1

# Now start and enable the pacemaker_remote daemon on the remote node
sudo systemctl enable pacemaker_remote.service
sudo systemctl start pacemaker_remote.service

# Open the port 3121 on the remote node
sudo firewall-cmd --permanent --add-port=3121/tcp
sudo firewall-cmd --reload

