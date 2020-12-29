
# Clone Options

- clone-max
  - How many copies of the resource to start. Defaults to the number of nodes in the cluster.

- clone-node-max
  - How many copies of the resource can be started on a single node; the default value is 1.

- clone-min
  - The number of instances that must be running before any dependent resources can run. This parameter can be of particular use for services behind a virtual IP and HAProxy, such as is often required for an OpenStack platform.

- notify
  - When stopping or starting a copy of the clone, tell all the other copies beforehand and when the action was successful. Allowed values: false, true. The default value is false.

- globally-unique
  - Does each copy of the clone perform a different function? Allowed values: false, true
  - If the value of this option is false, these resources behave identically everywhere they are running and thus there can be only one copy of the clone active per machine.
  - If the value of this option is true, a copy of the clone running on one machine is not equivalent to another instance, whether that instance is running on another node or on the same node. The default value is true if the value of clone-node-max is greater than one; otherwise the default value is false.

- ordered
  - Should the copies be started in series (instead of in parallel). Allowed values: false, true. The default value is false.

- interleave
  - Changes the behavior of ordering constraints (between clones/masters) so that copies of the first clone can start or stop as soon as the copy on the same node of the second clone has started or stopped (rather than waiting until every instance of the second clone has started or stopped). Allowed values: false, true. The default value is false.

# constraint

- location:
    - prefers, avoid for normal case like allow/not allow resource on current node even if other node not available.
    - complex: `constraint location csm-kibana rule score=-INFINITY '#uname' eq $lnode and consul-c1-running eq 0`
    - Use resource-discovery=never if we don't want resource to run anywhere in system.
      - always: default, discover on this node.
      - never: never find on this node.
      - exclusive: only find on this node and exclude other node. If run with multiple node name then it maintain set of active node.
    ```
      [root@ssc-vm-c-1628 ~]# pcs constraint
      colocation  location    order       ref         remove      rule        ticket

      # Fast performance use resource-discovery
      $ pcs constraint location add http_ban_2 http srvnode-1 -INFINITY resource-discovery=never

        ref: Resource: http
          Disabled on: srvnode-1 (score:-INFINITY) (resource-discovery=never)
          Disabled on: srvnode-3 (score:-INFINITY) (resource-discovery=never)

        ref: Resource: http
          http_ban_2
          http_ban_3

      #
      $ pcs constraint location add http_allow_1 http-clone srvnode-1 INFINITY resource-discovery=exclusive
      $ pcs constraint location add http_allow_2 http-clone srvnode-2 INFINITY resource-discovery=exclusive

      Clone Set: http-clone [http]
        Started: [ srvnode-1 srvnode-2 ]
        Stopped: [ srvnode-3 ]
    ```

- colocation
    - colocation options are `add, remove`
    - default role is Started. options are [ 'Master', 'Slave', 'Started', 'Stopped' ]
    - It can also work on clone resource
    ```
    # pcs constraint  colocation add [<role>] statsd-clone with [<role>] http-clone score=INFINITY

    # IT mean keep statsd-clone colocated with httpd-clone opposite is not possible.
    pcs constraint  colocation add statsd-clone with http-clone score=INFINITY

    # It mean if kibana-vip stopped on node then only start haproxy-clone
    pcs constraint  colocation add haproxy-c1-clone with kibana-vip-clone score=-INFINITY
    ```

- order
    - we can manage order between clone and unclone resource.
    - In clone resource we can use `clone-min` to manage how many clone need to fail before failing dependency resource.

    ```
    pcs resource restart statsd-clone srvnode-3

    ```
===================================================================================

pcs resource create http systemd:httpd clone clone-max=3 clone-node-max=1 clone-min=2 globally-unique=true interleave=true

# Test case

```
pcs resource create stats systemd:s3server clone clone-max=33 clone-node-max=11 globally-unique=true
```

1. colocation of clone and unclone resource
  - if clone fail then unclone resource will switch over to other node

  ```
  pcs constraint colocation add http with statsd-clone score=INFINITY

  # If clone fail then http switch to other node
  Clone Set: statsd-clone [statsd]
      Started: [ srvnode-2 srvnode-3 ]
      Stopped: [ srvnode-1 ]
  http   (systemd:httpd):        Started srvnode-2

  # If http fail clone will not fail but http run on other node
  Clone Set: statsd-clone [statsd]
      Started: [ srvnode-1 srvnode-2 srvnode-3 ]
  http   (systemd:httpd):        Started srvnode-1
  ```

