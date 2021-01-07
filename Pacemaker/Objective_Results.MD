## Purposes:
1. Verify pcs cluster supports upto 36 nodes.
2. Validate pcs cluster is stable with 36 nodes.

## Experiments:
1. Add nodes up to 36 verify corosync limit and add remote nodes once it exceed corosync limit.
2. Configure the dummy resources with the dependency.
3. Measure network traffic.
4. Performs the basic pcs command and verify the stability of the cluster.
5. Tune cluster property to support large cluster and measure impact on the network traffic and cluster stability.

## Results
- cluster is possible with 36 node with some tuning.
- Network traffic depend on action to be done on no. of node. Max usage see upto 90 to 120 MB. Avg is low as 50 to 150 kb.
    - If try to stop/start all node at one time then take lot of traffic and cpu utilization.
    - If stop/starting node 3 at time the traffic is low upto 2 MB avg and 16 MB max.
