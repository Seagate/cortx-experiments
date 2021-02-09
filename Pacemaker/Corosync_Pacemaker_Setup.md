# Corosync and Pacemaker Setup Guide

**Note:**
1. Run step 1-3 below, on both nodes and other step on primary node node.
2. For configure it on one node follow all step as considering node1

# On Both Node
### Step 1 - OS Settings
* Disable selinux policy on both nodes
```
$ vi /etc/selinux/config
SELINUX=disabled  # Set selinux policy to disabled

$ init 6  # Restart node
```
* Disable firewall on both nodes
```
$ systemctl stop firewalld
$ systemctl disable firewalld
```
* Make sure /etc/hosts is reflected properly or DNS is updated to resolve host names
```
$ cat /etc/hosts
10.0.15.10      node1
10.0.15.11      node2
```

### Step 2 - Install required Software

Install EPEL Repository, corosync pacemaker pcsd.
```
$ yum -y install epel-release
$ yum -y install corosync pacemaker pcs
```

### Step 3 - Configure Pacemaker, Corosync, and Pcsd
Enable pacemaker, corosync, and pcsd service
```
$ systemctl enable pcsd
$ systemctl enable corosync
$ systemctl enable pacemaker
```

Start pcsd service
```
$ systemctl start pcsd
```

Configure a password for the 'hacluster' user.
```
$ echo <new-password> | passwd --stdin hacluster
```

### Step 4 - Create and Configure the Cluster.

Authorise all servers with the pcs command and hacluster user and password.
```
$ pcs cluster auth node1 node2
Username: hacluster
Password:
```

# On Primary Node

Set up the cluster. Define cluster name and servers that will be part of the cluster.
```
$ pcs cluster setup --name HA_cluster node1 node2
```

Now start all cluster services and also enable them.
```
$ pcs cluster start --all
$ pcs cluster enable --all
```

### Step 6 - Disable STONITH and Ignore the Quorum Policy
Since we're not using the fencing device, we will disable the STONITH. STONITH or Shoot The Other Node In The Head is the fencing implementation on Pacemaker. If you're in production, it's better to enable STONITH.
```
$ pcs property set stonith-enabled=false
$ pcs property set no-quorum-policy=ignore
$ pcs property list
```

Check cluster status
```
$ pcs status cluster
```