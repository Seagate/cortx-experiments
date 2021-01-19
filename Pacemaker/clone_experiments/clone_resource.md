# Objective
  - Perform clone constrain related experiment like
    - colocation
    - location
    - order
  - Find multiple clone options and its meaning.
  - Find multiple way to configure clone resource having multiple instances on node.
  - Explore Group clone.

# Summery
  - By using clone constrain we can manipulate clone dependency and order among resources. Constrain and test cases given below.
  - There and multiple clone option available from which we can manage clone size in cluster as well as per node, order of clone across nodes.
  - We can configure clone resource having multiple instances as
    - Create clone on cluster and divide in per node.
    ```console
    # Eg for 3 node and s3sever with 11 instance.
    clone-max=33, clone-node-max=11
    ```
    - Create resource per node with max clone size per node.
    ```console
    # Eg for 3 node and s3sever with 11 instance.
    For each resource on node clone-max=11, clone-node-max=11
    resource will be fixed on that node.
    ```
    - Create clone group.
    ```
    # Eg for 3 node and s3sever with 11 instance.
    Create 11 resource of s3server with group s3server_group and then clone that group.
    ```
  - We can use clone group property for io-stack and management stack.
  - resource-discovery can be used to reduce network traffic in large cluster.
  - Resource group clone is best solution and will be going to used for s3server and motr like resources.

# constraint
  - location:
    - prefers, avoid for normal case like allow/not allow resource on current node even if other node not available.
    - complex: `constraint location csm-kibana rule score=-INFINITY '#uname' eq $lnode and consul-c1-running eq 0`
    - Below are options for **resource-discovery**:
      - always: default, discover resource on this node.
      - never: never find resource on this node.
      - exclusive: only find resource on this node and exclude other node. If run with multiple node name then it maintain set of active node.
    ```bash
      # Fast performance use resource-discovery
      $ pcs constraint location add http_ban_1 http srvnode-1 -INFINITY resource-discovery=never

        ref: Resource: http
          Disabled on: srvnode-1 (score:-INFINITY) (resource-discovery=never)
          Disabled on: srvnode-3 (score:-INFINITY) (resource-discovery=never)

        ref: Resource: http
          http_ban_1

      # Allow http on specific node
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

# Clone Options
  - clone-max
    - How many copies of the resource to start. Defaults to the number of nodes in the cluster.

  - clone-node-max
    - How many copies of the resource can be started on a single node; the default value is 1.

  - clone-min
    - The number of instances that must be running before any dependent resources can run.

  - globally-unique
    - Does each copy of the clone perform a different function? Allowed values: false, true
    - If the value of this option is false, these resources behave identically everywhere they are running and thus there can be only one copy of the clone active per machine.
    - If the value of this option is true, a copy of the clone running on one machine is not equivalent to another instance, whether that instance is running on another node or on the same node. The default value is true if the value of clone-node-max is greater than one; otherwise the default value is false.

  - ordered
    - Should the copies be started in series (instead of in parallel). Allowed values: false, true. The default value is false.

  - interleave
    - Changes the behavior of ordering constraints (between clones/masters) so that copies of the first clone can start or stop as soon as the copy on the same node of the second clone has started or stopped (rather than waiting until every instance of the second clone has started or stopped). Allowed values: false, true. The default value is false.

### Test case for constrain and clone options.
  1. colocation of clone and unclone resource
    - if clone fail then unclone resource will switch over to other node
  ```bash
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

# Multiple clone instance on same node

### Approach 1: Create clone on cluster and divide in per node.
  - Here all clones running equally divided on nodes.
  - after adding and removing node may run different clone on that node
  - Approach good if clone not bind to node.

```bash
# First configure resource agent on each node.
  # Move s3server to /usr/lib/ocf/resource.d/seagate/
  # Create s3server@.service to /usr/lib/systemd/system/
  # reload systemd daemon

$ pcs resource create s3server ocf:seagate:s3server service=s3server unique_clone=true clone clone-max=33 clone-node-max=11 globally-unique=true
Output:
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

### Approach 2: Create resource per node with max clone size per node.
  - Here each node have s3server resource having 11 clone.
  - Approach good if clone if node less and clone can not move across node.

```
$ pcs resource create s3server-1 ocf:seagate:s3server num=1 unique_clone=true clone clone-max=11 clone-node-max=11 globally-unique=true

$ pcs resource create s3server-2 ocf:seagate:s3server num=2 unique_clone=true clone clone-max=11 clone-node-max=11 globally-unique=true

