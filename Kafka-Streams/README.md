# Kafka Streams Windowing applications using DSL

- Some important details and chages in config


The pom.xml, MANIFEST.MF, log4j.properties file are common to all the streams application, just change the main java class names in each file respectively.


POM.xml contains all the dependencies and plugins required for the project by maven.


In the BOOTSTRAP_SERVERS_CONFIG, replace the VM names by the ones you are using.


The APPLICATION_ID_CONFIG must be simple but unique name.


If you need to specify any other serdes for the application you can do it explicitly in streams DSL.


Here in all the windowing applications, the streams application is fetching input from the Input Kafka topic "TextLinesTopic" and streams application is outputting the results 
to some Kafka topic. (e.g. tumblingoutputtopic).


Please refer to Kafka streams official DSL Developer guide for more information.
