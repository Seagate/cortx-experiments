package org.apache.kafka;

import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.common.serialization.Serde;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.kafka.common.serialization.StringSerializer;
import org.apache.kafka.streams.kstream.TimeWindowedDeserializer;
import org.apache.kafka.streams.kstream.TimeWindowedSerializer;
import org.apache.kafka.common.utils.Bytes;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.kstream.*;
import org.apache.kafka.streams.state.KeyValueStore;
import org.apache.kafka.streams.state.WindowStore;

import java.time.Duration;
import java.util.Arrays;
import java.util.Properties;

public class TumblingWindow {

    public static void main(String[] args) {

        StringSerializer stringSerializer = new StringSerializer();
        StringDeserializer stringDeserializer = new StringDeserializer();
        TimeWindowedSerializer<String> windowedSerializer = new TimeWindowedSerializer<>(stringSerializer);
        TimeWindowedDeserializer<String> windowedDeserializer = new TimeWindowedDeserializer<>(stringDeserializer);
        Serde<Windowed<String>> windowSerde = Serdes.serdeFrom(windowedSerializer, windowedDeserializer);

        Properties streamsConfiguration = new Properties();
        streamsConfiguration.put(StreamsConfig.APPLICATION_ID_CONFIG, "GTA");
        streamsConfiguration.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "ssc-vm-c-0333.colo.seagate.com:9092, ssc-vm-c-0332.colo.seagate.com:9092, ssc-vm-0789.colo.seagate.com:9092");
        streamsConfiguration.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        streamsConfiguration.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass());
        streamsConfiguration.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass());

        StreamsBuilder builder = new StreamsBuilder();
        KStream<String, String> initialstream = builder.stream("TextLinesTopic", Consumed.with(Serdes.String(), Serdes.String()));

        KStream<String, String> Tstream = initialstream
                .flatMapValues(value -> Arrays.asList(value.toLowerCase().split("\\W+")));

        KGroupedStream<String, String> TgroupedStream = Tstream
                .groupBy((key, word) -> word, Grouped.with(Serdes.String(), Serdes.String()));

        KTable<Windowed<String>, Long> Ttable = TgroupedStream
                .windowedBy(TimeWindows.of(Duration.ofMinutes(5)))
                .count();
        Ttable
                .toStream()
                .selectKey((key, word) -> key.key())
                .to("tumblingoutputtopic", Produced.with(Serdes.String(), Serdes.Long()));

        TgroupedStream.count(Materialized.<String, Long, KeyValueStore<Bytes, byte[]>>as("simple-word-count")
                .withValueSerde(Serdes.Long()));

        TgroupedStream
                .windowedBy(TimeWindows.of(Duration.ofMinutes(5)))
                .count(Materialized.<String, Long, WindowStore<Bytes, byte[]>>as("tumbling-window-count")
                        .withValueSerde(Serdes.Long())
                        .withKeySerde(Serdes.String()))
                        .toStream()
                .to("tumblingstatestoretopic", Produced.with(windowSerde, Serdes.Long()));

        KafkaStreams streams = new KafkaStreams(builder.build(), streamsConfiguration);
        streams.start();

        Runtime.getRuntime().addShutdownHook(new Thread(streams::close));
    }
}