2. Both clone resource colocation

  - `score=INFINITY` use positive for same node and negative for opposite node.
  - `statsd-clone with http-clone` mean statsd-clone should be on same node of http-clone. if http clone fail statsd will get stopped.
  - `statsd-clone with http-clone`, here if statsd fail then http will not get stopped.
  - We can set opposite clone property
  ```
  # cmd
  pcs constraint  colocation add statsd-clone with http-clone score=INFINITY

  # http fail will stop statsd on that node
  Clone Set: statsd-clone [statsd]
      Started: [ srvnode-1 srvnode-3 ]
      Stopped: [ srvnode-2 ]
  Clone Set: http-clone [http]
      Started: [ srvnode-1 srvnode-3 ]
      Stopped: [ srvnode-2 ]

  # statsd fail will not stop http
  Clone Set: statsd-clone [statsd]
      Started: [ srvnode-1 srvnode-3 ]
      Stopped: [ srvnode-2 ]
  Clone Set: http-clone [http]
      Started: [ srvnode-1 srvnode-2 srvnode-3 ]

  # if haproxy stopped then only start kibana
  pcs constraint  colocation add haproxy-c1-clone with kibana-vip-clone score=-INFINITY

  Clone Set: kibana-vip-clone [kibana-vip]
      Started: [ srvnode-1 srvnode-2 ]
      Stopped: [ srvnode-3 ]
  Clone Set: haproxy-c1-clone [haproxy-c1]
      Started: [ srvnode-3 ]
      Stopped: [ srvnode-1 srvnode-2 ]

  ```

3. Order between clone resources

  - default if colocation not given then failing one clone will not affect other.
  - We can configure clone-min so that this count of clone should fail before failing dependencies.
  ```
  pcs constraint order statsd-clone then haproxy-c1-clone

  # clone-min=2 mean 2 statsd-clone need to fail before stopping order.

  Clone Set: haproxy-c1-clone [haproxy-c1]
     Stopped: [ srvnode-1 srvnode-2 srvnode-3 ]
  Clone Set: statsd-clone [statsd]
     Started: [ srvnode-3 ]
     Stopped: [ srvnode-1 srvnode-2 ]
  ```

4. Stop start clone on particular node
  ```
  pcs resource ban statsd-clone srvnode-3
  pcs resource clear statsd-clone
  ```

=======================================================================

# multiple clone on node

- Try running multiple resource running on multiple node.
- Here for every clone resource count start from 0.
- From clone-max=33 clone-node-max=11, we can consider no. of clone per node.
- Removing node will not remove extra clone.
- Adding node will also not create extra clone.

### Approach 1: all clone on all node

- Here all clones running equally divided on nodes.
- after adding and removing node may run different clone on that node
- Approach good if clone not bind to node.

```
pcs resource create s3server ocf:seagate:s3server service=s3server unique_clone=true clone clone-max=33 clone-node-max=11 globally-unique=true

pcs resource create motr ocf:seagate:s3server service=motr unique_clone=true clone clone-max=6 clone-node-max=2 globally-unique=true

pcs constraint colocation add s3server-clone with http-clone

  Clone Set: s3server-clone [s3server] (unique)
     s3server:0 (ocf::seagate:s3server):        Started srvnode-3
     s3server:1 (ocf::seagate:s3server):        Started srvnode-1
     s3server:2 (ocf::seagate:s3server):        Started srvnode-2
     s3server:3 (ocf::seagate:s3server):        Started srvnode-3
     s3server:4 (ocf::seagate:s3server):        Started srvnode-1
     s3server:5 (ocf::seagate:s3server):        Started srvnode-2
     s3server:6 (ocf::seagate:s3server):        Started srvnode-3
     s3server:7 (ocf::seagate:s3server):        Started srvnode-1
     s3server:8 (ocf::seagate:s3server):        Started srvnode-2
     s3server:9 (ocf::seagate:s3server):        Started srvnode-3
     s3server:10        (ocf::seagate:s3server):        Started srvnode-1
     s3server:11        (ocf::seagate:s3server):        Started srvnode-2
     s3server:12        (ocf::seagate:s3server):        Started srvnode-3
     s3server:13        (ocf::seagate:s3server):        Started srvnode-1
     s3server:14        (ocf::seagate:s3server):        Started srvnode-2
     s3server:15        (ocf::seagate:s3server):        Started srvnode-3
     s3server:16        (ocf::seagate:s3server):        Started srvnode-1
     s3server:17        (ocf::seagate:s3server):        Started srvnode-2
     s3server:18        (ocf::seagate:s3server):        Started srvnode-3
     s3server:19        (ocf::seagate:s3server):        Started srvnode-1
     s3server:20        (ocf::seagate:s3server):        Started srvnode-2
     s3server:21        (ocf::seagate:s3server):        Started srvnode-3
     s3server:22        (ocf::seagate:s3server):        Started srvnode-1
     s3server:23        (ocf::seagate:s3server):        Started srvnode-2
     s3server:24        (ocf::seagate:s3server):        Started srvnode-3
     s3server:25        (ocf::seagate:s3server):        Started srvnode-1
     s3server:26        (ocf::seagate:s3server):        Started srvnode-2
     s3server:27        (ocf::seagate:s3server):        Started srvnode-3
     s3server:28        (ocf::seagate:s3server):        Started srvnode-1
     s3server:29        (ocf::seagate:s3server):        Started srvnode-2
     s3server:30        (ocf::seagate:s3server):        Started srvnode-3
     s3server:31        (ocf::seagate:s3server):        Started srvnode-1
     s3server:32        (ocf::seagate:s3server):        Started srvnode-2
```