$ pcs resource create s3server-3 ocf:seagate:s3server num=3 unique_clone=true clone clone-max=11 clone-node-max=11 globally-unique=true

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

### Approach 3: Create clone group.
  - For s3server Create 11 instance in group and then clone group
  - It good when scaling cluster.
  - when clones not move across node and not necessary to start all service in parallel.

```
    # Move motr_fid.conf to /root/
    # Assuming all service available
    # Eg for 3 node and s3sever with 11 instance.
    Create 11 resource of s3server with group s3server_group and then clone that group.

    $ pcs resource create s3server-1 ocf:seagate:clone-service service=s3server --group s3server
    $ pcs resource create s3server-2 ocf:seagate:clone-service service=s3server --group s3server
    $ pcs resource create s3server-3 ocf:seagate:clone-service service=s3server --group s3server
    $ pcs resource create s3server-4 ocf:seagate:clone-service service=s3server --group s3server
    $ pcs resource create s3server-5 ocf:seagate:clone-service service=s3server --group s3server
    $ pcs resource create s3server-6 ocf:seagate:clone-service service=s3server --group s3server
    $ pcs resource create s3server-7 ocf:seagate:clone-service service=s3server --group s3server
    $ pcs resource create s3server-8 ocf:seagate:clone-service service=s3server --group s3server
    $ pcs resource create s3server-9 ocf:seagate:clone-service service=s3server --group s3server
    $ pcs resource create s3server-10 ocf:seagate:clone-service service=s3server --group s3server
    $ pcs resource create s3server-11 ocf:seagate:clone-service service=s3server --group s3server
    $ pcs resource clone s3server

    Clone Set: s3server-clone [s3server]
      Started: [ srvnode-1 srvnode-2 srvnode-3 ]
```

# Clone Group
  - Here pacemaker allow multiple resource in same group and we can clone group to flow across node.
  - In group resource will start in order on same node and across node it start in parallel

```bash

# Move motr_fid.conf to /root/
# Assuming all service available
cib_file=cib_cortx_cluster.xml
pcs cluster cib $cib_file
pcs -f $cib_file resource create motr-confd ocf:heartbeat:Dummy --group io-stack
pcs -f $cib_file resource create motr-ios-1 ocf:seagate:clone-service service=motr --group motr_ios
pcs -f $cib_file resource create motr-ios-2 ocf:seagate:clone-service service=motr --group motr_ios
pcs -f $cib_file resource create hax ocf:heartbeat:Dummy --group io-stack
pcs -f $cib_file resource create haproxy  ocf:heartbeat:Dummy --group io-stack
pcs -f $cib_file resource create s3auth  ocf:heartbeat:Dummy --group io-stack
pcs -f $cib_file resource create s3server-1 ocf:seagate:clone-service service=s3server --group s3server
pcs -f $cib_file resource create s3server-2 ocf:seagate:clone-service service=s3server --group s3server
pcs -f $cib_file resource create s3server-3 ocf:seagate:clone-service service=s3server --group s3server
pcs -f $cib_file resource create s3server-4 ocf:seagate:clone-service service=s3server --group s3server
pcs -f $cib_file resource create s3server-5 ocf:seagate:clone-service service=s3server --group s3server
pcs -f $cib_file resource create s3server-6 ocf:seagate:clone-service service=s3server --group s3server
pcs -f $cib_file resource create s3server-7 ocf:seagate:clone-service service=s3server --group s3server
pcs -f $cib_file resource create s3server-8 ocf:seagate:clone-service service=s3server --group s3server
pcs -f $cib_file resource create s3server-9 ocf:seagate:clone-service service=s3server --group s3server
pcs -f $cib_file resource create s3server-10 ocf:seagate:clone-service service=s3server --group s3server
pcs -f $cib_file resource create s3server-11 ocf:seagate:clone-service service=s3server --group s3server
pcs -f $cib_file resource clone motr_ios
pcs -f $cib_file resource clone s3server
pcs -f $cib_file resource clone io-stack
pcs cluster cib-push $cib_file


 Clone Set: motr_ios-clone [motr_ios]
     Started: [ srvnode-1 srvnode-2 srvnode-3 srvnode-4 srvnode-5 ]
 Clone Set: s3server-clone [s3server]
     Started: [ srvnode-1 srvnode-2 srvnode-3 srvnode-4 srvnode-5 ]
 Clone Set: io-stack-clone [io-stack]
     Started: [ srvnode-1 srvnode-2 srvnode-3 srvnode-4 srvnode-5 ]
```
