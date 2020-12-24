## Horizontal Scalability

1. #### Add a new node

	1. For adding a new node (Kafka broker) to the existing cluster, install Kafka on new node.
	2. Configure Kafka broker by assigning a new unique id to it in server.properties.
	        ```
		broker.id=<new unique broker id>
	        ```
	3. In server.properties, assign following property to existing zookeeper.
	        ```
		zookeeper.connect=<Existing ZK server>
		```

	4. Start the kafka broker on the new node using above configuration files.
	&nbsp;

	5. We can verify that the new node is now a part of the kafka cluster by running the following command
		```
		$ ./bin/zookeeper-shell.sh localhost:2181 ls /broker/ids
		```
        6. Note that the partitions of existing topics will not be moved to new node automatically. It needs to be done manually as described in next section.
	
2. #### Re-distributing partitions to new node
        
	1. For re-distributing partitions after adding a node, there is tool provided by kafka - kafka-reassign-partitions.sh.
	2. First generate a json file, having list of all topics which requires rebalancing.
	        ```
		$ cat topics-to-move.json
                  {"topics": [{"topic": "topic1"},
                              {"topic": "topic2"}],
                    "version":1
                  }
		```
	2. Generate a new plan for partition assignment as below (new node have broker id as 3)-
	        ```
		$ bin/kafka-reassign-partitions.sh --bootstrap-server <brokers> --topics-to-move-json-file topics-to-move.json --broker-list "0,1,2,3" --generate
		Current partition replica assignment

               {"version":1,
                "partitions":[{"topic":"topic1","partition":2,"replicas":[0,1]},
                              {"topic":"topic1","partition":0,"replicas":[1,2]},
                              {"topic":"topic2","partition":2,"replicas":[0,2]},
                              {"topic":"topic2","partition":0,"replicas":[0,1]},
                              {"topic":"topic1","partition":1,"replicas":[1,2]},
                              {"topic":"topic2","partition":1,"replicas":[0,2]}]
               }

               Proposed partition reassignment configuration

               {"version":1,
                "partitions":[{"topic":"foo1","partition":2,"replicas":[0,1]},
                              {"topic":"foo1","partition":0,"replicas":[1,2]},
                              {"topic":"foo2","partition":2,"replicas":[0,1]},
                              {"topic":"foo2","partition":0,"replicas":[1,2]},
                              {"topic":"foo1","partition":1,"replicas":[2,3]},
                              {"topic":"foo2","partition":1,"replicas":[2,3]}]
               }
		
		```
	3. Store proposed partition in a json file, new_partitions.json.
	4. Execute following commands to move the partitions -
	        ```
		$ bin/kafka-reassign-partitions.sh --bootstrap-server <brokers> --reassignment-json-file new_partitions.json --execute
		```
	5. The following command is used for verifying whether the movement is complete or not-
	        ```
	        $ bin/kafka-reassign-partitions.sh --bootstrap-server <brokers> --reassignment-json-file new_partitions.json --verify
	        ```
	6. Since the cluster is running while movement is done. The replica leaders may still be from existing nodes. In order to make new node leader of some partitions,                  following command can be executed -
	        ```
	        $ bin/kafka-preferred-replica-election.sh --bootstrap-server <brokers>
	        ```


3. #### Decommission/Remove a broker/node
	For decommissioning a broker, we first need to reassign the topic partitions on that node to some other node. In order to do so, we need to first list all the topic partitions on the node that we wish to remove. Below are the steps that can be followed to remove a broker from a cluster.
	&nbsp;

	1. On the node lits all the topics and identify the ones to be removed using the following command
		```
		$ ./bin/kafka-topics.sh --zookeeper localhost:2182 --describe
		```

	2. Make a json file __MoveTopics.json__ with a list of all the topics to be moved to other nodes.
		```
		{
			"version":1,
			"topics":[
				{"topic":"<topic 1>"},
				{"topic":"<topic 2>"},
				{"topic":"<topic 3>"}
			]
		}
		```

	3. Generate a topic-partition reassignment plan using the command
		```
		$ ./bin/kafka-reassign-partitions.sh --generate --zookeeper localhost:2181 --topics-to-move-json-file MoveTopics.json --broker-list <list of brokers ids where we want to move the partitions. eg 1,2,3>
		```
		Note: This will only generate a plan and does not move the topic partitions to other nodes.
	&nbsp;

	4. The output of the above commnd shows a new plan for reassignment of the topic partitions. Either use the above plan or change the reassignment as per requirement on the brokers. Define the reassignment plan in a new json file __ReassignmentPlan.json__ .
	&nbsp;

	5. Move the topic-partions to other nodes as per the plan using the below command
		```
		$ ./bin/kafka-reassign-partitions.sh --execute --zookeeper localhost:2181 --reassignment-json-file ReassignmentPlan.json
		```

	6. Verify the assignment according to the plan using the below command
		```
		$ ./bin/kafka-reassign-partitions.sh --verify --zookeeper localhost:2181 --reassignment-json-file ReassignmentPlan.json
		```
		
	7. Stop the kafka server and the zookeeper server on the node to completely remove the node from the kafka cluster
&nbsp;


