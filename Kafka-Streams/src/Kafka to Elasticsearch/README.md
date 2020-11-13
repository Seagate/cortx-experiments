Kakfa to Elasticsearch Sink

In this Kafka to elasticsearch pipeline we have Data being generated from Kafka producer. This data is ingested into kafka topic/s. 
Further we have a Kafka Streams application which will be performing data manipulation on the records fetched from the input topic.
Manipulation to be performed is: Windowed Word Count operation along with timestamp and data to be outputted to elasticsearch database (data residing in elasticsearch needs to 
be in json format).

Pre requisites for implementation:
1. Elasticsearch (Better if 7 or above version).
2. Java/JDK 8 (if not, lambda functions used in the streams app need to be changed accordingly).
3. Kafka Connect from Confluent.

Related docs and informative links:
https://www.confluent.io/hub/confluentinc/kafka-connect-elasticsearch
https://www.elastic.co/guide/en/elasticsearch/reference/current/rpm.html
https://www.digitalocean.com/community/tutorials/how-to-install-java-on-centos-and-fedora


