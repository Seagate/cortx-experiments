# Sample code for consumer subscribed to topic 'test' 

from confluent_kafka import Consumer

def commit_completed(err, partitions):
    if err:
        print(str(err))
    else:
        print("Committed partition offsets: " + str(partitions))


c = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'mygrp',
    # 'on_commit': commit_completed
})

c.subscribe(['test'])

while True:
    msg = c.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue

    print('Received message: {}'.format(msg.value().decode('utf-8')))

c.close()