## Kafka 3 node cluster setup

1. Java is required for kafka. If not already present, install it using
    ```
	$ yum install java 
    $ yum install java-devel
	```

2. Download kafka (latest version 2.5.0) binary using the command 
    ```
	$ curl “http://apache.spinellicreations.com/kafka/2.5.0/kafka_2.12-2.5.0.tgz” -o kafka.tgz  
	```

    For the older version (0.11.0.3)
    ```
	$ curl “https://archive.apache.org/dist/kafka/0.11.0.3/kafka_2.11-0.11.0.3.tgz” -o kafka.tgz
	```

3. Extract the files to a directory
    ```
	$ tar –xvzf kafka.tgz --strip 1
	```

4. For zookeeper setup, you can use the zookeeper which comes along with the kafka package or you can separately download the zookeeper package. For using the zookeeper which is in the kafka package follow the below steps and repeat on every node in the cluster.
&nbsp;

	1. Define the configuration for the zookeeper in the kafka/config/zookeeper.properties file by defining the following configuration parameters - 

			tickTime=2000
			initLimit=10
			syncLimit=5
			dataDir=<path for data directory>
			dataLogDir=<path for log data directory (if not defined, then datadir will be used)>
			clientPort=2181
			server.1=<node 1 address>:2888:3888
			server.2=<node 2 address>:2888:3888
			server.3=<node 3 address>:2888:3888
			autopurge.snapRetainCount=3
			autopurge.purgeInterval=24

		The details for the configuration parameters can be found at https://zookeeper.apache.org/doc/current/zookeeperStarted.html.
&nbsp;

	2. In the __dataDir__ folder, add a file __myid__ and add the node id 1 to the file in the first node. (This must be a single integer value).
	Similarly, for nodes 2 and 3, add their respective ids in __dataDir/myid__ file on the respective nodes.
&nbsp;

	3. From the kafka directory, start the zookeeper server using the config defined above 
		```
		$ ./bin/zookeeper-server-start.sh config/zookeeper.properties 
		```

	4. For independent zookeeper installation and setup follow the steps listed in Zookeeper installation and setup 
&nbsp;

5. Update the kafka server configuration in the __config/server.properties__ file in the kafka directory as follows
&nbsp;

	1. Define a unique broker id for each kafka server.
		```
		broker.id=0 
		```
		Note : It is possible to have multiple kafka server instances on a single node. In that case we need to define separate server.properties file for each instance.
&nbsp;

	2. Define a directory for storing of log files
		```
		log.dirs=<path for storing logs>
		```
		Note : It is possible to define a comma separated list of directories
&nbsp;

	3. To form a cluster of 3 nodes, add a comma separated list of node and port addresses in the zookeeper.connect parameter so that if a zookeeper instance fails, the node will automatically try to connect to the next available address
    	```
		zookeeper.connect= <node 1 address>:2181,
                           <node 2 address>:2181,
                           <node 3 address>:2181
		```

	4. Repeat the above steps for each node in the cluster.
&nbsp;

6. From the kafka directory run the kafka server on each node

	```
	$ ./bin/kafka-server-start.sh config/server.properties
	```

7. On one of the nodes create a topic named __test__

	```
	$ ./bin/kafka-topics.sh --create –bootstrap-server <list of server:port> --replication-factor 3 --partitions 1 --topic <topicname>
	```

	Note: Here __list of server:port__ can be __localhost:9092__ or a comma separated list of bootstrap servers
	If using the older version, use __-- zookeeper__ instead of __--bootstrap-server__ .
&nbsp;

8. Verify that the topic has been created on the by 
    ```
	$ ./bin/kafka-topics.sh --list –bootstrap-server <list of server:port>
	```

9. Now run the producer script to publish a message
    ```
	$ ./bin/kafka-console-producer.sh --bootstrap-server <list of server:port> --topic test
      > This is a message
      > This is another message
	```

	Note: Here __list of server:port__ can be __localhost:9092__ or a comma separated list of bootstrap servers
	If using the older version, use __–broker-list__ instead of __-- bootstrap-server__ .
&nbsp;

