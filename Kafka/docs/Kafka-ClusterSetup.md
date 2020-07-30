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
