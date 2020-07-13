from confluent_kafka import Consumer
import datetime

def commit_completed(err, partitions):
    if err:
        print(str(err))
    else:
        print("Committed partition offsets: " + str(partitions))


c = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'mygrp',
    # 'auto.offset.reset': 'earliest',
    'isolation.level' : 'read_committed',
    # 'on_commit': commit_completed,
    # 'request.timeout.ms' : 10,
    # 'auto.commit.interval.ms' : 10000,
    'enable.auto.commit' : False
})

c.subscribe(['perftest'])

msg_count = 0

while True:
    msg = c.poll(0.01)

    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue
    else:
        msg_count += 1
        print(msg_count)
        
        # recd = datetime.datetime.now()
        # timestamp = str(msg.timestamp())[4:-1]
        # sent = datetime.datetime.fromtimestamp(float( timestamp[:10] + '.' + timestamp[10:] ))
        # delta = recd - sent
        # f = open('./Performance/DeliveryLatency.csv',"a")
        # f.write('sent: ' + str(sent) + ',\trecd: ' + str(recd) + ',\ttimediff: ' + str(delta) + '\n')
        # f.close()

        c.commit()

c.close()