# Creation of a simple Kubernetes cluster with Ansible

This ansible directory contains of ansible playbook (ansible_k8s_setup.yml) that may be used to create a simple 3-node kubernetes cluster using the latest stable version of kubernetes and the containerd runtime.

## Pre-requisites
- Three pre-provisioned CentOS-7.9 nodes with connectivity to the Internet to download packages and images from repositories and registries.
- A user account with sudo (root) privileges provisioned on the ansible control node and all CentOS-7.9 nodes. Also ensure that the user’s SSH keys are set up to allow execution of the ansible playbook.

## Implementation
- Set the hostname and public IP of each nodes under the host group name '[kubernetes-master-nodes]' and '[kubernetes-worker-nodes]' in the inventory file(*host* file).
- Also in the variables group([all:vars]) set the hostname and public IP for writing inside '/etc/hosts'
- Execute the following command:

      ansible-playbook ansible_k8s_setup.yml -i host

## Working
- In the background *ansible_k8s_setup.yml* invokes 5 different playbooks to setup the entire cluster.
- This particular process will create a k8s cluster in such a way that the master node will also be used to schedule pods(ie. pods on primary).