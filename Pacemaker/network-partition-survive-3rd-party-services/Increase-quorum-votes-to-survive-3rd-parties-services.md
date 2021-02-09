#Problem

If Cortx cluster is partitioned, pacemaker will have two types of partitions -

1. Partition with quorum
2. Partition without quorum

If majority of nodes running 3rd party services are part of partition without quorum, none of the partitions will be functional as 3rd party services will not be available in the partition with quorum.

#Solution

The solution lies in the algorithm which is used for deciding the quorum votes. Currently every node has single vote so every node is treated equally. But a node running 3rd party services should have higher votes in deciding the quorum.

There a tool called **corosync-quorumtool** can be used to increase quorum vote of the specific node.

**corosync-quorumtool** - Display the current state of quorum in the cluster and set vote quorum options.

```
[root@ssc-vm-c-1713 677029]# corosync-quorumtool -h
usage:
corosync-quorumtool <options>

  options:

  -s             show quorum status
  -m             constantly monitor quorum status
  -l             list nodes
  -a             show all names or addresses for each node
  -p             when used with -s or -l, generates machine parsable output
  -v <votes>     change the number of votes for a node (*)
  -n <nodeid>    optional nodeid of node for -v
  -e <expected>  change expected votes for the cluster (*)
  -H             show nodeids in hexadecimal rather than decimal
  -i             show node IP addresses instead of the resolved name
  -o <a|n|i>     order by [a] IP address (default), [n] name, [i] nodeid
  -f             forcefully unregister a quorum device *DANGEROUS* (*)
  -h             show this help text
  -V             show version and exit

  (*) Starred items only work if votequorum is the quorum provider for corosync

```

##Experiment: Change quorum vote of the node using corosync-quorum tool

1. Created cluster with the 5 nodes and configured dummy clone resource

    ```
    [root@ssc-vm-c-1885 677029]# pcs status
    Cluster name: hacluster
    Stack: corosync
    Current DC: srvnode-1 (version 1.1.23-1.el7-9acf116022) - partition with quorum
    Last updated: Thu Feb  4 23:29:36 2021
    Last change: Thu Feb  4 22:50:35 2021 by root via cibadmin on srvnode-55 nodes configured
    6 resource instances configured
    Online: [ srvnode-1 srvnode-2 srvnode-3 srvnode-4 srvnode-5 ]
    Full list of resources: Clone Set: dummy_clone-clone [dummy_clone]
        Started: [ srvnode-1 srvnode-2 srvnode-3 srvnode-4 srvnode-5 ]
    dummy_third_party      (ocf::heartbeat:Dummy): Started srvnode-5Daemon Status:
    corosync: active/enabled
    pacemaker: active/enabled
    pcsd: active/enabled
    ```

2. Modified quorum vote of the srvnode-5 from srvnode-1

```bash
corosync-quorumtool -v 5 -n 5
```

Quorum settings after changing the quorum votes of the specific nodes

    ```
    [root@ssc-vm-c-1884 677029]# corosync-quorumtool
    Quorum information
    ------------------
    Date:             Fri Feb  5 01:22:24 2021
    Quorum provider:  corosync_votequorum
    Nodes:            5
    Node ID:          5
    Ring ID:          3/10554
    Quorate:          YesVotequorum information
    ----------------------
    Expected votes:   9
    Highest expected: 9
    Total votes:      9
    Quorum:           5
    Flags:            QuorateMembership information
    ----------------------
        Nodeid      Votes Name
            3          1 srvnode-3
            1          1 srvnode-1
            5          5 srvnode-5 (local)
            4          1 srvnode-4
            2          1 srvnode-2
    ```

3. Isolated srvnode-5 from the other nodes using the iptable command

```bash
iptables -A INPUT -s srvnode-1 -j DROP && iptables -A INPUT -s srvnode-2 -j DROP && iptables -A INPUT -s srvnode-3 -j DROP && iptables -A INPUT -s srvnode-4 -j DROP
```

#Results

1. pcs status on the srvnode-5

    ```
    [root@ssc-vm-c-1884 677029]# pcs status
    Cluster name: hacluster
    Stack: corosync
    Current DC: srvnode-5 (version 1.1.23-1.el7-9acf116022) - partition with quorum
    Last updated: Fri Feb  5 01:26:13 2021
    Last change: Thu Feb  4 22:50:35 2021 by root via cibadmin on srvnode-55 nodes configured
    6 resource instances configured
    Online: [ srvnode-5 ]
    OFFLINE: [ srvnode-1 srvnode-2 srvnode-3 srvnode-4 ]
    Full list of resources: Clone Set: dummy_clone-clone [dummy_clone]
        Started: [ srvnode-5 ]
        Stopped: [ srvnode-1 srvnode-2 srvnode-3 srvnode-4 ]
    dummy_third_party      (ocf::heartbeat:Dummy): Started srvnode-5Daemon Status:
    corosync: active/enabled
    pacemaker: active/enabled
    pcsd: active/enabled
    ```

- Observed partition with quorum on the srvnode-5 as it has more than half quorum votes from the total quorum votes.

2. pcs status on the other nodes

    ```
    [root@ssc-vm-c-1885 677029]# pcs status
    Cluster name: hacluster
    Stack: corosync
    Current DC: srvnode-2 (version 1.1.23-1.el7-9acf116022) - partition WITHOUT quorum
    Last updated: Fri Feb  5 01:40:06 2021
    Last change: Thu Feb  4 22:50:35 2021 by root via cibadmin on srvnode-55 nodes configured
    6 resource instances configured 
    Online: [ srvnode-1 srvnode-2 srvnode-3 srvnode-4 ]
    OFFLINE: [ srvnode-5 ]
    Full list of resources: Clone Set: dummy_clone-clone [dummy_clone]
        Stopped: [ srvnode-1 srvnode-2 srvnode-3 srvnode-4 srvnode-5 ]
    dummy_third_party      (ocf::heartbeat:Dummy): StoppedDaemon Status:
    corosync: active/enabled
    pacemaker: active/enabled
    pcsd: active/enabled
    ```

- Observed partition without quorum on all other nodes as their quorum votes are less than total expected votes

#Conclusion

- From the above experiment, It looks like it's possible to modify the quorum vote of the specific node using corosync-quorum tool and quorum votes can play a important role to survive 3rd parties services during network partition.