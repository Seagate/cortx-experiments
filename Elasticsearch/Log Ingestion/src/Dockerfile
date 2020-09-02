FROM ubuntu:16.04

RUN apt-get update && apt-get -y install software-properties-common
RUN apt-get update && apt-get install -y openjdk-8-jdk
RUN apt-get update && apt-get install -y wget
ENV JAVA_HOME /use/lib/jvm/openjdk-8-jdk
ENV LT_PKG_NAME logstash-7.8.1
RUN cd / && wget https://artifacts.elastic.co/downloads/logstash/logstash-7.8.1.tar.gz && tar xzf logstash-7.8.1.tar.gz && rm -f logstash-7.8.1.tar.gz && mv /logstash-7.8.1 /logstash
VOLUME ["/data"]
ADD logstash_config.conf /data/logstash_config.conf
WORKDIR /data
ADD test_log.log /data/test_log.log
CMD ["/logstash/bin/logstash","-f","/data/logstash_config.conf"]
