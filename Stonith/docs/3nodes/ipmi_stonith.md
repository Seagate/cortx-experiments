### Setup on 3 Node HW (Opposite fencing)

```
*** Checked status of BMC Ipmi nodes and taken our IPS:
smc40-m09-ipmi.colo.seagate.com / 10.230.244.126
smc37-m09-ipmi.colo.seagate.com / 10.230.244.123
smc33-m09-ipmi.colo.seagate.com / 10.230.241.149

*** updated hosts file on each node 

node1 / 192.168.81.104
node2 /  192.168.81.106
node3 / 192.168.81.105

192.168.81.104  node1
192.168.81.106  node2
192.168.81.105  node3

*** Configured cluster

Using this link I have configured cluster on 3 nodes:
https://github.com/Seagate/cortx-ha/wiki/Corosync-Pacemaker-Setup

[root@smc40-m09 cluster]# pcs status
Cluster name: test_cluster
Stack: corosync
Current DC: node2 (version 1.1.23-1.el7-9acf116022) - partition with quorum
Last updated: Sun Feb 14 23:01:59 2021
Last change: Sun Feb 14 22:54:17 2021 by root via cibadmin on node1

3 nodes configured
Online: [ node1 node2 node3]

Daemon Status:
  corosync: active/enabled
  pacemaker: active/enabled
  pcsd: active/enabled


*** Configured Stonith:
pcs stonith create stonith-c1 fence_ipmilan ipaddr=10.230.244.126 login=ADMIN passwd=adminBMC! pcmk_host_list=node1 pcmk_host_check=static-list lanplus=true auth=PASSWORD power_timeout=40 verbose=true op monitor interval=10s meta failure-timeout=15s
pcs stonith create stonith-c2 fence_ipmilan ipaddr=10.230.244.123 login=ADMIN passwd=adminBMC! delay=15 pcmk_host_list=node2 pcmk_host_check=static-list lanplus=true auth=PASSWORD power_timeout=40 verbose=true op monitor interval=10s meta failure-timeout=15s
pcs stonith create stonith-c3 fence_ipmilan ipaddr=10.230.241.149 login=ADMIN passwd=adminBMC! delay=30 pcmk_host_list=node3 pcmk_host_check=static-list lanplus=true auth=PASSWORD power_timeout=40 verbose=true op monitor interval=10s meta failure-timeout=15s

*** Added location constraint to avoid action on same node
 
pcs constraint location stonith-c1 avoids node1
pcs constraint location stonith-c2 avoids node2
pcs constraint location stonith-c3 avoids node3

*** Clone stonith resources

pcs resource clone stonith-c1
pcs resource clone stonith-c2
pcs resource clone stonith-c3

[root@smc40-m09 cluster]# pcs status
Cluster name: test_cluster
Stack: corosync
Current DC: node2 (version 1.1.23-1.el7-9acf116022) - partition with quorum
Last updated: Sun Feb 14 23:01:59 2021
Last change: Sun Feb 14 22:54:17 2021 by root via cibadmin on node1

3 nodes configured
12 resource instances configured

Online: [ node1 node2 ]
OFFLINE: [ node3 ]

Full list of resources:

 Clone Set: dummy-clone [dummy]
     Started: [ node1 node2 node3 ]
 Clone Set: stonith-c1-clone [stonith-c1]
     Started: [ node2 node3 ]
     Stopped: [ node1 ]
 Clone Set: stonith-c2-clone [stonith-c2]
     Started: [ node1 node3 ]
     Stopped: [ node2 ]
 Clone Set: stonith-c3-clone [stonith-c3]
     Started: [ node1 node2 ]
     Stopped: [ node3 ]
   
Daemon Status:
  corosync: active/enabled
  pacemaker: active/enabled
  pcsd: active/enabled  


*** Check stonith device status

[root@smc33-m09 ~]# fence_ipmilan -a 10.230.241.149 -l ADMIN -p adminBMC! -o status
Status: ON
[root@smc33-m09 ~]# fence_ipmilan -a 10.230.244.123 -l ADMIN -p adminBMC! -o status
Status: ON
[root@smc33-m09 ~]# fence_ipmilan -a 10.230.244.126 -l ADMIN -p adminBMC! -o status
Status: ON

==============================
Scenario 1
==============================
*** Did manual fence testing by taking ip link down:
ip link set down enp175s0f1

After the above command execution it has shown the output like below:

[root@smc40-m09 cluster]# pcs status
Cluster name: test_cluster
Stack: corosync
Current DC: node2 (version 1.1.23-1.el7-9acf116022) - partition with quorum
Last updated: Sun Feb 14 23:01:59 2021
Last change: Sun Feb 14 22:54:17 2021 by root via cibadmin on node1

3 nodes configured
12 resource instances configured

Online: [ node1 node2 ]
OFFLINE: [ node3 ]

Full list of resources:

 Clone Set: dummy-clone [dummy]
     Started: [ node1 node2 ]
     Stopped: [ node3 ]
 Clone Set: stonith-c1-clone [stonith-c1]
     Started: [ node2 ]
     Stopped: [ node1 node3 ]
 Clone Set: stonith-c2-clone [stonith-c2]
     Started: [ node1 ]
     Stopped: [ node2 node3 ]
 Clone Set: stonith-c3-clone [stonith-c3]
     Started: [ node1 node2 ]
     Stopped: [ node3 ]

Daemon Status:
  corosync: active/enabled
  pacemaker: active/enabled
  pcsd: active/enabled

Means node3 is stopped and we are good with our POC.

After doing node on manually for node3 we can see its joined the cluster again

*** After making node3 on we are able to the below output

[root@smc40-m09 cluster]# pcs status
Cluster name: test_cluster
Stack: corosync
Current DC: node2 (version 1.1.23-1.el7-9acf116022) - partition with quorum
Last updated: Sun Feb 14 23:13:26 2021
Last change: Sun Feb 14 22:54:17 2021 by root via cibadmin on node1

3 nodes configured
12 resource instances configured

Online: [ node1 node2 node3 ]

Full list of resources:

 Clone Set: dummy-clone [dummy]
     Started: [ node1 node2 node3 ]
 Clone Set: stonith-c1-clone [stonith-c1]
     Started: [ node2 node3 ]
     Stopped: [ node1 ]
 Clone Set: stonith-c2-clone [stonith-c2]
     Started: [ node1 node3 ]
     Stopped: [ node2 ]
 Clone Set: stonith-c3-clone [stonith-c3]
     Started: [ node1 node2 ]
     Stopped: [ node3 ]

Daemon Status:
  corosync: active/enabled
  pacemaker: active/enabled
  pcsd: active/enabled
[root@smc40-m09 cluster]# 

```
