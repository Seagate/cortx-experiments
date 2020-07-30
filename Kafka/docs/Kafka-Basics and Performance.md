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
