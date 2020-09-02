# ELK Stack
ELK Stack is a collection of three open-source products:
   1. Elasticsearch: Log aggregator 
   2. Logstash: Agent to send logs into Elasticsearch 
   3. Kibana: GUI web interface to search logs 

Elasticsearch is an open source, full-text search and analysis engine, based on the Apache Lucene search engine. Logstash is a log aggregator that collects data from various input sources, executes different transformations and enhancements and then ships the data to various supported output destinations. Kibana is a visualization layer that works on top of Elasticsearch, providing users with the ability to analyze and visualize the data.   

Modern log management and analysis solutions include the following key capabilities: 

     Aggregation – the ability to collect and ship logs from multiple data sources. 

     Processing – the ability to transform log messages into meaningful data for easier analysis. 

     Storage – the ability to store data for extended time periods to allow for monitoring, trend analysis, and security use cases. 

     Analysis – the ability to dissect the data by querying it and creating visualizations and dashboards on top of it. 
 
 ## Logstash  
 ### Introduction: 
 Logstash is an open source data collection engine with real-time pipelining capabilities. Logstash can dynamically unify data from disparate sources and normalize the data into destinations of your choice. Cleanse and democratize all your data for diverse advanced downstream analytics and visualization use cases. 

While Logstash originally drove innovation in log collection, its capabilities extend well beyond that use case. Any type of event can be enriched and transformed with a broad array of input, filter, and output plugins, with many native codecs further simplifying the ingestion process. Logstash accelerates your insights by harnessing a greater volume and variety of data. 

 ### Installing Logstash: 
 This section guides you through the process of installing Logstash and verifying that everything is running properly. 
 #### Java (JVM) versionedit 

Logstash requires one of these versions: 
  
  Java 8 
  
  Java 11 
  
  Java 14 

### Logstash on docker: 
A list of all published Docker images and tags is available at www.docker.elastic.co. The source code is in GitHub. 

We can create our own Dockerfile with required configrations (myconfig.conf)
#### Configuring Logstash:
To configure Logstash, you create a config file that specifies which plugins you want to use and settings for each plugin. You can reference event fields in a configuration and use conditionals to process events when they meet certain criteria. When you run logstash, you use the -f to specify your config file. 

Let’s step through creating a simple config file and using it to run Logstash. Create a file named "myconfig.conf".A Logstash config file has a separate section for each type of plugin you want to add to the event processing pipeline. 
```python
# This is a comment. You should use comments to describe
# parts of your configuration.
input {
  ...
}

filter {
  ...
}

output {
  ...
}
```
The Logstash event processing pipeline has three stages: **inputs → filters → outputs**. 

**Inputs** generate events, **filters** modify them, and **outputs** ship them elsewhere. 

Each section contains the configuration options for one or more plugins. If you specify multiple filters, they are applied in the order of their appearance in the configuration file. 

#### Process of creating logstash image: 
   1. Create a new directory. 
   2. Add myconfig.conf and Dockerfile for logstash 
   3. Create docker image using follwing command:
   ```python
docker build –t logstash . 
```
This process will generate logstash image with name "logstash".

### Sincedb:
Logstash has an interesting component or feature called sincedb. Logstash keeps track of where it was last reading a file before it crashed or stopped.

By default, the sincedb file is placed in the data directory of Logstash with a filename based on the filename patterns being watched (i.e. the path option). Thus, changing the filename patterns will result in a new sincedb file being used and any existing current position state will be lost. If you change your patterns with any frequency it might make sense to explicitly choose a sincedb path with the sincedb_path option.
** NOTE: Provide path to sincedb which points directory from main container so that even logstash fails it will start reading from the same place where it left.**

**Use this “logstash” image in sidecar container** 
## Elasticsearch
Elasticsearch is the distributed search and analytics engine at the heart of the Elastic Stack. 

Elasticsearch provides near real-time search and analytics for all types of data. Whether you have structured or unstructured text, numerical data, or geospatial data, Elasticsearch can efficiently store and index it in a way that supports fast searches. 

### Install Elasticsearch from archive on Linux 

Elasticsearch is as a .tar.gz archive for Linux and MacOS.
 ```python
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.8.1-linux-x86_64.tar.gz
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.8.1-linux-x86_64.tar.gz.sha512
shasum -a 512 -c elasticsearch-7.8.1-linux-x86_64.tar.gz.sha512 
tar -xzf elasticsearch-7.8.1-linux-x86_64.tar.gz
cd elasticsearch-7.8.1/ 
```
### Access elasticsearch from a remote location
**elasticsearch.yml** for configuring Elasticsearch. These files are located in the config directory, whose default location depends on whether or not the installation is from an archive distribution 
 ```python
 http.host : "IP_OF_HOST"
 http.port : "9200"
```
Add above lines to elasticsearch.yml

Run Elasticsearch using command(make sure that you are in a same directory where elasticsearch is installed):
 ```python
 ./elasticsearch-7.8.1/bin/elasticsearch
```
## Kibana — your window into the Elastic Stackedit
Visualize and analyze your data and manage all things Elastic Stack.

Whether you’re an analyst or an admin, Kibana makes your data actionable by providing three key functions. Kibana is:

- An open-source analytics and visualization platform. Use Kibana to explore your Elasticsearch data, and then build beautiful visualizations and dashboards.
- A UI for managing the Elastic Stack. Manage your security settings, assign user roles, take snapshots, roll up your data, and more — all from the convenience of a Kibana UI.
- A centralized hub for Elastic’s solutions. From log analytics to document discovery to SIEM, Kibana is the portal for accessing these and other capabilities.
### Install kibana
Download and Install kibana using this [link.](https://www.elastic.co/guide/en/kibana/current/setup.html)

### Access kibana from remote location:
In kibana.yml add following lines:
```python
 server.host: "IP_of_host"
```
### Run Kibana
```python
 bin/kibana
```


