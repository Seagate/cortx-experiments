## Consul Install [on DevVM]
*	wget https://releases.hashicorp.com/consul/1.8.0/consul_1.8.0_linux_amd64.zip (latest version is available @ https://www.consul.io/downloads)
*	unzip consul_1.8.0_linux_amd64.zip [insatall zip unzip : yum install zip unzip -y]
*	sudo mv consul /bin/
*	fire 'consul' and you should be looking at consul help as shown below.
 <p align="center"><img src="../images/consul_help.JPG?raw=true"></p>
 
## Running consul agent [server mode only]
In this section we will be Running the consul as a server in a development mode to understand the default consul functionalities without extra configuration.
*	consul agent –dev –node myMachine (-dev: Enable development server mode. This is useful for quickly starting a Consul agent with all persistence options turned off.)
*	consul members –detailed
*	consul leave
This -dev flag should not be used in production environment.

## Service registration and calling the service
* There are two ways to register a service. Via service definition or using an HTTP API.
  * Consul config directory setup
   * mkdir {directory of your wish}/consul.d
   * Add service definition to a file with yourServiceName.json
    *	i.e. Web service definition would look like.
    *	‘{“service”:{“name”:”web”, “tags”: [“rails”], “port”:80}}’
   * Paste this into file {directory chosen in first step}/consul.d/web.json
* Restart the agent
* consul agent –dev –config-dir= {directory chosen in first step}/consul.d -node=myMachine
* Quering the service
  * Curl http://localhost:8500/v1/catalog/service/web 
  * for further details on service is available at https://learn.hashicorp.com/consul/getting-started/services

## KV operations using consul kv cli
* Two ways to store key-value
  * http api
  * consul kv cli
  
* Put 
  * consul kv put key val
  * example : consul kv put foo bar	
* Get
  * consul kv get -recurse
  * consul kv get key
  * consul kv get -detailed key
  * example : consul kv get foo
* delete
  * consul kv delete key
  * consul kv delete -recurse prefix
  * example : consul kv delete foo
* Update(put)
  * consul kv put foo bar
  * consul kv get foo
  * consul kv put foo one
  * consul kv get foo
* Check before setting a value to a key (CAS – check and set)
  * consul kv get -detailed key
  * consul kv put -cas -modify-index=27 key val
  * consul kv put -cas -modify-index=123 key val
  * for example checkout sequence of following command-
    * consul put foo test1
    * consul kv get -detailed foo
      * Above command Shows details as
        
        `[CreateIndex      101]`
        
        `Flags            0`
        
        `Key              foo`
        
        `LockIndex        0`
        
        `ModifyIndex      101`
        
        `Session          -`
        
        `Value            test1`
        
    * Check modify-index and if found as passed as args in put command, then only let set foo key with test2
    * consul kv put -cas -modify-index=97 foo test2 
  * We get an error messsage as as modify index is 101 and we our cas condition says 97 value: “Error! Did not write to foo: CAS failed”

## Locking in KV
* One can create a lock and attach process with that. As soon as one acquires that lock, process starts and if any-other process try to acquire the same lock then it has to wait and hence serialization is mandated using locking.
* Consul lock {options} prefix child-process
	* Prefix is a lock(or semaphore) which is writable area
	* Child-process is something which gets invoked when lock gets acquired.
	* i.e. consul lock sem1 pwd
		* whenever anyone will try to acquire sem1 lock, then one has to wait for termination of child process (pwd in this case).

## Multi Node Cluster Setup
* On the first node (N1) install consul and run consul with the following command- 

	* consul agent -server -bind=<IP_ADDRESS of that node> -bootstrap-expect=<NO_OF_SERVERS_NODES_IN_CLUSTER> -node=<NODE_NAME> -data-dir=<DATA_DIR_PATH> -config-dir=<CONFIG_DIR_PATH>

`-server           = if the node is server (blank for client)`

`-bind             = Ip address of that node`

`-bootstrap-expect = The number of server nodes in the cluster.`

`-node             = Name of node 1 in the data center`

`-data-dir         = The path where consul agent will store their state`

`-config-dir       = The path for storing the configuration settings`

`-retry-join       = List of IP address/DNS address of any of the node in the cluster`

* Similarly, on other nodes install consul and run consul with the same command without the –bootstrap-expect option.

* Now join the nodes from N1 to form a cluster using the following command

`consul join <IP_ADDR_N2> <IP_ADDR_OF_N3>`

* Verify the nodes are in sync by adding a kv pair on one node and reading the same from the other nodes



## Create consul cluster using config file (json)
* Create a directory to store the configuration file for consul.
	* mkdir path_to_consfigdir/config_dir

* In the config_dir , create a conf.json file and add the following content (along with your config params here) to it

    {
        “server” : <true for server, false for client>,
        “bootstrap_expect” : <no of servers in cluster>,
        “node_name” : “<node name>”,
        “data_dir” : “<path to your data dir>”,
        “datacenter” : “<name of datacenter>”,
        "acl" : {
		         "enabled" : false,
		         "default_policy" : "deny",
		         "enable_token_replication" : true,
		         "enable_token_persistence" : true
	        },
        “retry_join” : [
            <List of addresses to connect to>
        ]
    }

* Start the consul agent (server or client) using the command 
	* consul agent –config-dir=<path to your config dir>

* Define the bootstrap_expect option only in one server as only a single server can be present in bootstrap mode in a cluster. Never use bootstrap_expect option on multiple agents.

* Similarly start the other agents by defining the configuration file for each agent without the bootstrap_expect option.

* The agents will automatically join to form a cluster if the retry join addresses of the nodes in the cluster are defined correctly.
	* i.e. "ssc-vm-XXXX.colo.seagate.com"
