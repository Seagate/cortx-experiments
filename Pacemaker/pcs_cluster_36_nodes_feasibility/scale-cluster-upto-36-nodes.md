# 36 Node pacemaker cluster experiments

Tunning Summery:
- Increases open file limit.
```
# login
$ echo '*    -    nofile    1048576' > /etc/security/limits.d/transmission.conf
$systemctl daemon-reload

# logout and login again
$ ulimit -a | grep "open files"
open files                      (-n) 1048576
```
- Increases Pacemaker Buffer
```
# Update /etc/sysconfig/pacemaker before starting cluster
PCMK_ipc_buffer=19725604
```
- standby/unstandby: For this standby/unstandby nodes 3 at a time instead successfully before moving to next 3.

Outcome:

## 1. Add nodes up to 36 verify corosync limit
- Able to create 36 nodes cluster with 32 normal nodes and 4 remote nodes.
- We created below scripts to create cluster, add normal and remote nodes.
config.sh

## 2. Configure the dummy resources with the dependency
- Configured around 603 resource with the dependecy in the cluster and observed that pcs cluster became unstable. We observed from corosync logs, PCMK_ipc_buffer has exceeded buffer limit and also saw some bad file descriptor related errors.

Solution: We tried below solution and able to get rid of from those errors.
        i. Increased IPC buffer limit (PCMK_ipc_buffer=19725604)
        ii. Increased open file limit to 1048575 (ulimit -n 1048575)

Check PCS Output after configuring the resources (`check pcs_status.txt`)

## 3. Measure network traffic

Without any operation network traffic

```
Incoming:
        Curr: 1.54 kBit/s
        Avg: 2.74 kBit/s
        Min: 472.00 Bit/s
        Max: 40.59 kBit/s
        Ttl: 2.60 GByte
Outgoing:
        Curr: 328.00 Bit/s
        Avg: 3.04 kBit/s
        Min: 0.00 Bit/s
        Max: 44.96 kBit/s
        Ttl: 4.07 GByte
```

Moving two nodes into standby mode

```
Incoming:
        Curr: 2.84 kBit/s
        Avg: 9.14 kBit/s
        Min: 472.00 Bit/s
        Max: 1.33 MBit/s
        Ttl: 2.60 GByte
Outgoing:
        Curr: 0.00 Bit/s
        Avg: 16.82 kBit/s
        Min: 0.00 Bit/s
        Max: 2.23 MBit/s
        Ttl: 4.07 GByte
```

Moving two nodes into unstandby mode

```
Incoming:
        Curr: 10.36 kBit/s
        Avg: 17.29 kBit/s
        Min: 472.00 Bit/s
        Max: 401.16 kBit/s
        Ttl: 2.60 GByte
Outgoing:
        Curr: 18.60 kBit/s
        Avg: 81.29 kBit/s
        Min: 0.00 Bit/s
        Max: 1.80 MBit/s
        Ttl: 4.07 GByte
```

## 4. Performs the basic pcs command and verify the stability of the cluster
   i. pcs status
    - We observed that "pcs status" command is taking bit more time around 10 sec to 13 sec for the execution.
    - We figured out some other alternatives to get nodes and resources status which are much faster than "pcs status".
        i. pcs status nodes -> Returns the status of all the nodes including remote nodes which are present in the cluster. It took around 1-2 secs for the execution.
        ii. pcs resource -> Returns the resource status of the cluster. It took around 1-2 secs for the execution.

    ii. pcs cluster standby --all
    - We observed pretty much high traffic around XX Mbps on the network when we perform the standby for all the nodes of the cluster.
    - Also observed that some services failed due to timeout.

    Solution:
    - We increased stop/start timeout from 20 sec to 50 sec but it did not help to fix the issue.
    - We divided all the nodes in the group of three and performed granularly standby like move to next 3 nodes once all the resounces of the first three nodes move to stopped state and it went well. All the services stopped properly.
    - We used below script to automate the operations.

    iii. pcs cluster unstandby --all
    - We observed same behaviour like standby operation. We divided nodes in the group and able to performs unstandby operation succesfully.

## 5. Tune cluster property to support large cluster and measure impact on the network traffic and cluster stability
    - We tuned below property to see impact on the cluster performance.

**Batch-limit** - The maximum number of actions that the cluster may execute in parallel across all nodes. The "correct" value will depend on the speed and load of your network and cluster nodes. If zero, the cluster will impose a dynamically calculated limit only when any node has high load.

**cluster-ipc-limit** - 500	The maximum IPC message backlog before one cluster daemon will disconnect another. This is of use in large clusters, for which a good value is the number of resources in the cluster multiplied by the number of nodes. The default of 500 is also the minimum. Raise this if you see "Evicting client" messages for cluster daemon PIDs in the logs.

    i. Batch-limit - 0 and cluster-ipc-limit - 500
    - Outgoing traffic - 1.43 MBit/s Avg, 5.87 MBit/s Max
    - Incoming traffic - 219.55 kBit/s Avg, 1.77 MBit/s Max

    ii Batch-limit - 25 and cluster-ipc-limit - 10000
    - Outgoing traffic - 725.84 kBit/s Avg, 347.45 MBit/s Max
    - Incoming traffic - 1.14 MBit/s Avg, 47.00 MBit/s Max

    - Observed some services got failed during granularly unstandby operation.

    iii. Batch-limit - 0 and cluster-ipc-limit - 10000
    - Outgoing traffic - 627.52 kBit/s Avg, 6.25 MBit/s Max
    - Incoming traffic - 134.63 kBit/s Avg, 1.40 MBit/s Max
