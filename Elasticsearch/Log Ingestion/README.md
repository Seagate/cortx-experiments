# Objective: 
Application logs can help you understand what is happening inside your application. The logs are particularly useful for debugging problems and monitoring activity. Most modern applications have some kind of logging mechanism; as such, most container engines are likewise designed to support some kind of logging. The easiest and most embraced logging method for containerized applications is to write to the standard output and standard error streams. 

However, the native functionality provided by a container engine or runtime is usually not enough for a complete logging solution. For example, if a container crashes, a pod is evicted, or a node dies, you'll usually still want to access your application's logs. As such, logs should have a separate storage and lifecycle independent of nodes, pods, or containers. 
While Kubernetes does not provide a native solution for cluster-level logging, there are several common approaches you can consider. Here are some options: 
   1. Use a node-level logging agent that runs on every node. 
   2. Include a dedicated sidecar container for logging in an application pod. 
   3. Push logs directly to a backend from within an application. 
we are selecting second option amoung this for logging.
## Include a dedicated sidecar container for logging in an application pod. 
**Ingestion** refers to the process of formatting and uploading data from external sources like applications, platforms, and servers. Log ingestion will automatically ingests log data for fast, real-time log management and analysis. 
#### Basic idea behind this concept is : 
The **Elastic Stack** (sometimes known as the ELK Stack) is the most popular open source logging platform.
Sidecar container includes logstash image. **Logstash** will help us in collecting logs from main container and parsing them. Logstash dynamically ingests, transforms, and ships your data regardless of format or complexity. Derive structure from unstructured data with grok, decipher geo coordinates from IP addresses, anonymize or exclude sensitive fields, and ease overall processing. 
**Elasticsearch** will store those logs. **Kibana** enables you to explore logs for common servers, containers, and services. You can filter the logs by various fields, start and stop live streaming, and highlight text of interest. 

 

   
