# 36 Node pacemaker cluster experiments

Cluster stability Summary:
-   Increases open file limit.

```bash
# login
$ echo '*    -    nofile    1048576' > /etc/security/limits.d/transmission.conf
$systemctl daemon-reload

# logout and login again
$ ulimit -a | grep "open files"
open files                      (-n) 1048576
```

-   Increases Pacemaker Buffer

```bash
# Update /etc/sysconfig/pacemaker before starting cluster
PCMK_ipc_buffer=19725604
```

-   standby/unstandby: Move 3 nodes to standby/unstandby at a time once those are done with no active resources then move to the next 3 nodes.
-   cluster-ipc-limit
    *   Default value of the cluster-ipc-limit is 500 and recommanded is the number of resources in the cluster multiplied by the number of nodes.
    *   We tried cluster-ipc-limit 10000 when cluster has 36 nodes and 600 resources

  ```bash
  pcs property set cluster-ipc-limit=10000
  ```

-   interleave
    *   It is clone property used in cloning useful for order.
    *   If we want to limit order of resources to same node use this.
    *   Please refer below link for the more information
  [Clone options link](https://clusterlabs.org/pacemaker/doc/en-US/Pacemaker/1.1/html/Pacemaker_Explained/_clone_options.html)

```bash
pcs resource create hax clone interleave=true
```

-   Scaling/Adding resources
    *   Best way is to create resource with minimum node then add nodes to scale the cluster.
    *   When we create resource with 36 node then network traffics/cpu usage increases quickly. To avoid this problem use below step.
  **How to create/start resources in cluster:**

  ```bash
  # Create cib file
  $ pcs cluster cib cortx-pcs.xml

  # Put one node in standby
  $ pcs -f cortx-pcs.xml cluster standby srvnode-1

  # Add resources
  $ pcs -f cortx-pcs.xml resource create myres ocf:heartbeat:Dummy clone

  # Add nodes but do not start them
  $ pcs -f cortx-pcs.xml cluster node add srvnode-2 --enable
  $ pcs -f cortx-pcs.xml cluster node add srvnode-3 --enable

  # Verify and push file
  $ pcs cluster verify -V cortx-pcs.xml
  $ pcs cluster cib-push cortx-pcs.xml

  # Now unstandby srvnode-1 and start other newly added nodes in a group
  $ pcs cluster unstandby srvnode-1
  $ pcs cluster start srvnode-2
  $ pcs cluster start srvnode-3
  ```

-   System Utilization (ram/cpu/network)
    *   DC node will use high utilization as it will act as leader and responsible for action.
    *   Resource utilization depends on number of nodes and resources.
    *   Standby 3 nodes will have less utilization but standby all nodes will have high utilization.

-   Update clone size dynamically while scaling the cluster
    *   Dynamically change in the clone size is allowed in the pcs cluster and this is needed while scaling the cluster for services like motr and s3.
    *   We performed experiment mentioned in the example and able to modify clone-max and clone-node-max count.

  ```bash
  # Example
  # Create resource with clone-max=10 and clone-node-max=2
  $ pcs resource create motr ocf:seagate:s3server service=motr unique_clone=true clone clone-max=10 clone-node-max=2 globally-unique=true

  # Modify clone-max number later after scaling the cluster
  $ pcs resource update motr-clone meta clone-max=20 clone-node-max=2
  ```

Outcome:

## 1. Add nodes up to 36 verify corosync limit
-   Able to create 36 nodes cluster with 32 normal nodes and 4 remote nodes.
-   We created scripts to create 36 nodes cluster and already shared in the scripts dir.

## 2. Configure the dummy resources with the dependency
-   Configured around 618 resources with the dependecy in the cluster and observed that pcs cluster became unstable.
-   We observed from corosync logs, PCMK_ipc_buffer has exceeded buffer limit and also saw some bad file descriptor related errors.
-   We tunned some parameters to make cluster stable. Please find details in tunning section.
-   Check PCS Output after configuring the resources (`check pcs_status.txt`)

## 3. Cluster tunning details

Below issue observed after scaling cluster and configuring resources
-   PCMK_ipc_buffer exceeded
-   Bad file descriptor related errors

**Tunning performed**
1.  IPC buffer limit
-   Increased IPC buffer limit (PCMK_ipc_buffer=19725604)
-   IPC buffer is the size of message used by corosync for heartbeat communication.

2.  Open file limit
-   Increased open file limit to 1048575 (ulimit -n 1048575)
-   We observed bad file descriptor errors in the corosync logs and did above change to fix the issue.

3.  Batch-limit
-   Batch-limit is the maximum number of actions that the cluster may execute in parallel across all nodes. The "correct" value will depend on the speed and load of your network and cluster nodes. If zero, the cluster will impose a dynamically calculated limit only when any node has high load.
-   We tried 25 fixed batch-limit instead of dynamic limit and observed that network increased upto 345 Mbits/s and due to high CPU usage DC node got also changes. We also observed that some resources got time-out during unstandby nodes operation.
-   We reverted batch-limit to zero and network load back to normal. So, We concluded batch-limit zero is suitable for large cluster.

4.  cluster-ipc-limit
-   CLuster-ipc-limit is the maximum IPC message backlog before one cluster daemon will disconnect another. This is of use in large clusters, for which a good value is the number of resources in the cluster multiplied by the number of nodes. The default of 500 is also the minimum. Raise this if you see "Evicting client" messages for cluster daemon PIDs in the logs.
-   We tried 10000 cluster-ipc-limit but not seen much improvement in the cluster.
-   As per corosync guide this cluster property is useful for large sized cluster and recommanded value is ( Number of Nodes * Resources count )

[All cluster option link](https://clusterlabs.org/pacemaker/doc/en-US/Pacemaker/1.1/html/Pacemaker_Explained/s-cluster-options.html)

## 4. Cluster status alternative
-   We observed that "pcs status" command is taking bit more time around 10 sec to 13 sec for the execution.
-   We figured out some other alternatives to get nodes and resources status which are much faster than "pcs status".

```bash
  # Alternative commands to get node status
  $ pcs status nodes # Returns the status of all the nodes including remote nodes which are present in the cluster. It took around 1-2 secs for the execution.

  # Alternative command to get resource status
  $ pcs resource # Returns the resource status of the cluster. It took around 1-2 secs for the execution.
```

## 5. Nodes standby/Unstandby operation

1.  pcs cluster standby/unstandby --all
-   We observed pretty much high traffic max 90 Mbits/s on the network when we performed the standby/unstandby for all the nodes of the cluster.
-   Also observed that some services failed due to timeout.

Solution:
-   We increased stop/start timeout from 20 sec to 50 sec but it did not help to fix the issue.
-   We divided all the nodes in the gorup of three and moved 3 nodes to standby/unstandby at a time once those are done with no active resources then move to the next 3 nodes. These solution went well and all the services stopped and started succesfully
-   We used below scripts to automate above operations

```bash 
scripts/standby.sh
scripts/unstandby.sh
```

## 6. Network traffic

1.  Normal traffic after tunning
-   Avg 16-17 kbits/s
-   Max 1-2 Mbits/s

2.  Standby/Unstandby after tunning with all nodes at once
-   Avg 3-4 Mbits/s
-   Max 92 Mbits/s

3.  Standby/Unstandby after tunning with group of 3 nodes
-   Avg 1-3 Mbits/s
-   Max 7-12 Mbits/s
