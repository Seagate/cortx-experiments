package org.apache.kafka;

        import org.apache.kafka.clients.consumer.KafkaConsumer;
        import org.apache.kafka.clients.consumer.ConsumerRecords;
        import org.apache.kafka.clients.consumer.ConsumerRecord;

        import java.time.Duration;
        import java.util.Collections;
        import java.util.Properties;

public class ConsumerScript
{
    public static void main(String[] args)
    {
        KafkaConsumer<String, String> consumer;
        Properties pop = new Properties();
        pop.setProperty("bootstrap.servers", "list of bootstrap servers");
        pop.setProperty("group.id", "unique group id");
        pop.setProperty("key.deserializer","org.apache.kafka.common.serialization.StringDeserializer");
        pop.setProperty("value.deserializer","org.apache.kafka.common.serialization.StringDeserializer");
        pop.setProperty("auto.offset.reset","latest");

        consumer = new KafkaConsumer<>(pop);
        consumer.subscribe(Collections.singletonList("topic name from which you will consume records"));

        int count = 0;
        while(true) {
            ConsumerRecords<String, String> records = consumer.poll(Duration.ofMinutes(5));
            if (records.count() == 0) {
            } else {
                for(ConsumerRecord<String, String> record: records) {
                    count += 1;
                    System.out.println( count + ": " + record.value());
                }
            }
        }
    }
}
