#!/bin/bash

cluster_node1_hostname="ssc-vm-1137"
cluster_node2_hostname="ssc-vm-c-0823"
cluster_name="CORTX_Cluster"

# Authenticate every node you want to add in a cluster
sudo pcs cluster auth ${cluster_node1_hostname} ${cluster_node2_hostname}

# populate a cluster with those nodes
sudo pcs cluster setup --name ${cluster_name} ${cluster_node1_hostname} ${cluster_node2_hostname}

# Enable the cluster and start it
sudo pcs cluster enable --all
sudo pcs cluster start --all


