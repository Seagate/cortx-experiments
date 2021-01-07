- [Setup network partitioning via iptables](#orgf2e17f9)
  - [Experiment 1: isolate 1 node in 4 node cluster](#org56c2302)
    - [Added following rules on ssc-vm-1550.colo.seagate.com](#org9862f03)
    - [Results:](#org0849ec7)
  - [Experiment 2: stop both clusters and start them at ones](#org657ecaf)
    - [Despite the fact, that cluster is divided, it was stopped on all nodes:](#org223086a)
    - [Start entire cluster running command on 1551](#org53b4d87)
  - [Experiment 3: delete blocking rules from one node](#org9ce4bea)
    - [Commands entered on node 1550:](#orgdd508e6)
    - [Observed behavior](#org213525a)
    - [Logs:](#orgb933403)
  - [Experiment 4: add dummy stonith resources and repeat experiment 1](#org2b46a25)
    - [fence\_dummy.py resource agent will be used to replace real fence agent.](#orgeac56dd)
    - [Stonith configuration performed:](#orga4e41ec)
    - [Stonith configuration testing:](#org49d1654)
    - [Apply iptables rules:](#orgf400b6e)
  - [Experiment 5: isolate one node if 5 node cluster](#org48784a4)
    - [Apply iptables rules:](#orgf2c33b2)
    - [Observed behavior](#org2d187f8)
  - [Summary:](#orgb09a0cb)


<a id="orgf2e17f9"></a>

# Setup network partitioning via iptables

The main idea of following POC is to imitate network problems that lead to partial visibility of selected nodes from corosync protocol perspective. Cluster behavior shall be observed, documented and explained if possible.  
iptables tool is used to force one node to drop packages from another nodes.  


<a id="org56c2302"></a>

## Experiment 1: isolate 1 node in 4 node cluster


<a id="org9862f03"></a>

### Added following rules on ssc-vm-1550.colo.seagate.com

```bash
iptables -A INPUT -s 10.230.242.228 -j DROP
iptables -A INPUT -s 10.230.250.142 -j DROP
```

This blocks all communications with ssc-vm-1552.colo.seagate.com and ssc-vm-1558.colo.seagate.com  
Communications with ssc-vm-1551.colo.seagate.com are still possible.  


<a id="org0849ec7"></a>

### Results:

1.  Node 1552 considers 1550 and 1551 as offline

    ```
    [root@ssc-vm-1552 ~]# pcs status
    Cluster name: new_cluster
    Stack: corosync
    Current DC: ssc-vm-1552.colo.seagate.com (version 1.1.21-4.el7-f14e36fd43) - partition WITHOUT quorum
    Last updated: Sun Dec 20 15:30:10 2020
    Last change: Sun Dec 20 15:16:37 2020 by root via cibadmin on ssc-vm-1550.colo.seagate.com
    
    4 nodes configured
    66 resources configured
    
    Online: [ ssc-vm-1552.colo.seagate.com ssc-vm-1558.colo.seagate.com ]
    OFFLINE: [ ssc-vm-1550.colo.seagate.com ssc-vm-1551.colo.seagate.com ]
    ```

2.  Node 1550 considers 1552 and 1558 as offline (expected)

    ```
    [root@ssc-vm-1550 ~]# pcs status
    Cluster name: new_cluster
    Stack: corosync
    Current DC: ssc-vm-1551.colo.seagate.com (version 1.1.21-4.el7-f14e36fd43) - partition WITHOUT quorum
    Last updated: Sun Dec 20 15:25:34 2020
    Last change: Sun Dec 20 15:16:37 2020 by root via cibadmin on ssc-vm-1550.colo.seagate.com
    
    4 nodes configured
    66 resources configured
    
    Online: [ ssc-vm-1550.colo.seagate.com ssc-vm-1551.colo.seagate.com ]
    OFFLINE: [ ssc-vm-1552.colo.seagate.com ssc-vm-1558.colo.seagate.com ]
    ```

3.  2 different DCs (cluster leaders) are present

4.  Behavior on 1550 node side is expected - both "banned" nodes are displayed as offline

5.  Behavior on 1552 seems unexpected at the first glance. Why node 1551 could not join 1552 and 1558?

6.  corosyn.log on 1550

    ```
    [434] ssc-vm-1550.colo.seagate.com corosyncnotice  [TOTEM ] A processor failed, forming new configuration.
    [434] ssc-vm-1550.colo.seagate.com corosyncnotice  [TOTEM ] A new membership (10.230.240.166:507) was formed. Members left: 4 3
    [434] ssc-vm-1550.colo.seagate.com corosyncnotice  [TOTEM ] Failed to receive the leave message. failed: 4 3
    [434] ssc-vm-1550.colo.seagate.com corosyncwarning [CPG   ] downlist left_list: 2 received
    [434] ssc-vm-1550.colo.seagate.com corosyncwarning [CPG   ] downlist left_list: 2 received
    [434] ssc-vm-1550.colo.seagate.com corosyncnotice  [QUORUM] This node is within the non-primary component and will NOT provide any services.
    [434] ssc-vm-1550.colo.seagate.com corosyncnotice  [QUORUM] Members[2]: 2 1
    [434] ssc-vm-1550.colo.seagate.com corosyncnotice  [MAIN  ] Completed service synchronization, ready to provide service.
    Dec 20 15:24:09 [501] ssc-vm-1550.colo.seagate.com       crmd:  warning: pcmk_quorum_notification:      Quorum lost | membership=507 members=2
    Dec 20 15:24:09 [501] ssc-vm-1550.colo.seagate.com       crmd:   notice: crm_update_peer_state_iter:    Node ssc-vm-1558.colo.seagate.com state is now lost | nodeid=4 previous=member source=crm_reap_unseen_nodes
    Dec 20 15:24:09 [501] ssc-vm-1550.colo.seagate.com       crmd:     info: peer_update_callback:  Cluster node ssc-vm-1558.colo.seagate.com is now lost (was member)
    Dec 20 15:24:09 [501] ssc-vm-1550.colo.seagate.com       crmd:   notice: crm_update_peer_state_iter:    Node ssc-vm-1552.colo.seagate.com state is now lost | nodeid=3 previous=member source=crm_reap_unseen_nodes
    Dec 20 15:24:09 [501] ssc-vm-1550.colo.seagate.com       crmd:     info: peer_update_callback:  Cluster node ssc-vm-1552.colo.seagate.com is now lost (was member)
    Dec 20 15:24:09 [501] ssc-vm-1550.colo.seagate.com       crmd:     info: pcmk_cpg_membership:   Group crmd event 19: ssc-vm-1552.colo.seagate.com (node 3 pid 29007) left via cluster exit
    Dec 20 15:24:09 [501] ssc-vm-1550.colo.seagate.com       crmd:     info: crm_update_peer_proc:  pcmk_cpg_membership: Node ssc-vm-1552.colo.seagate.com[3] - corosync-cpg is now offline
    Dec 20 15:24:09 [501] ssc-vm-1550.colo.seagate.com       crmd:     info: peer_update_callback:  Client ssc-vm-1552.colo.seagate.com/peer now has status [offline] (DC=ssc-vm-1551.colo.seagate.com, changed=4000000)
    Dec 20 15:24:09 [501] ssc-vm-1550.colo.seagate.com       crmd:     info: pcmk_cpg_membership:   Group crmd event 19: ssc-vm-1558.colo.seagate.com (node 4 pid 25538) left via cluster exit
    Dec 20 15:24:09 [501] ssc-vm-1550.colo.seagate.com       crmd:     info: crm_update_peer_proc:  pcmk_cpg_membership: Node ssc-vm-1558.colo.seagate.com[4] - corosync-cpg is now offline
    Dec 20 15:24:09 [501] ssc-vm-1550.colo.seagate.com       crmd:     info: peer_update_callback:  Client ssc-vm-1558.colo.seagate.com/peer now has status [offline] (DC=ssc-vm-1551.colo.seagate.com, changed=4000000)
    Dec 20 15:24:09 [501] ssc-vm-1550.colo.seagate.com       crmd:     info: pcmk_cpg_membership:   Group crmd event 19: ssc-vm-1550.colo.seagate.com (node 1 pid 501) is member
    Dec 20 15:24:09 [501] ssc-vm-1550.colo.seagate.com       crmd:     info: pcmk_cpg_membership:   Group crmd event 19: ssc-vm-1551.colo.seagate.com (node 2 pid 24805) is member
    Dec 20 15:24:09 [497] ssc-vm-1550.colo.seagate.com stonith-ng:     info: pcmk_cpg_membership:   Group stonith-ng event 19: ssc-vm-1552.colo.seagate.com (node 3 pid 29003) left via cluster exit
    Dec 20 15:24:09 [497] ssc-vm-1550.colo.seagate.com stonith-ng:     info: crm_update_peer_proc:  pcmk_cpg_membership: Node ssc-vm-1552.colo.seagate.com[3] - corosync-cpg is now offline
    Dec 20 15:24:09 [497] ssc-vm-1550.colo.seagate.com stonith-ng:   notice: crm_update_peer_state_iter:    Node ssc-vm-1552.colo.seagate.com state is now lost | nodeid=3 previous=member source=crm_update_peer_proc
    Dec 20 15:24:09 [497] ssc-vm-1550.colo.seagate.com stonith-ng:     info: crm_reap_dead_member:  Removing node with name ssc-vm-1552.colo.seagate.com and id 3 from membership cache
    Dec 20 15:24:09 [497] ssc-vm-1550.colo.seagate.com stonith-ng:   notice: reap_crm_member:       Purged 1 peer with id=3 and/or uname=ssc-vm-1552.colo.seagate.com from the membership cache
    Dec 20 15:24:09 [497] ssc-vm-1550.colo.seagate.com stonith-ng:     info: pcmk_cpg_membership:   Group stonith-ng event 19: ssc-vm-1558.colo.seagate.com (node 4 pid 25534) left via cluster exit
    Dec 20 15:24:09 [497] ssc-vm-1550.colo.seagate.com stonith-ng:     info: crm_update_peer_proc:  pcmk_cpg_membership: Node ssc-vm-1558.colo.seagate.com[4] - corosync-cpg is now offline
    Dec 20 15:24:09 [497] ssc-vm-1550.colo.seagate.com stonith-ng:   notice: crm_update_peer_state_iter:    Node ssc-vm-1558.colo.seagate.com state is now lost | nodeid=4 previous=member source=crm_update_peer_proc
    Dec 20 15:24:09 [497] ssc-vm-1550.colo.seagate.com stonith-ng:     info: crm_reap_dead_member:  Removing node with name ssc-vm-1558.colo.seagate.com and id 4 from membership cache
    Dec 20 15:24:09 [497] ssc-vm-1550.colo.seagate.com stonith-ng:   notice: reap_crm_member:       Purged 1 peer with id=4 and/or uname=ssc-vm-1558.colo.seagate.com from the membership cache
    Dec 20 15:24:09 [497] ssc-vm-1550.colo.seagate.com stonith-ng:     info: pcmk_cpg_membership:   Group stonith-ng event 19: ssc-vm-1550.colo.seagate.com (node 1 pid 497) is member
    Dec 20 15:24:09 [497] ssc-vm-1550.colo.seagate.com stonith-ng:     info: pcmk_cpg_membership:   Group stonith-ng event 19: ssc-vm-1551.colo.seagate.com (node 2 pid 24801) is member
    Dec 20 15:24:09 [495] ssc-vm-1550.colo.seagate.com pacemakerd:  warning: pcmk_quorum_notification:      Quorum lost | membership=507 members=2
    Dec 20 15:24:09 [495] ssc-vm-1550.colo.seagate.com pacemakerd:   notice: crm_update_peer_state_iter:    Node ssc-vm-1558.colo.seagate.com state is now lost | nodeid=4 previous=member source=crm_reap_unseen_nodes
    Dec 20 15:24:09 [495] ssc-vm-1550.colo.seagate.com pacemakerd:   notice: crm_update_peer_state_iter:    Node ssc-vm-1552.colo.seagate.com state is now lost | nodeid=3 previous=member source=crm_reap_unseen_nodes
    Dec 20 15:24:09 [499] ssc-vm-1550.colo.seagate.com      attrd:     info: pcmk_cpg_membership:   Group attrd event 21: ssc-vm-1552.colo.seagate.com (node 3 pid 29005) left via cluster exit
    Dec 20 15:24:09 [499] ssc-vm-1550.colo.seagate.com      attrd:     info: crm_update_peer_proc:  pcmk_cpg_membership: Node ssc-vm-1552.colo.seagate.com[3] - corosync-cpg is now offline
    Dec 20 15:24:09 [495] ssc-vm-1550.colo.seagate.com pacemakerd:     info: pcmk_cpg_membership:   Group pacemakerd event 21: ssc-vm-1552.colo.seagate.com (node 3 pid 29001) left via cluster exit
    Dec 20 15:24:09 [495] ssc-vm-1550.colo.seagate.com pacemakerd:     info: crm_update_peer_proc:  pcmk_cpg_membership: Node ssc-vm-1552.colo.seagate.com[3] - corosync-cpg is now offline
    Dec 20 15:24:09 [495] ssc-vm-1550.colo.seagate.com pacemakerd:     info: pcmk_cpg_membership:   Group pacemakerd event 21: ssc-vm-1558.colo.seagate.com (node 4 pid 25532) left via cluster exit
    Dec 20 15:24:09 [495] ssc-vm-1550.colo.seagate.com pacemakerd:     info: crm_update_peer_proc:  pcmk_cpg_membership: Node ssc-vm-1558.colo.seagate.com[4] - corosync-cpg is now offline
    Dec 20 15:24:09 [495] ssc-vm-1550.colo.seagate.com pacemakerd:     info: pcmk_cpg_membership:   Group pacemakerd event 21: ssc-vm-1550.colo.seagate.com (node 1 pid 495) is member
    Dec 20 15:24:09 [495] ssc-vm-1550.colo.seagate.com pacemakerd:     info: pcmk_cpg_membership:   Group pacemakerd event 21: ssc-vm-1551.colo.seagate.com (node 2 pid 24799) is member
    Dec 20 15:24:09 [499] ssc-vm-1550.colo.seagate.com      attrd:   notice: crm_update_peer_state_iter:    Node ssc-vm-1552.colo.seagate.com state is now lost | nodeid=3 previous=member source=crm_update_peer_proc
    Dec 20 15:24:09 [499] ssc-vm-1550.colo.seagate.com      attrd:   notice: attrd_peer_remove:     Removing all ssc-vm-1552.colo.seagate.com attributes for peer loss
    Dec 20 15:24:09 [499] ssc-vm-1550.colo.seagate.com      attrd:     info: crm_reap_dead_member:  Removing node with name ssc-vm-1552.colo.seagate.com and id 3 from membership cache
    Dec 20 15:24:09 [499] ssc-vm-1550.colo.seagate.com      attrd:   notice: reap_crm_member:       Purged 1 peer with id=3 and/or uname=ssc-vm-1552.colo.seagate.com from the membership cache
    Dec 20 15:24:09 [499] ssc-vm-1550.colo.seagate.com      attrd:     info: pcmk_cpg_membership:   Group attrd event 21: ssc-vm-1558.colo.seagate.com (node 4 pid 25536) left via cluster exit
    Dec 20 15:24:09 [499] ssc-vm-1550.colo.seagate.com      attrd:     info: crm_update_peer_proc:  pcmk_cpg_membership: Node ssc-vm-1558.colo.seagate.com[4] - corosync-cpg is now offline
    Dec 20 15:24:09 [499] ssc-vm-1550.colo.seagate.com      attrd:   notice: crm_update_peer_state_iter:    Node ssc-vm-1558.colo.seagate.com state is now lost | nodeid=4 previous=member source=crm_update_peer_proc
    Dec 20 15:24:09 [499] ssc-vm-1550.colo.seagate.com      attrd:   notice: attrd_peer_remove:     Removing all ssc-vm-1558.colo.seagate.com attributes for peer loss
    Dec 20 15:24:09 [499] ssc-vm-1550.colo.seagate.com      attrd:     info: crm_reap_dead_member:  Removing node with name ssc-vm-1558.colo.seagate.com and id 4 from membership cache
    Dec 20 15:24:09 [495] ssc-vm-1550.colo.seagate.com pacemakerd:     info: mcp_cpg_deliver:       Ignoring process list sent by peer for local node
    Dec 20 15:24:09 [499] ssc-vm-1550.colo.seagate.com      attrd:   notice: reap_crm_member:       Purged 1 peer with id=4 and/or uname=ssc-vm-1558.colo.seagate.com from the membership cache
    Dec 20 15:24:09 [499] ssc-vm-1550.colo.seagate.com      attrd:     info: pcmk_cpg_membership:   Group attrd event 21: ssc-vm-1550.colo.seagate.com (node 1 pid 499) is member
    Dec 20 15:24:09 [499] ssc-vm-1550.colo.seagate.com      attrd:     info: pcmk_cpg_membership:   Group attrd event 21: ssc-vm-1551.colo.seagate.com (node 2 pid 24803) is member
    ...
    [434] ssc-vm-1550.colo.seagate.com corosyncnotice  [TOTEM ] A new membership (10.230.240.166:519) was formed. Members
    [434] ssc-vm-1550.colo.seagate.com corosyncwarning [CPG   ] downlist left_list: 0 received
    [434] ssc-vm-1550.colo.seagate.com corosyncwarning [CPG   ] downlist left_list: 0 received
    [434] ssc-vm-1550.colo.seagate.com corosyncnotice  [QUORUM] Members[2]: 2 1
    [434] ssc-vm-1550.colo.seagate.com corosyncnotice  [MAIN  ] Completed service synchronization, ready to provide service.
    Dec 20 15:24:14 [495] ssc-vm-1550.colo.seagate.com pacemakerd:     info: pcmk_quorum_notification:      Quorum still lost | membership=519 members=2
    Dec 20 15:24:14 [501] ssc-vm-1550.colo.seagate.com       crmd:     info: pcmk_quorum_notification:      Quorum still lost | membership=519 members=2
    ```

7.  corosync.log on 1552

    ```
    [28986] ssc-vm-1552.colo.seagate.com corosyncnotice  [TOTEM ] A processor failed, forming new configuration.
    [28986] ssc-vm-1552.colo.seagate.com corosyncnotice  [TOTEM ] A new membership (10.230.242.228:507) was formed. Members left: 2 1
    [28986] ssc-vm-1552.colo.seagate.com corosyncnotice  [TOTEM ] Failed to receive the leave message. failed: 2 1
    [28986] ssc-vm-1552.colo.seagate.com corosyncwarning [CPG   ] downlist left_list: 2 received
    [28986] ssc-vm-1552.colo.seagate.com corosyncwarning [CPG   ] downlist left_list: 2 received
    [28986] ssc-vm-1552.colo.seagate.com corosyncnotice  [QUORUM] This node is within the non-primary component and will NOT provide any services.
    [28986] ssc-vm-1552.colo.seagate.com corosyncnotice  [QUORUM] Members[2]: 4 3
    [28986] ssc-vm-1552.colo.seagate.com corosyncnotice  [MAIN  ] Completed service synchronization, ready to provide service.
    Dec 20 15:24:09 [29007] ssc-vm-1552.colo.seagate.com       crmd:  warning: pcmk_quorum_notification:    Quorum lost | membership=507 members=2
    Dec 20 15:24:09 [29007] ssc-vm-1552.colo.seagate.com       crmd:   notice: crm_update_peer_state_iter:  Node ssc-vm-1551.colo.seagate.com state is now lost | nodeid=2 previous=member source=crm_reap_unseen_nodes
    Dec 20 15:24:09 [29007] ssc-vm-1552.colo.seagate.com       crmd:     info: peer_update_callback:        Cluster node ssc-vm-1551.colo.seagate.com is now lost (was member)
    Dec 20 15:24:09 [29007] ssc-vm-1552.colo.seagate.com       crmd:   notice: crm_update_peer_state_iter:  Node ssc-vm-1550.colo.seagate.com state is now lost | nodeid=1 previous=member source=crm_reap_unseen_nodes
    Dec 20 15:24:09 [29007] ssc-vm-1552.colo.seagate.com       crmd:     info: peer_update_callback:        Cluster node ssc-vm-1550.colo.seagate.com is now lost (was member)
    Dec 20 15:24:09 [29007] ssc-vm-1552.colo.seagate.com       crmd:  warning: reap_dead_nodes:     Our DC node (ssc-vm-1551.colo.seagate.com) left the cluster
    Dec 20 15:24:09 [29007] ssc-vm-1552.colo.seagate.com       crmd:   notice: do_state_transition: State transition S_NOT_DC -> S_ELECTION | input=I_ELECTION cause=C_FSA_INTERNAL origin=reap_dead_nodes
    Dec 20 15:24:09 [29007] ssc-vm-1552.colo.seagate.com       crmd:     info: update_dc:   Unset DC. Was ssc-vm-1551.colo.seagate.com
    Dec 20 15:24:09 [29007] ssc-vm-1552.colo.seagate.com       crmd:     info: pcmk_cpg_membership: Group crmd event 22: ssc-vm-1550.colo.seagate.com (node 1 pid 501) left via cluster exit
    Dec 20 15:24:09 [29007] ssc-vm-1552.colo.seagate.com       crmd:     info: crm_update_peer_proc:        pcmk_cpg_membership: Node ssc-vm-1550.colo.seagate.com[1] - corosync-cpg is now offline
    Dec 20 15:24:09 [29007] ssc-vm-1552.colo.seagate.com       crmd:     info: peer_update_callback:        Client ssc-vm-1550.colo.seagate.com/peer now has status [offline] (DC=<null>, changed=4000000)
    Dec 20 15:24:09 [29007] ssc-vm-1552.colo.seagate.com       crmd:     info: pcmk_cpg_membership: Group crmd event 22: ssc-vm-1551.colo.seagate.com (node 2 pid 24805) left via cluster exit
    Dec 20 15:24:09 [29007] ssc-vm-1552.colo.seagate.com       crmd:     info: crm_update_peer_proc:        pcmk_cpg_membership: Node ssc-vm-1551.colo.seagate.com[2] - corosync-cpg is now offline
    Dec 20 15:24:09 [29007] ssc-vm-1552.colo.seagate.com       crmd:     info: peer_update_callback:        Client ssc-vm-1551.colo.seagate.com/peer now has status [offline] (DC=<null>, changed=4000000)
    Dec 20 15:24:09 [29007] ssc-vm-1552.colo.seagate.com       crmd:     info: pcmk_cpg_membership: Group crmd event 22: ssc-vm-1552.colo.seagate.com (node 3 pid 29007) is member
    Dec 20 15:24:09 [29007] ssc-vm-1552.colo.seagate.com       crmd:     info: pcmk_cpg_membership: Group crmd event 22: ssc-vm-1558.colo.seagate.com (node 4 pid 25538) is member
    Dec 20 15:24:09 [29003] ssc-vm-1552.colo.seagate.com stonith-ng:     info: pcmk_cpg_membership: Group stonith-ng event 22: ssc-vm-1550.colo.seagate.com (node 1 pid 497) left via cluster exit
    Dec 20 15:24:09 [29003] ssc-vm-1552.colo.seagate.com stonith-ng:     info: crm_update_peer_proc:        pcmk_cpg_membership: Node ssc-vm-1550.colo.seagate.com[1] - corosync-cpg is now offline
    Dec 20 15:24:09 [29003] ssc-vm-1552.colo.seagate.com stonith-ng:   notice: crm_update_peer_state_iter:  Node ssc-vm-1550.colo.seagate.com state is now lost | nodeid=1 previous=member source=crm_update_peer_proc
    Dec 20 15:24:09 [29005] ssc-vm-1552.colo.seagate.com      attrd:     info: pcmk_cpg_membership: Group attrd event 25: ssc-vm-1550.colo.seagate.com (node 1 pid 499) left via cluster exit
    Dec 20 15:24:09 [29005] ssc-vm-1552.colo.seagate.com      attrd:     info: crm_update_peer_proc:        pcmk_cpg_membership: Node ssc-vm-1550.colo.seagate.com[1] - corosync-cpg is now offline
    Dec 20 15:24:09 [29001] ssc-vm-1552.colo.seagate.com pacemakerd:     info: pcmk_cpg_membership: Group pacemakerd event 26: ssc-vm-1550.colo.seagate.com (node 1 pid 495) left via cluster exit
    Dec 20 15:24:09 [29001] ssc-vm-1552.colo.seagate.com pacemakerd:     info: crm_update_peer_proc:        pcmk_cpg_membership: Node ssc-vm-1550.colo.seagate.com[1] - corosync-cpg is now offline
    Dec 20 15:24:09 [29001] ssc-vm-1552.colo.seagate.com pacemakerd:     info: pcmk_cpg_membership: Group pacemakerd event 26: ssc-vm-1551.colo.seagate.com (node 2 pid 24799) left via cluster exit
    Dec 20 15:24:09 [29001] ssc-vm-1552.colo.seagate.com pacemakerd:     info: crm_update_peer_proc:        pcmk_cpg_membership: Node ssc-vm-1551.colo.seagate.com[2] - corosync-cpg is now offline
    Dec 20 15:24:09 [29001] ssc-vm-1552.colo.seagate.com pacemakerd:     info: pcmk_cpg_membership: Group pacemakerd event 26: ssc-vm-1552.colo.seagate.com (node 3 pid 29001) is member
    Dec 20 15:24:09 [29001] ssc-vm-1552.colo.seagate.com pacemakerd:     info: pcmk_cpg_membership: Group pacemakerd event 26: ssc-vm-1558.colo.seagate.com (node 4 pid 25532) is member
    Dec 20 15:24:09 [29003] ssc-vm-1552.colo.seagate.com stonith-ng:     info: crm_reap_dead_member:        Removing node with name ssc-vm-1550.colo.seagate.com and id 1 from membership cache
    Dec 20 15:24:09 [29003] ssc-vm-1552.colo.seagate.com stonith-ng:   notice: reap_crm_member:     Purged 1 peer with id=1 and/or uname=ssc-vm-1550.colo.seagate.com from the membership cache
    Dec 20 15:24:09 [29003] ssc-vm-1552.colo.seagate.com stonith-ng:     info: pcmk_cpg_membership: Group stonith-ng event 22: ssc-vm-1551.colo.seagate.com (node 2 pid 24801) left via cluster exit
    Dec 20 15:24:09 [29003] ssc-vm-1552.colo.seagate.com stonith-ng:     info: crm_update_peer_proc:        pcmk_cpg_membership: Node ssc-vm-1551.colo.seagate.com[2] - corosync-cpg is now offline
    Dec 20 15:24:09 [29003] ssc-vm-1552.colo.seagate.com stonith-ng:   notice: crm_update_peer_state_iter:  Node ssc-vm-1551.colo.seagate.com state is now lost | nodeid=2 previous=member source=crm_update_peer_proc
    Dec 20 15:24:09 [29005] ssc-vm-1552.colo.seagate.com      attrd:   notice: crm_update_peer_state_iter:  Node ssc-vm-1550.colo.seagate.com state is now lost | nodeid=1 previous=member source=crm_update_peer_proc
    Dec 20 15:24:09 [29005] ssc-vm-1552.colo.seagate.com      attrd:   notice: attrd_peer_remove:   Removing all ssc-vm-1550.colo.seagate.com attributes for peer loss
    Dec 20 15:24:09 [29005] ssc-vm-1552.colo.seagate.com      attrd:     info: crm_reap_dead_member:        Removing node with name ssc-vm-1550.colo.seagate.com and id 1 from membership cache
    Dec 20 15:24:09 [29005] ssc-vm-1552.colo.seagate.com      attrd:   notice: reap_crm_member:     Purged 1 peer with id=1 and/or uname=ssc-vm-1550.colo.seagate.com from the membership cache
    Dec 20 15:24:09 [29005] ssc-vm-1552.colo.seagate.com      attrd:     info: pcmk_cpg_membership: Group attrd event 25: ssc-vm-1551.colo.seagate.com (node 2 pid 24803) left via cluster exit
    Dec 20 15:24:09 [29005] ssc-vm-1552.colo.seagate.com      attrd:     info: crm_update_peer_proc:        pcmk_cpg_membership: Node ssc-vm-1551.colo.seagate.com[2] - corosync-cpg is now offline
    Dec 20 15:24:09 [29005] ssc-vm-1552.colo.seagate.com      attrd:   notice: attrd_remove_voter:  Lost attribute writer ssc-vm-1551.colo.seagate.com
    Dec 20 15:24:09 [29005] ssc-vm-1552.colo.seagate.com      attrd:     info: attrd_start_election_if_needed:      Starting an election to determine the writer
    Dec 20 15:24:09 [29003] ssc-vm-1552.colo.seagate.com stonith-ng:     info: crm_reap_dead_member:        Removing node with name ssc-vm-1551.colo.seagate.com and id 2 from membership cache
    Dec 20 15:24:09 [29003] ssc-vm-1552.colo.seagate.com stonith-ng:   notice: reap_crm_member:     Purged 1 peer with id=2 and/or uname=ssc-vm-1551.colo.seagate.com from the membership cache
    Dec 20 15:24:09 [29003] ssc-vm-1552.colo.seagate.com stonith-ng:     info: pcmk_cpg_membership: Group stonith-ng event 22: ssc-vm-1552.colo.seagate.com (node 3 pid 29003) is member
    Dec 20 15:24:09 [29003] ssc-vm-1552.colo.seagate.com stonith-ng:     info: pcmk_cpg_membership: Group stonith-ng event 22: ssc-vm-1558.colo.seagate.com (node 4 pid 25534) is member
    Dec 20 15:24:09 [29001] ssc-vm-1552.colo.seagate.com pacemakerd:  warning: pcmk_quorum_notification:    Quorum lost | membership=507 members=2
    Dec 20 15:24:09 [29001] ssc-vm-1552.colo.seagate.com pacemakerd:   notice: crm_update_peer_state_iter:  Node ssc-vm-1551.colo.seagate.com state is now lost | nodeid=2 previous=member source=crm_reap_unseen_nodes
    Dec 20 15:24:09 [29001] ssc-vm-1552.colo.seagate.com pacemakerd:   notice: crm_update_peer_state_iter:  Node ssc-vm-1550.colo.seagate.com state is now lost | nodeid=1 previous=member source=crm_reap_unseen_nodes
    Dec 20 15:24:09 [29005] ssc-vm-1552.colo.seagate.com      attrd:   notice: crm_update_peer_state_iter:  Node ssc-vm-1551.colo.seagate.com state is now lost | nodeid=2 previous=member source=crm_update_peer_proc
    Dec 20 15:24:09 [29005] ssc-vm-1552.colo.seagate.com      attrd:   notice: attrd_peer_remove:   Removing all ssc-vm-1551.colo.seagate.com attributes for peer loss
    Dec 20 15:24:09 [29005] ssc-vm-1552.colo.seagate.com      attrd:     info: crm_reap_dead_member:        Removing node with name ssc-vm-1551.colo.seagate.com and id 2 from membership cache
    Dec 20 15:24:09 [29005] ssc-vm-1552.colo.seagate.com      attrd:   notice: attrd_peer_remove:   Removing all ssc-vm-1551.colo.seagate.com attributes for peer loss
    Dec 20 15:24:09 [29005] ssc-vm-1552.colo.seagate.com      attrd:     info: crm_reap_dead_member:        Removing node with name ssc-vm-1551.colo.seagate.com and id 2 from membership cache
    Dec 20 15:24:09 [29005] ssc-vm-1552.colo.seagate.com      attrd:   notice: reap_crm_member:     Purged 1 peer with id=2 and/or uname=ssc-vm-1551.colo.seagate.com from the membership cache
    Dec 20 15:24:09 [29005] ssc-vm-1552.colo.seagate.com      attrd:     info: pcmk_cpg_membership: Group attrd event 25: ssc-vm-1552.colo.seagate.com (node 3 pid 29005) is member
    Dec 20 15:24:09 [29005] ssc-vm-1552.colo.seagate.com      attrd:     info: pcmk_cpg_membership: Group attrd event 25: ssc-vm-1558.colo.seagate.com (node 4 pid 25536) is member
    Dec 20 15:24:09 [29001] ssc-vm-1552.colo.seagate.com pacemakerd:     info: mcp_cpg_deliver:     Ignoring process list sent by peer for local node
    Dec 20 15:24:09 [29005] ssc-vm-1552.colo.seagate.com      attrd:     info: election_count_vote: election-attrd round 10 (owner node ID 4) pass: vote from ssc-vm-1558.colo.seagate.com (Uptime)
    Dec 20 15:24:09 [29005] ssc-vm-1552.colo.seagate.com      attrd:     info: election_check:      election-attrd won by local node
    Dec 20 15:24:09 [29005] ssc-vm-1552.colo.seagate.com      attrd:   notice: attrd_declare_winner:        Recorded local node as attribute writer (was unset)
    Dec 20 15:24:09 [29005] ssc-vm-1552.colo.seagate.com      attrd:     info: write_attribute:     Processed 2 private changes for #attrd-protocol, id=n/a, set=n/a
    Dec 20 15:24:09 [29007] ssc-vm-1552.colo.seagate.com       crmd:     info: election_count_vote: election-DC round 4 (owner node ID 4) pass: vote from ssc-vm-1558.colo.seagate.com (Uptime)
    Dec 20 15:24:09 [29007] ssc-vm-1552.colo.seagate.com       crmd:     info: election_check:      election-DC won by local node
    Dec 20 15:24:09 [29007] ssc-vm-1552.colo.seagate.com       crmd:     info: do_log:      Input I_ELECTION_DC received in state S_ELECTION from election_win_cb
    Dec 20 15:24:09 [29007] ssc-vm-1552.colo.seagate.com       crmd:   notice: do_state_transition: State transition S_ELECTION -> S_INTEGRATION | input=I_ELECTION_DC cause=C_FSA_INTERNAL origin=election_win_cb
    Dec 20 15:24:09 [29007] ssc-vm-1552.colo.seagate.com       crmd:     info: do_te_control:       Registering TE UUID: 597a2c96-e379-403d-bb36-cf13b0459500
    Dec 20 15:24:09 [29007] ssc-vm-1552.colo.seagate.com       crmd:     info: set_graph_functions: Setting custom graph functions
    Dec 20 15:24:09 [29007] ssc-vm-1552.colo.seagate.com       crmd:     info: do_dc_takeover:      Taking over DC status for this partition
    Dec 20 15:24:09 [29007] ssc-vm-1552.colo.seagate.com       crmd:     info: join_make_offer:     Not making join-1 offer to inactive node ssc-vm-1551.colo.seagate.com
    Dec 20 15:24:09 [29007] ssc-vm-1552.colo.seagate.com       crmd:     info: join_make_offer:     Making join-1 offers based on membership event 507
    Dec 20 15:24:09 [29007] ssc-vm-1552.colo.seagate.com       crmd:     info: join_make_offer:     Sending join-1 offer to ssc-vm-1552.colo.seagate.com
    Dec 20 15:24:09 [29007] ssc-vm-1552.colo.seagate.com       crmd:     info: join_make_offer:     Sending join-1 offer to ssc-vm-1558.colo.seagate.com
    Dec 20 15:24:09 [29007] ssc-vm-1552.colo.seagate.com       crmd:     info: join_make_offer:     Not making join-1 offer to inactive node ssc-vm-1550.colo.seagate.com
    Dec 20 15:24:09 [29007] ssc-vm-1552.colo.seagate.com       crmd:     info: crm_update_peer_expected:    join_make_offer: Node ssc-vm-1550.colo.seagate.com[1] - expected state is now down (was (null))
    Dec 20 15:24:09 [29007] ssc-vm-1552.colo.seagate.com       crmd:     info: do_dc_join_offer_all:        Waiting on join-1 requests from 2 outstanding nodes
    Dec 20 15:24:09 [29007] ssc-vm-1552.colo.seagate.com       crmd:     info: update_dc:   Set DC to ssc-vm-1552.colo.seagate.com (3.0.14)
    Dec 20 15:24:09 [29007] ssc-vm-1552.colo.seagate.com       crmd:     info: crm_update_peer_expected:    update_dc: Node ssc-vm-1552.colo.seagate.com[3] - expected state is now member (was (null))
    Dec 20 15:24:09 [29007] ssc-vm-1552.colo.seagate.com       crmd:     info: crm_update_peer_expected:    do_dc_join_filter_offer: Node ssc-vm-1558.colo.seagate.com[4] - expected state is now member (was (null))
    Dec 20 15:24:09 [29007] ssc-vm-1552.colo.seagate.com       crmd:     info: do_state_transition: State transition S_INTEGRATION -> S_FINALIZE_JOIN | input=I_INTEGRATED cause=C_FSA_INTERNAL origin=check_join_state
    Dec 20 15:24:09 [29007] ssc-vm-1552.colo.seagate.com       crmd:     info: controld_delete_node_state:  Deleting resource history for node ssc-vm-1552.colo.seagate.com (via CIB call 3359) | xpath=//node_state[@uname='ssc-vm-1552.colo.seagate.com']/lrm
    Dec 20 15:24:09 [29007] ssc-vm-1552.colo.seagate.com       crmd:     info: controld_delete_node_state:  Deleting resource history for node ssc-vm-1558.colo.seagate.com (via CIB call 3361) | xpath=//node_state[@uname='ssc-vm-1558.colo.seagate.com']/lrm
    Dec 20 15:24:09 [29007] ssc-vm-1552.colo.seagate.com       crmd:     info: do_state_transition: State transition S_FINALIZE_JOIN -> S_POLICY_ENGINE | input=I_FINALIZED cause=C_FSA_INTERNAL origin=check_join_state
    Dec 20 15:24:09 [29007] ssc-vm-1552.colo.seagate.com       crmd:     info: abort_transition_graph:      Transition aborted: Quorum lost | source=crm_update_quorum:456 complete=true
    Dec 20 15:24:09 [29007] ssc-vm-1552.colo.seagate.com       crmd:     info: abort_transition_graph:      Transition aborted: Peer Cancelled | source=do_te_invoke:143 complete=true
    Dec 20 15:24:09 [29007] ssc-vm-1552.colo.seagate.com       crmd:     info: abort_transition_graph:      Transition aborted by deletion of lrm[@id='4']: Resource state removal | cib=0.153.9 source=abort_unless_down:370 path=/cib/status/node_state[@id='4']/lrm[@id='4'] complete=true
    Dec 20 15:24:09 [29007] ssc-vm-1552.colo.seagate.com       crmd:     info: abort_transition_graph:      Transition aborted: LRM Refresh | source=process_resource_updates:294 complete=true
    Dec 20 15:24:09 [29006] ssc-vm-1552.colo.seagate.com    pengine:  warning: unpack_config:       Blind faith: not fencing unseen nodes
    Dec 20 15:24:09 [29006] ssc-vm-1552.colo.seagate.com    pengine:  warning: cluster_status:      Fencing and resource management disabled due to lack of quorum
    Dec 20 15:24:09 [29006] ssc-vm-1552.colo.seagate.com    pengine:     info: determine_online_status:     Node ssc-vm-1558.colo.seagate.com is online
    Dec 20 15:24:09 [29006] ssc-vm-1552.colo.seagate.com    pengine:     info: determine_online_status:     Node ssc-vm-1552.colo.seagate.com is online
    ```

8.  rs-dummy-{1,2} resources didn't start due to missing quorum

    ```
    Dec 20 15:24:09 [29006] ssc-vm-1552.colo.seagate.com    pengine:   notice: LogAction:    * Start      rs-dummy-1     ( ssc-vm-1552.colo.seagate.com )   due to no quorum (blocked)
    Dec 20 15:24:09 [29006] ssc-vm-1552.colo.seagate.com    pengine:   notice: LogAction:    * Stop       rs-dummy-2     ( ssc-vm-1552.colo.seagate.com )   due to no quorum
    ```

9.  Both network partitions are considered as incomplete making cluster unusable.

    This is reasonable state assuming the fact that stonith is disabled in the cluster.  

10. Not clean why 1551 chosen to form cluster partition with 1550.

    In this situation it looks logical to expect 1551, 1552 and 1158 to form a cluster with a quorum and exclude 1550 from cluster.  


<a id="org657ecaf"></a>

## Experiment 2: stop both clusters and start them at ones


<a id="org223086a"></a>

### Despite the fact, that cluster is divided, it was stopped on all nodes:

```
[root@ssc-vm-1551 ~]# pcs cluster stop --all
ssc-vm-1558.colo.seagate.com: Stopping Cluster (pacemaker)...
ssc-vm-1552.colo.seagate.com: Stopping Cluster (pacemaker)...
ssc-vm-1551.colo.seagate.com: Stopping Cluster (pacemaker)...
ssc-vm-1550.colo.seagate.com: Stopping Cluster (pacemaker)...
ssc-vm-1558.colo.seagate.com: Stopping Cluster (corosync)...
ssc-vm-1550.colo.seagate.com: Stopping Cluster (corosync)...
ssc-vm-1551.colo.seagate.com: Stopping Cluster (corosync)...
ssc-vm-1552.colo.seagate.com: Stopping Cluster (corosync)...
```


<a id="org53b4d87"></a>

### Start entire cluster running command on 1551

Logic behind that move is to check whether cluster can "regroup" if started from the node which can access all nodes in the cluster.  

1.  Result is the same cluster configuration with 2 partitions:

    ```
    [root@ssc-vm-1551 ~]# pcs status
    Cluster name: new_cluster
    Stack: corosync
    Current DC: ssc-vm-1551.colo.seagate.com (version 1.1.21-4.el7-f14e36fd43) - partition WITHOUT quorum
    Last updated: Sun Dec 20 17:37:00 2020
    Last change: Sun Dec 20 15:16:37 2020 by root via cibadmin on ssc-vm-1550.colo.seagate.com
    
    4 nodes configured
    66 resources configured
    
    Online: [ ssc-vm-1550.colo.seagate.com ssc-vm-1551.colo.seagate.com ]
    OFFLINE: [ ssc-vm-1552.colo.seagate.com ssc-vm-1558.colo.seagate.com ]
    
    Full list of resources:
    
    ```


<a id="org9ce4bea"></a>

## Experiment 3: delete blocking rules from one node


<a id="orgdd508e6"></a>

### Commands entered on node 1550:

```bash
[root@ssc-vm-1550 ~]# iptables -D INPUT -s 10.230.250.142/32 -j DROP
[root@ssc-vm-1550 ~]# iptables -D INPUT -s 10.230.242.228/32 -j DROP
```


<a id="org213525a"></a>

### Observed behavior

Cluster immediately restored quorum. All nodes are online. All resources are online.  


<a id="orgb933403"></a>

### Logs:

```
[8105] ssc-vm-1552.colo.seagate.com corosyncnotice  [TOTEM ] A new membership (10.230.240.166:425968) was formed. Members joined: 2 1
[8105] ssc-vm-1552.colo.seagate.com corosyncwarning [CPG   ] downlist left_list: 0 received
[8105] ssc-vm-1552.colo.seagate.com corosyncwarning [CPG   ] downlist left_list: 0 received
[8105] ssc-vm-1552.colo.seagate.com corosyncwarning [CPG   ] downlist left_list: 0 received
[8105] ssc-vm-1552.colo.seagate.com corosyncwarning [CPG   ] downlist left_list: 0 received
Dec 22 15:17:27 [17653] ssc-vm-1552.colo.seagate.com       crmd:     info: pcmk_cpg_membership: Group crmd event 9: node 1 pid 20526 joined via cluster join
Dec 22 15:17:27 [17653] ssc-vm-1552.colo.seagate.com       crmd:     info: pcmk_cpg_membership: Group crmd event 9: ssc-vm-1550.colo.seagate.com (node 1 pid 20526) is member
Dec 22 15:17:27 [17653] ssc-vm-1552.colo.seagate.com       crmd:     info: crm_update_peer_proc:        pcmk_cpg_membership: Node ssc-vm-1550.colo.seagate.com[1] - corosync-cpg is now online
Dec 22 15:17:27 [17653] ssc-vm-1552.colo.seagate.com       crmd:     info: peer_update_callback:        Client ssc-vm-1550.colo.seagate.com/peer now has status [online] (DC=ssc-vm-1558.colo.seagate.com, changed=4000000)
Dec 22 15:17:27 [17653] ssc-vm-1552.colo.seagate.com       crmd:     info: pcmk_cpg_membership: Group crmd event 9: ssc-vm-1552.colo.seagate.com (node 3 pid 17653) is member
Dec 22 15:17:27 [17653] ssc-vm-1552.colo.seagate.com       crmd:     info: pcmk_cpg_membership: Group crmd event 9: ssc-vm-1558.colo.seagate.com (node 4 pid 25503) is member
Dec 22 15:17:27 [17653] ssc-vm-1552.colo.seagate.com       crmd:     info: pcmk_cpg_membership: Group crmd event 10: node 2 pid 13205 joined via cluster join
Dec 22 15:17:27 [17653] ssc-vm-1552.colo.seagate.com       crmd:     info: pcmk_cpg_membership: Group crmd event 10: ssc-vm-1550.colo.seagate.com (node 1 pid 20526) is member
Dec 22 15:17:27 [17653] ssc-vm-1552.colo.seagate.com       crmd:     info: pcmk_cpg_membership: Group crmd event 10: ssc-vm-1551.colo.seagate.com (node 2 pid 13205) is member
Dec 22 15:17:27 [17653] ssc-vm-1552.colo.seagate.com       crmd:     info: crm_update_peer_proc:        pcmk_cpg_membership: Node ssc-vm-1551.colo.seagate.com[2] - corosync-cpg is now online
Dec 22 15:17:27 [17653] ssc-vm-1552.colo.seagate.com       crmd:     info: peer_update_callback:        Client ssc-vm-1551.colo.seagate.com/peer now has status [online] (DC=ssc-vm-1558.colo.seagate.com, changed=4000000)
Dec 22 15:17:27 [17653] ssc-vm-1552.colo.seagate.com       crmd:     info: pcmk_cpg_membership: Group crmd event 10: ssc-vm-1552.colo.seagate.com (node 3 pid 17653) is member
Dec 22 15:17:27 [17653] ssc-vm-1552.colo.seagate.com       crmd:     info: pcmk_cpg_membership: Group crmd event 10: ssc-vm-1558.colo.seagate.com (node 4 pid 25503) is member
Dec 22 15:17:27 [8143] ssc-vm-1552.colo.seagate.com      attrd:     info: pcmk_cpg_membership:  Group attrd event 24: node 1 pid 20524 joined via cluster join
Dec 22 15:17:27 [8141] ssc-vm-1552.colo.seagate.com stonith-ng:     info: pcmk_cpg_membership:  Group stonith-ng event 24: node 1 pid 20522 joined via cluster join
[8105] ssc-vm-1552.colo.seagate.com corosyncnotice  [QUORUM] This node is within the primary component and will provide service.
[8105] ssc-vm-1552.colo.seagate.com corosyncnotice  [QUORUM] Members[4]: 2 4 1 3
[8105] ssc-vm-1552.colo.seagate.com corosyncnotice  [MAIN  ] Completed service synchronization, ready to provide service.

```


<a id="org2b46a25"></a>

## Experiment 4: add dummy stonith resources and repeat experiment 1


<a id="orgeac56dd"></a>

### fence\_dummy.py resource agent will be used to replace real fence agent.


<a id="orga4e41ec"></a>

### Stonith configuration performed:

```bash
# On each node
yum install -y pacemaker-cts

# Provided:
# [root@ssc-vm-1550 ~]# file /usr/share/pacemaker/tests/cts/fence_dummy
# /usr/share/pacemaker/tests/cts/fence_dummy: Python script, ASCII text executable

# On each node
ln -sf /usr/share/pacemaker/tests/cts/fence_dummy /usr/sbin/fence_dummy

# On one cluster node
for i in 1550 1552 1551 1558 ; do pcs stonith create stonith-$i fence_dummy pcmk_host_list=ssc-vm-$i.colo.seagate.com pcmk_host_check=static-list monitor_mode=pass mode=pass; done
for i in 1550 1551 1552 1558 ; do  pcs constraint location stonith-$i avoids ssc-vm-$i.colo.seagate.com; done
pcs property set stonith-enabled=true

```


<a id="org49d1654"></a>

### Stonith configuration testing:

1.  Command to execute

    ```bash
    pcs stonith fence ssc-vm-1552.colo.seagate.com
    ```

2.  Expected behavior

    -   Node becomes OFFLINE in pcs status
    -   Cluster is stopped on the node

3.  Restore cluster to initial state:

    ```bash
    pcs cluster start ssc-vm-1552.colo.seagate.com
    ```


<a id="orgf400b6e"></a>

### Apply iptables rules:

```bash
iptables -A INPUT -s 10.230.242.228 -j DROP && iptables -A INPUT -s 10.230.250.142 -j DROP
```

1.  Observed behavior

    1.  Cluster divided to 2 parts qualified as "partition without quorum" with different pcs status output
    
        1.  Node 1550
        
            ```
            [root@ssc-vm-1550 sbin]# pcs status
            Cluster name: new_cluster
            Stack: corosync
            Current DC: ssc-vm-1550.colo.seagate.com (version 1.1.23-1.el7-9acf116022) - partition WITHOUT quorum
            Last updated: Tue Dec 22 16:55:36 2020
            Last change: Tue Dec 22 16:20:35 2020 by root via cibadmin on ssc-vm-1550.colo.seagate.com
            
            4 nodes configured
            70 resource instances configured
            
            Node ssc-vm-1552.colo.seagate.com: UNCLEAN (offline)
            Node ssc-vm-1558.colo.seagate.com: UNCLEAN (offline)
            Online: [ ssc-vm-1550.colo.seagate.com ssc-vm-1551.colo.seagate.com ]
            
            Full list of resources:
            
             Clone Set: rs-1-clone [rs-1]
                 rs-1       (ocf::heartbeat:Dummy): Started ssc-vm-1558.colo.seagate.com (UNCLEAN)
                 rs-1       (ocf::heartbeat:Dummy): Started ssc-vm-1552.colo.seagate.com (UNCLEAN)
                 Stopped: [ ssc-vm-1550.colo.seagate.com ssc-vm-1551.colo.seagate.com ]
            ```
        
        2.  Node 1552
        
            ```
            [root@ssc-vm-1552 ~]# pcs status
            Cluster name: new_cluster
            Stack: corosync
            Current DC: ssc-vm-1558.colo.seagate.com (version 1.1.23-1.el7-9acf116022) - partition WITHOUT quorum
            Last updated: Tue Dec 22 16:57:25 2020
            Last change: Tue Dec 22 16:20:35 2020 by root via cibadmin on ssc-vm-1550.colo.seagate.com
            
            4 nodes configured
            70 resource instances configured
            
            Node ssc-vm-1550.colo.seagate.com: UNCLEAN (offline)
            Node ssc-vm-1551.colo.seagate.com: UNCLEAN (offline)
            Online: [ ssc-vm-1552.colo.seagate.com ssc-vm-1558.colo.seagate.com ]
            
            Full list of resources:
            
             Clone Set: rs-1-clone [rs-1]
                 rs-1       (ocf::heartbeat:Dummy): Started ssc-vm-1551.colo.seagate.com (UNCLEAN)
                 rs-1       (ocf::heartbeat:Dummy): Started ssc-vm-1550.colo.seagate.com (UNCLEAN)
                 Stopped: [ ssc-vm-1552.colo.seagate.com ssc-vm-1558.colo.seagate.com ]
            ```
    
    2.  Despite the fact that other nodes are considered UNCLEAN due to "stonith-enabled" option, stonith action were not performed - they are missing in corosync.log
    
        Possible explanation for that: parititon without quorum can't serve resources. Stonith resources were stopped along with other resources, thus, making fencing impossible - nobody ask for fencing.  
    
    3.  Called pcs stonith confirm to manually resolve unclean state
    
        ```
        pcs stonith confirm ssc-vm-1558.colo.seagate.com
        pcs stonith confirm ssc-vm-1552.colo.seagate.com
        ```
        
        The state of cluster partition become the same as in Experiment 1 - 1552 and 1558 nodes became OFFLINE, all resources are stopped.  
        
        ```
        [root@ssc-vm-1550 sbin]# pcs status
        Cluster name: new_cluster
        Stack: corosync
        Current DC: ssc-vm-1550.colo.seagate.com (version 1.1.23-1.el7-9acf116022) - partition WITHOUT quorum
        Last updated: Tue Dec 22 17:07:14 2020
        Last change: Tue Dec 22 16:20:35 2020 by root via cibadmin on ssc-vm-1550.colo.seagate.com
        
        4 nodes configured
        70 resource instances configured
        
        Online: [ ssc-vm-1550.colo.seagate.com ssc-vm-1551.colo.seagate.com ]
        OFFLINE: [ ssc-vm-1552.colo.seagate.com ssc-vm-1558.colo.seagate.com ]
        
        Full list of resources:
        
         Clone Set: rs-1-clone [rs-1]
             Stopped: [ ssc-vm-1550.colo.seagate.com ssc-vm-1551.colo.seagate.com ssc-vm-1552.colo.seagate.com ssc-vm-1558.colo.seagate.com ]
        ```


<a id="org48784a4"></a>

## Experiment 5: isolate one node if 5 node cluster


<a id="orgf2c33b2"></a>

### Apply iptables rules:

```bash
iptables -A INPUT -s 10.230.242.228 -j DROP && iptables -A INPUT -s 10.230.250.142 -j DROP
```


<a id="org2d187f8"></a>

### Observed behavior

1.  Cluster divided to 2 parts

    1.  3 nodes partition with quorum where resourses are running
    
        ```
        [root@ssc-vm-1550 sbin]# pcs status
        Cluster name: new_cluster
        Stack: corosync
        Current DC: ssc-vm-1550.colo.seagate.com (version 1.1.23-1.el7-9acf116022) - partition with quorum
        Last updated: Wed Dec 23 16:13:13 2020
        Last change: Wed Dec 23 16:04:02 2020 by root via cibadmin on ssc-vm-1559.colo.seagate.com
        
        5 nodes configured
        87 resource instances configured
        
        Online: [ ssc-vm-1550.colo.seagate.com ssc-vm-1551.colo.seagate.com ssc-vm-1559.colo.seagate.com ]
        OFFLINE: [ ssc-vm-1552.colo.seagate.com ssc-vm-1558.colo.seagate.com ]
        
        Full list of resources:
        
         Clone Set: rs-1-clone [rs-1]
             Started: [ ssc-vm-1550.colo.seagate.com ssc-vm-1551.colo.seagate.com ssc-vm-1559.colo.seagate.com ]
             Stopped: [ ssc-vm-1552.colo.seagate.com ssc-vm-1558.colo.seagate.com ]
        ```
    
    2.  2 nodes partitions without quorum where resources are stopped
    
        ```
        [root@ssc-vm-1552 ~]# pcs status
        Cluster name: new_cluster
        Stack: corosync
        Current DC: ssc-vm-1558.colo.seagate.com (version 1.1.23-1.el7-9acf116022) - partition WITHOUT quorum
        Last updated: Wed Dec 23 16:21:56 2020
        Last change: Wed Dec 23 16:04:02 2020 by root via cibadmin on ssc-vm-1559.colo.seagate.com
        
        5 nodes configured
        87 resource instances configured
        
        Node ssc-vm-1550.colo.seagate.com: UNCLEAN (offline)
        Node ssc-vm-1551.colo.seagate.com: UNCLEAN (offline)
        Node ssc-vm-1559.colo.seagate.com: UNCLEAN (offline)
        Online: [ ssc-vm-1552.colo.seagate.com ssc-vm-1558.colo.seagate.com ]
        
        Full list of resources:
        
         Clone Set: rs-1-clone [rs-1]
             rs-1       (ocf::heartbeat:Dummy): Started ssc-vm-1551.colo.seagate.com (UNCLEAN)
             rs-1       (ocf::heartbeat:Dummy): Started ssc-vm-1550.colo.seagate.com (UNCLEAN)
             rs-1       (ocf::heartbeat:Dummy): Started ssc-vm-1559.colo.seagate.com (UNCLEAN)
             Stopped: [ ssc-vm-1552.colo.seagate.com ssc-vm-1558.colo.seagate.com ]
        ```

2.  Stonith behavior (with fence\_dummy agent)

    1.  Expected behavior:
    
        1.  Nodes 1552 and 1558 are fenced
        
            -   Stonith resources are triggered to fence target nodes
            -   Cluster is stopped on target nodes
            -   Nodes are displayed as OFFLINE in \`pcs status\` output
    
    2.  Actual behavior
    
        -   Stonith resources were triggered to fence target nodes  
            
            ```
            Dec 23 16:12:36 [19203] ssc-vm-1550.colo.seagate.com       crmd:   notice: te_fence_node:       Requesting fencing (reboot) of node ssc-vm-1552.colo.seagate.com | action=2 timeout=60000
            Dec 23 16:12:36 [19203] ssc-vm-1550.colo.seagate.com       crmd:   notice: te_fence_node:       Requesting fencing (reboot) of node ssc-vm-1558.colo.seagate.com | action=1 timeout=60000
            ...
            Dec 23 16:12:36 [19198] ssc-vm-1550.colo.seagate.com stonith-ng:   notice: can_fence_host_with_device:  stonith-1552 can fence (reboot) ssc-vm-1552.colo.seagate.com: static-list
            ...
            Dec 23 16:12:36 [19198] ssc-vm-1550.colo.seagate.com stonith-ng:   notice: can_fence_host_with_device:  stonith-1558 can fence (reboot) ssc-vm-1558.colo.seagate.com: static-list
            ...
            Dec 23 16:12:36 [19203] ssc-vm-1550.colo.seagate.com       crmd:   notice: tengine_stonith_notify:      Peer ssc-vm-1552.colo.seagate.com was terminated (reboot) by ssc-vm-1551.colo.seagate.com on behalf of crmd.19203: OK | initiator=ssc-vm-1550.colo.seagate.com ref=fc2d39d2-5068-4484-9b80-dd998cb1ec1b
            ...
            Dec 23 16:12:36 [19203] ssc-vm-1550.colo.seagate.com       crmd:   notice: tengine_stonith_notify:      Peer ssc-vm-1558.colo.seagate.com was terminated (reboot) by ssc-vm-1551.colo.seagate.com on behalf of crmd.19203: OK | initiator=ssc-vm-1550.colo.seagate.com ref=01227f64-b797-4e78-9688-4e131536b136
            ```
        -   Cluster was not stopped on target nodes
        -   Nodes were displayed as OFFLINE in \`pcs status\` output
    
    3.  Analysis
    
        -   The expectation that cluster shall be stopped was based on experiment where \`pcs stonith fence <node>\` command was called (using fence\_dummy agent).
        -   There was no networking issues (artificial/natural). That may be the key reason why cluster became stopped on target node.
        -   So, probably expectations regarding fence\_dummy behavior were not correct. It doesn't stop the cluster. And with normal fence agent node is going to be fenced properly.


<a id="orgb09a0cb"></a>

## Summary:

-   Network issues that breaks corosync communications divided cluser to 2 parts.
-   In case 4-node cluster both parts didn't have quorum.
-   In case 5-node cluster 3-node quorum was preserved.
-   Cluster partition without quorum can't run any resources including stonith resources.
-   Cluster partition without quorum displays quorum-complete nodes as unclean (offline)
-   Node fencing decisions (and actions) are possible only in cluster with quorum.
-   Cluster partition with quorum displays quorum-incomplete nodes as offline after fencing action is triggered.
