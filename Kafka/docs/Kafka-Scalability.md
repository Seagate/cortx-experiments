## Horizontal Scalability

1. #### Add a new node

	1. For adding a new node to the existing cluster, we need to have separate configurations for the new node. The configuration will include zookeeper and kafka server configuration files. Also, the entry for new node must be present in the __zookeeper.properties__ file of the existing servers.
		```
		server.<id for new node>=<server:port config for the node>
		```

	2. Start the zookeeper server and the kafka broker on the new node using the appropriate configuration files.
	&nbsp;

	3. We can verify that the new node is now a part of the kafka cluster by running the following command
		```
		$ ./bin/zookeeper-shell.sh localhost:2181 ls /broker/ids
		```

2. #### Decommission/Remove a broker/node
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


