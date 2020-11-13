package org.apache.kafka;

import java.io.IOException;
import java.time.Instant;
import java.util.Properties;
import java.util.Random;

import com.fasterxml.jackson.databind.node.JsonNodeFactory;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.Producer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.StringSerializer;

public class Prodx
{
    public static void main(String[] args) throws IOException
    {
        Properties props = new Properties();

        props.setProperty(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "list of bootstrap servers, example: server name:9200");
        props.setProperty(ProducerConfig.ACKS_CONFIG, "all");
        props.setProperty(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        props.setProperty(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());

        Producer<String, String> producer = new KafkaProducer<>(props);

        Random ran = new Random();
        String[] sentences = new String[] {
                "conrad marriott grand hyatt",
                "novotel holidayinn westin",
                "corinthians ramee",
                "radisson sheratton oxford"
        };

        while (true){
            String sentence = sentences[ran.nextInt(sentences.length)];
            try
            {
                producer.send(new ProducerRecord<String, String>("to topic which will be input topic for your streams application", sentence)).get();
            }
            catch (Exception ex)
            {
                System.out.print(ex.getMessage());
                throw new IOException(ex.toString());
            }
        }

    }
}
