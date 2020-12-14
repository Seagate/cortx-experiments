# POC: Scale cluster adding more nodes

## Purpose

* Describe process and required cluster management commands
* Define points for additional configuration in case of...:
  - Special domain names usage
  - Network redundancy
  - Service discovery
  - Opt-in cluster ("symmetric-cluster" option is false)

## Add node to the cluster

Prerequisites:  
* Pacemaker is installed on new node.
* pcsd systemd service is started and enabled.
* hacluster user is created and known password is set for it.

Steps:

1. Authorize new nodes entering password for hacluster user
```
pcs cluster auth <node...>
```

2. Add node to existing cluster:
```
pcs cluster node add <node> --start --enable
```
`--start` and `--enable` are optional here depending on intention to start cluster immediately and make this setting persistent for further bootloads.

Note: For RRP-enabled cluster the <node> consists of ring 0 address followed by a ',' and then the ring 1 address.

3. Apply location constraints for unique resources depending on cluster type (Opt-in/Opt-out).

In Opt-out cluster all resources can run on any node. Location constrains are used to prevent chosen resources from running on specific nodes. If new node is not supposed to host some resources following constraint shall be added:
```
pcs constraint location <resource-name> avoids <new-node>
```

In Opt-in cluster, on the opposite,  all resources are prohibited to run anywhere. Location constraints shall be added to permit chosen resources to be started on new node.
```
pcs constraint location <resource-name> prefers <new-node>
```

Note: these examples add INFINITY scored constraints, but finite scores are also possible.

Whether cluster Opt-in or Opt-out depends on the value of `simmetric-cluster` property.

`resource-discovery` option in location constraint defines whether probe operation shall be executed. Depending on the cluster configuration such type of constraint may have to be applied for new node.

Example to make resource Dummy start possible only on node-1 and node-2:
```
pcs constraint location add <constraint-id> Dummy node-1 <score> resource-discovery=exclusive
pcs constraint location add <constraint-id> Dummy node-2 <score> resource-discovery=exclusive
```
Note 1: `resource-discovery` option controls only possibility of probe operation. What really affects placement logic is `score` - scores can be configured in such a way that only node-1 will normally host Dummy resource.
Note 2: for clone resources add `-clone` suffix to resource ID.

4. Fencing configuration.

A fencing device for new node shall be explicitly created. Such configuration highly depends on chosen fencing devices, so generic example is given:

```
pcs stonith create <stonith-device-name> <fence-agent> <fence-agent-attributes> op monitor interval=30s
```


## Additional configuration cases

### Special domain names are used

Example: srvnode-1 instead of ssc-vm.colo.seagate.com

DNS server configuration or `/etc/hosts` file have to be updated with a record for new node.


### Service discovery for clone resources

#### Node attribute

Resource discovery can be disabled on the cluster node. This is controlled via `resource-discovery-enabled` node-attribute. By default it is set to `true`.  
To verify whether this attribute is set, run the following command:
```
pcs node attribute --name resource-discovery-enabled
```
Empty output means that attributes on all nodes are set in default values.  
In general the usage of this attribute is not recommended. However if it is used and resource discovery shall be disabled for new node the following command shall be executed:
```
pcs node attribute <node-id> resource-discovery=enabled=false
```
Normally location constraints are used to select where resource shall be started.
