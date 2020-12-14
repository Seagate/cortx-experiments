# 16-node pacemaker cluster experiments

Purposes:
1. Understand whether Pacemaker can successfully handle the cluster of 16 nodes.
2. Estimate approximated network traffic consumption.
3. Try to find out possible bottlenecks.

Plan:
1. Create 16-nodes VM-based cluster in Pacemaker. Each node separate virtual machine.
2. Create N resources of different types.
3. Measure network load during usual cluster operations.
4. Measure timings for usual cluster operations.

**Usual cluster operations** are:
* Failover/failback due to node "disappearance" (reboot).
* Cluster start.
* Cluster stop.

## Approach

Each resources is represented with Dummy OCF resource agent.  
nload tool is used to measure network traffic consumption.  
Delays for interactive operations are measured by `time` command in conjunction with `/vac/log/cluster/corosync.log` timings analysis.

## Cluster 16 x 16 unique resources + 5 clones: 336 resources in summary

Setup with big amount of normal (unique) resources with location constraints to have exactly 16 normal resources on each of 16 nodes.

### Network consumption:

#### Max/min numbers:

* For node where pcs command was running:
  - Max incoming: 9.81 Mbit/s
  - Max outgoing: 25.80 Mbit/s
* For other nodes:
  - Max incoming: 3.29 Mbit/s
  - Max outgoing: 1.50 Mbit/s

#### Delete resources

* Peaks up to 900 kBit/s per resource deletion operation for both Input and Output for node where pcs command is running
* Peaks up to 100 kBit/s per resource deletion operation for both Input and Output on other node

####  Adding 256 resources: 16 rcs per 16 nodes with "prefers" location constraint for each node

* Peaks up to 6 MBit/s of outgoing traffic for node where pcs command is running
* Peaks up to 1 MBit/s of incoming/outgoing traffic for all other cases.
* The same numbers are valid for failover operation when node is reboot.

### Timings

#### Adding 256 resources: 16 rcs per 16 nodes with "prefers" location constraint for each node

* Overall time:  29 min 6 sec.
  - Start: Dec 09 13:07:08
  - Finish: Dec 09 13:36:14
* Time to create last resource: 8 sec
  - Start: Dec 09 13:36:03
  - Finish: Dec 09 13:36:11
* Time to create location constraints for last resource: 2 sec
   - Start: Dec 09 13:36:12
   - Finish: Dec 09 13:36:14
* Time to execute pcs status: 0m 5.112s
* Overall time to delete 96 resources: 48m45.112s

## Cluster 10 x 16 unique resources + 5 clones. 240 resources in summary

This setup is intended to represent "normal" configuration from the point of number of resources.

### Timings

* Time to stop entire cluster: 0 min 16.542 sec
* Time to start cluster: 2 min 20 sec
  - pcs status command time: 5 sec. Depends on number of nodes.
  - Start: after Wed Dec  9 14:50:04 MST 2020
  - Finish: 14:52:24


### Network consumption

* Peak values for incoming/outgoing traffic during cluster start: ~ 31 MBit/s

#### pcs operations: add/delete/failover/failback

* For node where pcs command was running:
  - Max incoming: 9.81 Mbit/s
  - Max outgoing: 25.80 Mbit/s

* For other nodes:
  - Max incoming: 3.29 Mbit/s
  - Max outgoing: 1.50 Mbit/s


## Cluster with 24 clones resources which consist of 24 * 16 = 384 resources

### Timings

* Time to create 24 clones resulting in 384 resources: 11 sec according to time command 
  - In corosync logs: 13 sec 
  - Start: 16:17:03 
  - Finish: 16:17:16 
* Time to stop the cluster: 9 sec
* Time to start the cluster: 6 sec
  - In corosync logs: 32 sec 
  - Start: 16:36:26 
  - Finish: 16:36:58 

### Network traffic consumption

* Peaks up to 45 Mbit/s for both incoming/outgoing traffic during cluster startup
* Average value for cluster startup: 3 Mbit/s
* Node reboot: 1 second to handle.
  There is no surprise here since for clone resources it just a matter of stop operation timings.  
  Number of nodes and resource does not affect performance.  
* Resource disable: 1 second to handle.  
  Also no surprise. Just an indication that clone resources are not affected.

#### Some experiments

Added ordering constraint for each clone forming linear sequence. Interleave is disabled. 
Ordering Constraints:  
```
  Resource Sets:
    set rs-1-clone rs-2-clone rs-3-clone rs-4-clone rs-5-clone rs-6-clone rs-7-clone rs-8-clone rs-9-clone rs-10-clone rs-11-clone rs-12-clone rs-13-clone rs-14-clone rs-15-clone rs-16-clone rs-17-clone rs-18-clone rs-19-clone rs-20-clone rs-21-clone rs-22-clone rs-23-clone rs-24-clone action=start (id:pcs_rsc_set_rs-1-clone_rs-2-clone_rs-3-clone_rs-4-clone_rs-5-clone_rs-6-clone_rs-7-clone_rs-8-clone_rs-9-clone_rs-10-clone_rs-11-clone_rs-12-clone_rs-13-clone_rs-14-clone_rs-15-clone_rs-16-clone_rs-17-clone_rs-18-clone_rs-19-clone_rs-20-clone_rs-21-clone_rs-22-clone_rs-23-clone_rs-24-clone) (id:clones-start-order-1)
```

Observations:
* Node reboot does not cause any changes when node is lost.
* When node is connected to cluster again all ordered resources are being restarted. It takes some time. Consider that Dummy resources are stopped immediately without time efforts.
  - In corosync logs: 24 sec.
  - Start: 17:04:18
  - Finish: 17:04:32
* Assuming that resources will take some time to restart it is quite a delay. However if interleave option is enabled - only local copy of clone resources will be required to proceed. In current test no resources were restarted except local copies on rebooted node.


## Summary & Results

* 16-node cluster have been created
* Network consumption does not exceed Cortx HW capabilities
* With big amount of nodes clone resources with interleave option enabled provide the best performance.
