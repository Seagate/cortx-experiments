
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
    ```
      [root@ssc-vm-c-1628 ~]# pcs constraint
      colocation  location    order       ref         remove      rule        ticket

    # Fast performance use resource-discovery
      $ pcs constraint location kibana-vip avoids srvnode-3
      $ pcs constraint location add location-kibana-vip-srvnode-3-INFINITY kibana-vip srvnode-3 -INFINITY resource-discovery=never
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
