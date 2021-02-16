# Setup on 3 Node HW (Opposite fencing)

1. Taken out IP addresses of BMC IPMI nodes and node HW.

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
```

2. Configured cluster

```
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
```

3. Configured Stonith

```
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
```

4. Check stonith device status

```
[root@smc33-m09 ~]# fence_ipmilan -a 10.230.241.149 -l ADMIN -p adminBMC! -o status
Status: ON
[root@smc33-m09 ~]# fence_ipmilan -a 10.230.244.123 -l ADMIN -p adminBMC! -o status
Status: ON
[root@smc33-m09 ~]# fence_ipmilan -a 10.230.244.126 -l ADMIN -p adminBMC! -o status
Status: ON
```

5. Did fence testing

```
-------------------------------------------------------------
Scenario 1
-------------------------------------------------------------
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
-------------------------------------------------------------
-------------------------------------------------------------
*** Means node3 is stopped and Stonith resources on it also gets stopped

```

5. Results with actual logs

```
Detailed steps of the result: 

1. Node shuts down after we disable the network adapter on the node3 from the cluster

2. In pcs status we can see the node3 is offline due to connection lost with cluster

Feb 16 03:09:11 [27966] smc40-m09.colo.seagate.com       crmd:     info: peer_update_callback:  Client node3/peer now has status [offline] (DC=true, changed=4000000)

3. Election happens between remaining 2 nodes and 1 node became primary

Feb 14 23:30:37 [27960] smc40-m09.colo.seagate.com pacemakerd:     info: pcmk_quorum_notification:      Quorum retained | membership=34 members=2
[27935] smc40-m09.colo.seagate.com corosyncnotice  [MAIN  ] Completed service synchronization, ready to provide service.
Feb 14 23:30:37 [27964] smc40-m09.colo.seagate.com      attrd:     info: pcmk_cpg_membership:   Group attrd event 6: node1 (node 1 pid 27964) is member
Feb 14 23:30:37 [27964] smc40-m09.colo.seagate.com      attrd:     info: pcmk_cpg_membership:   Group attrd event 6: node2 (node 2 pid 2915) is member
Feb 14 23:30:37 [27960] smc40-m09.colo.seagate.com pacemakerd:   notice: crm_update_peer_state_iter:    Node node2 state is now lost | nodeid=3 previous=member source=crm_reap_unseen_nodes
Feb 14 23:30:37 [27966] smc40-m09.colo.seagate.com       crmd:   notice: do_state_transition:   State transition S_NOT_DC -> S_ELECTION | input=I_ELECTION cause=C_CRMD_STATUS_CALLBACK origin=peer_update_callback
Feb 14 23:30:37 [27966] smc40-m09.colo.seagate.com       crmd:     info: election_count_vote:   election-DC round 1 (owner node ID 1) pass: vote from node1 (Uptime)
Feb 14 23:30:37 [27966] smc40-m09.colo.seagate.com       crmd:     info: election_check:        election-DC won by local node
Feb 14 23:30:37 [27966] smc40-m09.colo.seagate.com       crmd:     info: do_log:        Input I_ELECTION_DC received in state S_ELECTION from election_win_cb

4. Joining remaining nodes as memebers

Feb 14 23:30:37 [27966] smc40-m09.colo.seagate.com       crmd:     info: join_make_offer:       Not making join-1 offer to inactive node node3
Feb 14 23:30:37 [27966] smc40-m09.colo.seagate.com       crmd:     info: join_make_offer:       Making join-1 offers based on membership event 34
Feb 14 23:30:37 [27966] smc40-m09.colo.seagate.com       crmd:     info: join_make_offer:       Sending join-1 offer to node2
Feb 14 23:30:37 [27966] smc40-m09.colo.seagate.com       crmd:     info: join_make_offer:       Sending join-1 offer to node1 

5. As node3 is offline in cluster, stonith triggered for verify the same & it got below output to stop the resources running for node3/peer

Feb 16 03:09:12 [27965] smc40-m09.colo.seagate.com    pengine:  warning: custom_action: Action dummy:2_stop_0 on node3 is unrunnable (offline)
Feb 16 03:09:12 [27965] smc40-m09.colo.seagate.com    pengine:  warning: custom_action: Action dummy:2_stop_0 on node3 is unrunnable (offline)
Feb 16 03:09:12 [27965] smc40-m09.colo.seagate.com    pengine:  warning: custom_action: Action stonith-c1:1_stop_0 on node3 is unrunnable (offline)
Feb 16 03:09:12 [27965] smc40-m09.colo.seagate.com    pengine:  warning: custom_action: Action stonith-c1:1_stop_0 on node3 is unrunnable (offline)
Feb 16 03:09:12 [27965] smc40-m09.colo.seagate.com    pengine:  warning: custom_action: Action stonith-c2:1_stop_0 on node3 is unrunnable (offline)
Feb 16 03:09:12 [27965] smc40-m09.colo.seagate.com    pengine:  warning: custom_action: Action stonith-c2:1_stop_0 on node3 is unrunnable (offline)
Feb 16 03:09:12 [27965] smc40-m09.colo.seagate.com    pengine:  warning: stage6:        Scheduling Node node3 for STONITH

