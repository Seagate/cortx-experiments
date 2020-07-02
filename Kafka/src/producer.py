# Sample code for producer to publish messages to topic 'test' 

from confluent_kafka import Producer

p = Producer({'bootstrap.servers': 'localhost:9092'})

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

for loop in range(10):
    p.produce('test', 'Test Msg ' + str(loop), callback=delivery_report)

p.flush()
