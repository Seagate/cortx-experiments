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

**JAVA_HOMEedit**

Logstash uses the Java version set in JAVA_HOME. The JAVA_HOME environment variable must be set for Logstash to operate correctly. 

On some Linux systems, you may need to have the JAVA_HOME environment exported before installing Logstash, particularly if you installed Java from a tarball. Logstash uses Java during installation to automatically detect your environment and install the correct startup method (SysV init scripts, Upstart, or systemd). If Logstash is unable to find the JAVA_HOME environment variable during package installation, you may get an error message, and Logstash will not start properly.
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

**Use this “logstash” image in sidecar container** 
