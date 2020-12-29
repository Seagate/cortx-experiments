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
- A special resource( ocf:pacemaker:remote ) needs to run on one of the cluster nodes to manage communication between the cluster node and the remote node

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