6. Status of other resources of stonith we have something like this

Feb 16 03:09:12 [27965] smc40-m09.colo.seagate.com    pengine:     info: native_stop_constraints:       dummy:2_stop_0 is implicit after node3 is fenced
Feb 16 03:09:12 [27965] smc40-m09.colo.seagate.com    pengine:     info: native_stop_constraints:       stonith-c1:1_stop_0 is implicit after node3 is fenced
Feb 16 03:09:12 [27965] smc40-m09.colo.seagate.com    pengine:     info: native_stop_constraints:       stonith-c2:1_stop_0 is implicit after node3 is fenced
Feb 16 03:09:12 [27965] smc40-m09.colo.seagate.com    pengine:   notice: LogNodeActions:         * Fence (off) node3 'peer is no longer part of the cluster'
Feb 16 03:09:12 [27965] smc40-m09.colo.seagate.com    pengine:     info: LogActions:    Leave   dummy:0 (Started node2)
Feb 16 03:09:12 [27965] smc40-m09.colo.seagate.com    pengine:     info: LogActions:    Leave   dummy:1 (Started node1)
Feb 16 03:09:12 [27965] smc40-m09.colo.seagate.com    pengine:   notice: LogAction:      * Stop       dummy:2          ( node3 )   due to node availability
Feb 16 03:09:12 [27965] smc40-m09.colo.seagate.com    pengine:     info: LogActions:    Leave   stonith-c1:0    (Started node2)
Feb 16 03:09:12 [27965] smc40-m09.colo.seagate.com    pengine:   notice: LogAction:      * Stop       stonith-c1:1     ( node3 )   due to node availability
Feb 16 03:09:12 [27965] smc40-m09.colo.seagate.com    pengine:     info: LogActions:    Leave   stonith-c1:2    (Stopped)
Feb 16 03:09:12 [27965] smc40-m09.colo.seagate.com    pengine:     info: LogActions:    Leave   stonith-c2:0    (Started node1)
Feb 16 03:09:12 [27965] smc40-m09.colo.seagate.com    pengine:   notice: LogAction:      * Stop       stonith-c2:1     ( node3 )   due to node availability
Feb 16 03:09:12 [27965] smc40-m09.colo.seagate.com    pengine:     info: LogActions:    Leave   stonith-c2:2    (Stopped)
Feb 16 03:09:12 [27965] smc40-m09.colo.seagate.com    pengine:     info: LogActions:    Leave   stonith-c3:0    (Started node2)
Feb 16 03:09:12 [27965] smc40-m09.colo.seagate.com    pengine:     info: LogActions:    Leave   stonith-c3:1    (Started node1)
Feb 16 03:09:12 [27965] smc40-m09.colo.seagate.com    pengine:     info: LogActions:    Leave   stonith-c3:2    (Stopped)

7. Now system tries to fence the node - node3

Feb 16 03:09:12 [27962] smc40-m09.colo.seagate.com stonith-ng:   notice: handle_request:        Client crmd.27966.49199d43 wants to fence (off) 'node3' with device '(any)'
Feb 16 03:09:12 [27962] smc40-m09.colo.seagate.com stonith-ng:   notice: initiate_remote_stonith_op:    Requesting peer fencing (off) targeting node3 | id=377d32c8-d7b8-4b2e-b282-a91344b4b587 state=0
Feb 16 03:09:12 [27962] smc40-m09.colo.seagate.com stonith-ng:   notice: can_fence_host_with_device:    stonith-c2 can not fence (off) node3: static-list
Feb 16 03:09:12 [27962] smc40-m09.colo.seagate.com stonith-ng:   notice: can_fence_host_with_device:    stonith-c3 can fence (off) node3: static-list
Feb 16 03:09:12 [27962] smc40-m09.colo.seagate.com stonith-ng:   notice: can_fence_host_with_device:    stonith-c2:0 can not fence (off) node3: static-list
Feb 16 03:09:12 [27962] smc40-m09.colo.seagate.com stonith-ng:   notice: can_fence_host_with_device:    stonith-c3:0 can fence (off) node3: static-list
Feb 16 03:09:12 [27962] smc40-m09.colo.seagate.com stonith-ng:     info: process_remote_stonith_query:  Query result 1 of 2 from node1 for node3/off (2 devices) 377d32c8-d7b8-4b2e-b282-a91344b4b587
Feb 16 03:09:12 [27962] smc40-m09.colo.seagate.com stonith-ng:     info: call_remote_stonith:   Total timeout set to 120 for peer's fencing targeting node3 for crmd.27966|id=377d32c8-d7b8-4b2e-b282-a91344b4b587

