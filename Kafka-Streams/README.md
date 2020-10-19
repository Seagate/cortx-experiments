# Kafka Streams Windowing applications using DSL

- Some important details and chages in configuration for files in src


Use of Java 8 and above JDK as the application uses lambda functions supported by java version 8 and above.


The pom.xml, MANIFEST.MF, log4j.properties file are common to all the streams application, just change the main java class names in each file respectively.


POM.xml contains all the dependencies and plugins required for the project by maven.


In the BOOTSTRAP_SERVERS_CONFIG, replace the VM names by the ones you are using.


The APPLICATION_ID_CONFIG must be simple but unique name.


If you need to specify any other serdes for the application you can do it explicitly in streams DSL.


Here in all the windowing applications, the streams application is fetching input from the Input Kafka topic "TextLinesTopic" and streams application is outputting the results 
to some Kafka topic. (e.g. tumblingoutputtopic).


In order to package the whole code, use fatjar to create a jar file alongwith dependencies.


- For creating a jar file,


1. File >> Project Structure >> Artifacts >> JAR >> from module with dependencies


2. Change manifest directory, <project folder>\src\main\java to <project folder>\src\main\resources
  
  
3. Build the Artifacts.


4. Create new run/debug configuration for application. 


5. Add the "assembly:single" maven goal after build to be executed last. Save and Run.


6. JAR file gets created in target folder.


Next, for running the application JAR file through terminal; use java -jar /target/JAR_FILENAME.jar


Please refer to Kafka streams official DSL Developer guide for more information.

https://kafka.apache.org/10/documentation/streams/developer-guide/