10. Run the consumer scripts to read the message from the beginning
    ```
	$ ./bin/kafka-console-consumer.sh --bootstrap-server <list of server:port> --topic test --from-beginning
      > Test Msg1
      > Test Msg2 
	```
	
	Note: Here __list of server:port__ can be __localhost:9092__ or a comma separated list of bootstrap servers
&nbsp;

## Zookeeper installation and setup

1.	Download zookeeper using the command 
    ```
	$ curl “https://mirrors.sonic.net/apache/zookeeper/zookeeper-3.6.1/apache-zookeeper-3.6.1-bin.tar.gz” -o zookeeper.tar.gz
	```

2.	Extract the files to a directory
    ```
	$ tar –xvzf zookeeper.tar.gz --strip 1
	```

3.	Add a zoo.cfg file to the conf directory and add the following lines to the file.

    ```
	tickTime=2000
    initLimit=10
    syncLimit=5
    dataDir=<path for data directory>
    dataLogDir=<path for log data directory (if not defined, then datadir will be used)>
    clientPort=2181
    server.1=<node 1 address>:2888:3888
    server.2=<node 2 address>:2888:3888
    server.3=<node 3 address>:2888:3888
    autopurge.snapRetainCount=3
    autopurge.purgeInterval=24
	```

4.	From the zookeeper directory, start the zookeeper server
    ```
	$ ./bin/zkServer.sh start
	```
&nbsp;

## Kafka Basics
1. __Replication__ - The default values for replication configuration can be found in the __config/server.properties__ file. For deployment purposes it is recommended to have a replication factor of more than 1 to ensure availability.
&nbsp;

2. __Partitions__ - The default value for number of partitions can be found in the __config/server.properties__ file. More partitions allow greater parallelism for consumption, but this will also result in more files across the brokers. Custom partitions for a topic can also be defined while creating a topic.


&nbsp;

## Using the python Client for kafka

1.	Install python 3.6
    ```
	$ yum install python36
	```

2.	Download confluent kafka client for python
    ```
	$ pip3 install confluent-kafka
	```

3.	For running a __producer__ client, run the following code snippet

    ```
	from confluent_kafka import Producer

    p = Producer({'bootstrap.servers': 'localhost:9092'})
    def delivery_report(err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))
 
    for loop in range(10):
        p.produce('test', 'This is test msg '+str(loop), callback=delivery_report)
 
    p.flush()
	```
	The above code will publish 10 messages to the topic __test__
	
	Note : the topic must already be created on the broker or the flag for auto creating topics must be true
&nbsp;

4.	For running a __consumer__ client, run the following code snippet

    ```
	from confluent_kafka import Consumer

    c = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'mygrp',
    })
    c.subscribe(['test'])
 
    while True:
        msg = c.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue
       print('Received message: {}'.format(msg.value().decode('utf-8')))
     
    c.close()
	```
	The above code will subscribe to the topic __test__
	
	Note : the topic must already be created on the broker or the flag for auto creating topics must be true
&nbsp;

## ‘Exactly-Once’ implementation

In case of producer or broker failures, there is a possibility that the message might get duplicated due to retries at the producer end. To avoid such duplication, we can implement a transactional producer which will ensure that a message is published exactly once to a topic and thus achieve idempotency.

1.	The following config is required for the producer
	```
    p = Producer( {
        'bootstrap.servers': 'localhost:9092',
        'request.required.acks' : 'all',
        'transactional.id' : '<unique for each producer instance>',
        'max.in.flight.requests.per.connection' : <1-5 for achieving idempotency>,
        'enable.idempotence' : True
    } )
	```

2.	When publishing messages from the producer, use the following transaction APIs
	```
    p.init_transactions()     # this needs to be called once before any other transactional API
    .
    .
	p.begin_transaction()
	p.produce(<topic>, <message>)
	p.commit_transaction()
	```

3.	At the consumer, the following config is needed
	```
    c = Consumer( {
        'bootstrap.servers': 'localhost:9092',
        'group.id': '<group_name>',
        'isolation.level' : 'read_committed',
        'enable.auto.commit' : False
    } )
	```
	In order to achieve idempotency at the consumer, the consumer must be configured with isolation-level as read committed so that it will read only those messages which have been committed by the producer to the message queue.