8. Stonith operated sccessfully by making node3 totally off

Feb 16 03:10:08 [27962] smc40-m09.colo.seagate.com stonith-ng:  warning: log_action:    fence_ipmilan[145788] stderr: [ 2021-02-16 03:09:52,771 INFO: Executing: /usr/bin/ipmitool -I lanplus -H 10.230.241.149 -p 623 -U ADMIN -A PASSWORD -P [set] -L ADMINISTRATOR chassis power status ]
Feb 16 03:10:08 [27962] smc40-m09.colo.seagate.com stonith-ng:  warning: log_action:    fence_ipmilan[145788] stderr: [  ]
Feb 16 03:10:08 [27962] smc40-m09.colo.seagate.com stonith-ng:  warning: log_action:    fence_ipmilan[145788] stderr: [ 2021-02-16 03:10:06,858 DEBUG: 1  Error: Unable to establish IPMI v2 / RMCP+ session ]
Feb 16 03:10:08 [27962] smc40-m09.colo.seagate.com stonith-ng:  warning: log_action:    fence_ipmilan[145788] stderr: [  ]
Feb 16 03:10:08 [27962] smc40-m09.colo.seagate.com stonith-ng:  warning: log_action:    fence_ipmilan[145788] stderr: [  ]
Feb 16 03:10:08 [27962] smc40-m09.colo.seagate.com stonith-ng:  warning: log_action:    fence_ipmilan[145788] stderr: [ 2021-02-16 03:10:07,859 INFO: Executing: /usr/bin/ipmitool -I lanplus -H 10.230.241.149 -p 623 -U ADMIN -A PASSWORD -P [set] -L ADMINISTRATOR chassis power status ]
Feb 16 03:10:08 [27962] smc40-m09.colo.seagate.com stonith-ng:  warning: log_action:    fence_ipmilan[145788] stderr: [  ]
Feb 16 03:10:08 [27962] smc40-m09.colo.seagate.com stonith-ng:  warning: log_action:    fence_ipmilan[145788] stderr: [ 2021-02-16 03:10:08,929 DEBUG: 0 Chassis Power is off ]
Feb 16 03:10:08 [27962] smc40-m09.colo.seagate.com stonith-ng:  warning: log_action:    fence_ipmilan[145788] stderr: [   ]
Feb 16 03:10:08 [27962] smc40-m09.colo.seagate.com stonith-ng:  warning: log_action:    fence_ipmilan[145788] stderr: [  ]
Feb 16 03:10:08 [27962] smc40-m09.colo.seagate.com stonith-ng:   notice: log_operation: Operation 'off' [145788] (call 4 from crmd.27966) for host 'node3' with device 'stonith-c3' returned: 0 (OK)
Feb 16 03:10:08 [27962] smc40-m09.colo.seagate.com stonith-ng:   notice: remote_op_done:        Operation 'off' targeting node3 on node1 for crmd.27966@node1.377d32c8: OK
Feb 16 03:10:08 [27966] smc40-m09.colo.seagate.com       crmd:   notice: tengine_stonith_callback:      Stonith operation 4/1:112:0:0181077d-304e-4ce1-aefb-4bc3cdacd4bf: OK (0)
Feb 16 03:10:08 [27966] smc40-m09.colo.seagate.com       crmd:     info: tengine_stonith_callback:      Stonith operation 4 for node3 passed
Feb 16 03:10:08 [27966] smc40-m09.colo.seagate.com       crmd:     info: crm_update_peer_expected:      crmd_peer_down: Node node3[3] - expected state is now down (was member)
Feb 16 03:10:08 [27961] smc40-m09.colo.seagate.com        cib:     info: cib_process_request:   Forwarding cib_modify operation for section status to all (origin=local/crmd/214)
Feb 16 03:10:08 [27966] smc40-m09.colo.seagate.com       crmd:     info: controld_delete_node_state:    Deleting all state for node node3 (via CIB call 215) | xpath=//node_state[@uname='node3']/*
Feb 16 03:10:08 [27966] smc40-m09.colo.seagate.com       crmd:   notice: tengine_stonith_notify:        Peer node3 was terminated (off) by node1 on behalf of crmd.27966: OK | initiator=node1 ref=377d32c8-d7b8-4b2e-b282-a91344b4b587
Feb 16 03:10:08 [27966] smc40-m09.colo.seagate.com       crmd:     info: controld_delete_node_state:    Deleting all state for node node3 (via CIB call 217) | xpath=//node_state[@uname='node3']/*

```
