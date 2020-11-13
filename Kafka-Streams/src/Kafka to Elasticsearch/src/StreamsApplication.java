package org.apache.kafka;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import jdk.nashorn.internal.ir.debug.JSONWriter;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.common.serialization.Serde;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.kafka.common.serialization.StringSerializer;
import org.apache.kafka.common.serialization.Serializer;
import org.apache.kafka.streams.processor.TimestampExtractor;
import org.apache.kafka.clients.consumer.ConsumerRecords;

import org.apache.kafka.streams.processor.WallclockTimestampExtractor;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import org.apache.kafka.connect.json.JsonDeserializer;
import org.apache.kafka.streams.*;
import org.apache.kafka.streams.kstream.TimeWindowedDeserializer;
import org.apache.kafka.streams.kstream.TimeWindowedSerializer;
import org.apache.kafka.common.utils.Bytes;
import org.apache.kafka.streams.kstream.*;
import org.apache.kafka.streams.state.KeyValueStore;
import org.apache.kafka.streams.state.WindowStore;

import com.fasterxml.jackson.databind.JsonNode;
import org.apache.kafka.common.serialization.Deserializer;
import org.apache.kafka.common.serialization.Serde;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.common.serialization.Serializer;
import org.apache.kafka.connect.json.JsonSerializer;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.kstream.KStream;
import org.apache.kafka.streams.kstream.KTable;
import org.apache.kafka.streams.processor.AbstractProcessor;
import org.json.simple.parser.ParseException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.StringWriter;
import java.security.Key;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.time.Duration;
import java.util.Arrays;
import java.util.Date;
import java.util.Properties;
import java.util.TimeZone;

public class TumblingWindow {

    public static  void main(String[] args) {
        
        //Windowed serializer and deserializer
        StringSerializer stringSerializer = new StringSerializer();
        StringDeserializer stringDeserializer = new StringDeserializer();
        TimeWindowedSerializer<String> windowedSerializer = new TimeWindowedSerializer<>(stringSerializer);
        TimeWindowedDeserializer<String> windowedDeserializer = new TimeWindowedDeserializer<>(stringDeserializer);
        Serde<Windowed<String>> windowSerde = Serdes.serdeFrom(windowedSerializer, windowedDeserializer);

        //Properties configuration for your streams application
        Properties streamsConfiguration = new Properties();
        streamsConfiguration.put(StreamsConfig.APPLICATION_ID_CONFIG, "your unique application id");
        streamsConfiguration.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "list of your bootstrap servers");
        streamsConfiguration.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest or latest as per you application requirement");
        streamsConfiguration.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass().getName());
        streamsConfiguration.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass().getName());
        streamsConfiguration.put(StreamsConfig.DEFAULT_TIMESTAMP_EXTRACTOR_CLASS_CONFIG, WallclockTimestampExtractor.class.getName());

        //JSON serializer and deserializer
        Serializer<JsonNode> jsonSerializer = new JsonSerializer();
        Deserializer<JsonNode> jsonDeserializer = new JsonDeserializer();
        Serde<JsonNode> jsonSerde = Serdes.serdeFrom(jsonSerializer, jsonDeserializer);
        
        //Commented part to get kafka timestamp in hh:mm:ss format instead of long.

        /*long currentTimeMillis = System.currentTimeMillis();
        DateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        dateFormat.setTimeZone(TimeZone.getTimeZone("UTC"));
        Date date = new Date(currentTimeMillis);
        String currentTime = dateFormat.format(date);*/
        
        StreamsBuilder builder = new StreamsBuilder();
        KStream<String, String> recordstream = builder.stream("input topic name", Consumed.with(Serdes.String(), Serdes.String()));
        
        KStream<String, String> Tstream = recordstream
                .flatMapValues(value -> Arrays.asList(value.toLowerCase().split("\\W+")));
                
        KGroupedStream<String, String> TgroupedStream = Tstream
                .groupBy((key, word) -> word, Grouped.with(Serdes.String(), Serdes.String()));
                
        KTable<Windowed<String>, Long> Ttable = TgroupedStream
                .windowedBy(TimeWindows.of(Duration.ofMinutes(5)))
                .count();
        final ObjectMapper mapper = new ObjectMapper();
        
        Ttable
                .toStream()
                .selectKey((key, word) -> key.key())
                .map((key, value) -> {
                    JsonNode jsonNode = mapper.createObjectNode()
                            .put("data", key)
                            .put("count", value)
                            .put("kafka timestamp", System.currentTimeMillis());
                    return KeyValue.pair(key, jsonNode);
                })
                .to("output topic name", Produced.with(Serdes.String(), jsonSerde));
                
        TgroupedStream.count(Materialized.<String, Long, KeyValueStore<Bytes, byte[]>>as("state store name")
                .withValueSerde(Serdes.Long()));
                
       TgroupedStream
                .windowedBy(TimeWindows.of(Duration.ofMinutes(5)))
                .count(Materialized.<String, Long, WindowStore<Bytes, byte[]>>as("state store name")
                        .withValueSerde(Serdes.Long())
                        .withKeySerde(Serdes.String()))
                .toStream()
                .to("output topic name for window deserialized output", Produced.with(windowSerde, Serdes.Long()));
        KafkaStreams streams = new KafkaStreams(builder.build(), streamsConfiguration);
        streams.start();
        Runtime.getRuntime().addShutdownHook(new Thread(streams::close));
    }
}