&nbsp;
	Also, the auto-commit should be configured as false and the consumer should manually commit the offset after consuming the message using c.commit().
&nbsp;

4.	For a scenario where the consumer is reading from topic1 and publishing the same message to topic2 ( kafka streams application ), complete idempotency can be achieved using the above configuration and then committing the consumer offsets (for topic1) in the same transaction where the producer is writing to topic2.
&nbsp;

	For a standalone consumer, which is only reading and consuming the messages, to ensure idempotency, it is the user’s responsibility to ensure that consuming the message and committing the offset is done in a single atomic process.

## Performance Test measurement

1.	Install nmon utility for measurement of cpu statistics, memory statistics and network statistics
    ```
	$ yum install nmon
	```

2.	Before starting the test, measure the disk usage for the topic using the command __du-l__.
&nbsp;

3.	Run the nmon utility and observe the cpu, network and memory statistics.
Alternatively, nmon can also log the parameters periodically in a file. This can be done using the command
    ```
	$ nmon –F <File name (node1.nmon)> -c <number of snapshots to be captured> -s <interval between snapshots in sec> -T -U
	```
	Note : -T is used for capturing the top process statistics–U for capturing the CPU utilization statistics
&nbsp;

4.	Run 16 instances of producer_performance_test.py which will produce 64k messages of 1kb each to generate a total of 1Gb data. 
The number of producers can be increased depending on the test requirements. Running very high number of producers on a single VM will result in exhaustion of resources on the VM.
&nbsp;

5.	Run multiple instances of consumer_performance_test.py to consume the messages.
&nbsp;

6.	After the test finishes, capture the disk usage to verify that all the messages have been captured.
&nbsp;


## Kafka-Connect

Kafka connect is a tool which will allow kafka to import or export data from kafka topics to other external databases. In order to do so, Kafka provides a method to define the connector which will do the task of exporting data to external database (__sink connector__) and importing data from external database (__source connector__). The steps and configuration for connecting to the elasticsearch database is given below.

1. Install and run Elasticsearch

	1. Download elasticsearch using the below command
		```
		$ wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.8.0-linux-x86_64.tar.gz
		$ tar -xzf elasticsearch-7.8.0-linux-x86_64.tar.gz
		$ cd elasticsearch
		```

	2. Update the following configurations in __/config/elasticsearch.yaml__ file.
		```
		path.data=<Data directory for elasticsearch>
		path.log=<Log directory>
		network.host: 0.0.0.0
		http.port: 9200
		transport.host: 9200
		transport.tcp.port: 9300
		``` 

	3. Run the elasticsearch using the command below
		```
		$ ./bin/elasticsearch/
		```

2. Elasticsearch connector

	1. Download and extract the confluent kafka-elasticsearch sink connector from https://www.confluent.io/hub/confluentinc/kafka-connect-elasticsearch
&nbsp;

	2. Update the configuration file at __etc/quickstart-elasticsearch.properties__ for the connector with the following configurations
		```
		name=elasticsearch-sink
		connector.class=io.confluent.connect.elasticsearch.ElasticsearchSinkConnector
		tasks.max=1
		topics=<topic name>
		key.ignore=true
		schema.ignore=true
		connection.url=http://localhost:9200
		type.name=_doc
		```

3. Starting the kafka-connector

	1. In the kafka directory, update the configurations in the __config/connect-standalone.properties__ file as given below
		```
		.
		.
		value.converter.schemas.enable=false
		offset.storage.file.filename=<file for storing connect offsets>
		plugin.path=<path to the confluent kafka-elasticsearch connector folder>
		.
		```
	
	2. Run the kafka connnect and start the above connector using the below command
		```
		$ ./bin/connect-standalone.sh config/connect-standalone.properties <path to quickstart-elasticsearch.properties>
		```

	3. Run a producer to publish some json messages to the topic. For eg-
		```
		{"Key":"TestKey","Value":"TestValue"}
		```

	4. Verify the document in the elasticsearch database using the curl commands
		```
		$ curl -X GET localhost:9200/<topicname>/_search?pretty=true
		```

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
