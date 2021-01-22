### Conceptual Overview

- A regular pacemaker cluster with communication using corosync can be extended up to 32 nodes. With the pacemaker_remote service, High Availability clusters can be extended to include additional nodes beyond this limit.
- The pacemaker_remote service can be operated as a physical node (remote node) or as a virtual node (guest node). Unlike normal cluster nodes, both remote and guest nodes are managed by the cluster as resources.
- From the resource management point of view, they behave as regular cluster nodes.
- Remote nodes do not need to have the full cluster stack installed, as they only run the pacemaker_remote service. The service acts as a proxy, allowing the cluster stack on the“regular”cluster nodes to connect to the service.

### Terminology
###### **Cluster Node**: A node that runs the complete cluster stack.
A regular cluster node can perform following:
- Run cluster resources.
- Run all command line tools, such as crm , crm_mon.
- Execute fencing actions.
- Count toward cluster quorum.
- Serve as the designated coordinator (DC).

###### **Pacemaker Remote (systemd service: pacemaker_remote )**
- A service daemon that makes it possible to use a node as a Pacemaker node without deploying the full cluster stack.

###### **Remote Node: A physical machine that runs the pacemaker_remote daemon**
- A special resource( ocf:pacemaker:remote ) needs to run on one of the cluster nodes to manage communication between the cluster node and the remote node.
A remote node is different from cluster node:
- Can not be counted in cluster quorum.
- Can not be served as the designated coordinator(DC).
- Will be managed by cluster only if gets added as a resource in the cluster.

On the other side, Remote node can perform following same as cluster node:
- Run cluster resources.
- Run all command line tools, such as crm , crm_mon.
- Execute fencing actions.

### Configuartion Highlights
***1. Cluster Node:***
- Full corosync and pacemaker stack deployment
- IP and remote name entry for each remote node in hosts file
   Ex: 192.168.49.38 remote1
- Verify remote connection using:  $ ssh -p 3121 remote_name
   Ex: $ ssh -p 3121 remote1
  ** ssh_exhange_identification: read: Connection reset by peer. This specifies your setup is good.**
- create a new authkey in /etc/pacemaker directory for pacemeker_remote communication and copy on all other cluster and remote nodes for consistent communication overall.
$ sudo dd if=/dev/urandom of=/etc/pacemaker/authkey bs=4096 count=1

***2. Remote Node:***
- Only pacemaker_remote service installation.
- Open port 3121 for pacemaker_remote

### Test Cases and its result
***1. Create a clone resource and check whether it gets started automatically with new remote node addition.***
Result:- Successfully Verified.
***2. Shut Down some/all remote nodes and check whether resources gets switched to other cluster/remote nodes.***
Result:- Successfully Verified.
***3. Stop pacemaker_remote service and document the observation.***
Result:- pacemaker_remote will be quickly started by systemd. If the failure is not recoverable, remote node gets stopped and also cloned resources on that remote will be stopped. Other resources running on that remote will be switched to other node.
***4. How Dynamic addition of a remote node will happen.***
Explanation: Remote can be successfully added to the cluster assuming there is an IP to host mapping in the hosts file. So, we can directly modify the hosts file. And change will be in effect without restarting the system or any service. OR you can directly create the remote resource with hostname of the remote.
***5. Create the Active-passive resource such that one of the active resource is running on one of the remote and shutdown the remote and after some time, bring back the remote node and document the result.***
Result: resource running on that remote shifted to other cluster node. Now, after remote is back, initial trail took 15 mins for a cluster to populate and identify remote up case. So, after experiment, created the remote resource with some meta attributes. For eg: failure-timeout=200s and cluster-recheck-interval=120s. With this configuration, resource start operation was getting triggered at every 2 to 3 minutes of interval.And when resource was UP, it was automatically started by pacemaker after above defined interval.
