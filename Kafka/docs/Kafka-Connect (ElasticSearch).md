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

