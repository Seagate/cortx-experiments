## Purposes:
1. Verify pcs cluster supports upto 36 nodes.
2. Validate pcs cluster is stable with 36 nodes.

## Experiments:
1. Add nodes up to 36 verify corosync limit and add remote nodes once it exceed corosync limit.
2. Configure the dummy resources with the dependency.
3. Measure network traffic.
4. Perform the basic pcs command and verify the stability of the cluster.
5. Tune cluster property to support large cluster and measure impact on the network traffic and cluster stability.

## Results
- cluster can scale upto 36 nodes with some tuning.