### Approach 2: all clone on one node

```
cib_file=cib_cortx_cluster.xml

pcs cluster cib $cib_file

pcs -f $cib_file resource create s3server-1 ocf:seagate:s3server num=1 unique_clone=true clone clone-max=11 clone-node-max=11 globally-unique=true

pcs -f $cib_file constraint location add s3server_srvnode-1 s3server-1-clone srvnode-1 INFINITY resource-discovery=exclusive

pcs -f $cib_file constraint colocation add s3server-1-clone with http-clone

###
pcs -f $cib_file resource create s3server-2 ocf:seagate:s3server num=2 unique_clone=true clone clone-max=11 clone-node-max=11 globally-unique=true

pcs -f $cib_file constraint location add s3server_srvnode-2 s3server-2-clone srvnode-2 INFINITY resource-discovery=exclusive

pcs -f $cib_file constraint colocation add s3server-2-clone with http-clone

###
pcs -f $cib_file resource create s3server-3 ocf:seagate:s3server num=3 unique_clone=true clone clone-max=11 clone-node-max=11 globally-unique=true

pcs -f $cib_file constraint location add s3server_srvnode-3 s3server-3-clone srvnode-3 INFINITY resource-discovery=exclusive

pcs -f $cib_file constraint colocation add s3server-3-clone with http-clone

pcs cluster cib-push $cib_file

  Clone Set: s3server-1-clone [s3server-1] (unique)
     s3server-1:0       (ocf::seagate:s3server):        Started srvnode-1
     s3server-1:1       (ocf::seagate:s3server):        Started srvnode-1
     s3server-1:2       (ocf::seagate:s3server):        Started srvnode-1
     s3server-1:3       (ocf::seagate:s3server):        Started srvnode-1
     s3server-1:4       (ocf::seagate:s3server):        Started srvnode-1
     s3server-1:5       (ocf::seagate:s3server):        Started srvnode-1
     s3server-1:6       (ocf::seagate:s3server):        Started srvnode-1
     s3server-1:7       (ocf::seagate:s3server):        Started srvnode-1
     s3server-1:8       (ocf::seagate:s3server):        Started srvnode-1
     s3server-1:9       (ocf::seagate:s3server):        Started srvnode-1
     s3server-1:10      (ocf::seagate:s3server):        Started srvnode-1
 Clone Set: s3server-2-clone [s3server-2] (unique)
     s3server-2:0       (ocf::seagate:s3server):        Started srvnode-2
     s3server-2:1       (ocf::seagate:s3server):        Started srvnode-2
     s3server-2:2       (ocf::seagate:s3server):        Started srvnode-2
     s3server-2:3       (ocf::seagate:s3server):        Started srvnode-2
     s3server-2:4       (ocf::seagate:s3server):        Started srvnode-2
     s3server-2:5       (ocf::seagate:s3server):        Started srvnode-2
     s3server-2:6       (ocf::seagate:s3server):        Started srvnode-2
     s3server-2:7       (ocf::seagate:s3server):        Started srvnode-2
     s3server-2:8       (ocf::seagate:s3server):        Started srvnode-2
     s3server-2:9       (ocf::seagate:s3server):        Started srvnode-2
     s3server-2:10      (ocf::seagate:s3server):        Started srvnode-2
 Clone Set: s3server-3-clone [s3server-3] (unique)
     s3server-3:0       (ocf::seagate:s3server):        Started srvnode-3
     s3server-3:1       (ocf::seagate:s3server):        Started srvnode-3
     s3server-3:2       (ocf::seagate:s3server):        Started srvnode-3
     s3server-3:3       (ocf::seagate:s3server):        Started srvnode-3
     s3server-3:4       (ocf::seagate:s3server):        Started srvnode-3
     s3server-3:5       (ocf::seagate:s3server):        Started srvnode-3
     s3server-3:6       (ocf::seagate:s3server):        Started srvnode-3
     s3server-3:7       (ocf::seagate:s3server):        Started srvnode-3
     s3server-3:8       (ocf::seagate:s3server):        Started srvnode-3
     s3server-3:9       (ocf::seagate:s3server):        Started srvnode-3
     s3server-3:10      (ocf::seagate:s3server):        Started srvnode-3
```