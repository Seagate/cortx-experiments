#!/bin/bash

cluster_name="CORTX_Cluster"

cluster_node1_hostname="ssc-vm-1629"
cluster_node2_hostname="ssc-vm-1630"
cluster_node3_hostname="ssc-vm-1758"

remote_node1_hostname="ssc-vm-1779"
remote_node1_hostname="ssc-vm-1759"

# Create a new authentication key for communication if not created already
sudo dd if=/dev/urandom of=/etc/pacemaker/authkey bs=4096 count=1

# NOTE: copy the same key on all the nodes(cluster and remote) for successful
# communication
sudo scp /etc/pacemaker/authkey ssc-vm-1629.colo.seagate.com:/etc/pacemaker/authkey
sudo scp /etc/pacemaker/authkey ssc-vm-1630.colo.seagate.com:/etc/pacemaker/authkey
sudo scp /etc/pacemaker/authkey ssc-vm-1758.colo.seagate.com:/etc/pacemaker/authkey

# Authenticate every node you want to add in a cluster
sudo pcs cluster auth ${cluster_node1_hostname} ${cluster_node2_hostname}

# populate a cluster with those nodes
sudo pcs cluster setup --name ${cluster_name} ${cluster_node1_hostname} ${cluster_node2_hostname}

# Enable the cluster and start it
sudo pcs cluster enable --all
sudo pcs cluster start --all


