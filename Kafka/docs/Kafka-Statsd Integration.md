## Kafka-backend for statsd

Statsd is a network daemon that runs on the Node.js platform and listens for statistics, like counters and timers, sent over UDP or TCP and sends aggregates to one or more pluggable backend services. The following steps will illustrate how to export the data from statsd to a kafka topic.

1. Install [statsd](https://github.com/statsd/statsd#manual-installation)
&nbsp;

2. Install [statsd-kafka-backend](https://github.com/target/statsd-kafka-backend#install) in your statsd directory.
&nbsp;

3. In your statsd directory, add a configuration file __myconf.json__ and add the following contents to it.
	```
	{
        servers: {
            server: ["./servers/tcp" ]
        }, 
        port: 8125,
        backends: [ "./backends/console","./node_modules/statsd-kafka-backend/kafka-backend" ],
        console: {
            prettyprint: true
        },
        restProxyUrl: "http://localhost:8081/topics",
        kafkaTopic: "test-statsd"
    }
	```

4. Configure and add the metrics to monitor as required for the statsd service.
&nbsp;

5. Install __karapace__ using the steps given below. Karapace is a rest server for interacting with kafka.
	1. Download the [zip/tar](https://github.com/aiven/karapace/releases) archive and extract the contents or clone the [git repo](https://github.com/aiven/karapace).
	&nbsp;

	2. In the karapace root directory install the dependencies using the following command
		```
		$ pip3 install -r ./requirements-dev.txt
		```

	3. Build the karpace binary using the command
		```
		$ python3.6 setup.py bdist_egg
		```
	
	4. Install the binary using the command 
		```
		$ python3.6 -m easy_install dist/karapace-2.0.1.dev15-py3.6.egg
		```

	5. Add a configuration file __config.json__ for karapace and add the following content to it.
		```
        {
            "advertised_hostname": "localhost",
            "bootstrap_uri": "127.0.0.1:9092",
            "client_id": "sr-1",
            "compatibility": "FULL",
            "group_id": "statsd",
            "host": "127.0.0.1",
            "log_level": "INFO",
            "port": 8081,
            "master_eligibility": true,
            "replication_factor": 1,
            "security_protocol": "PLAINTEXT",
            "ssl_cafile": null,
            "ssl_certfile": null,
            "ssl_keyfile": null,
            "karapace_rest": true,
            "karapace_registry": true,
            "topic_name": "test-statsd"
        }
		```
	
	6. Start the karapace service using the command
		```
		$ karapace config.json
		```
		Note: This will start a REST server over the already running kafka cluster.
	&nbsp;
	
6. Start the statsd service using 
	```
	$ node stats.js myconf.json
	```

7. Verify the statsd logs in the kafka topic by running a consumer instance
