#!/bin/bash


# NOTE: resource name should be the remote_name with which we
# modified the hosts file
sudo pcs resource create remote1 ocf:pacemaker:remote

# Check pcs status
sudo pcs status
