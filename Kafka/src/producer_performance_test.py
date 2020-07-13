from confluent_kafka import Producer
import os
import datetime
import time
import sys

print(str(sys.argv[1]))
p = Producer({'bootstrap.servers': 'localhost:9092',
              'request.required.acks' : 'all',
              'client.id' : 'PythonClient',
              'transactional.id' : 'p' + str(sys.argv[1]),
            #   'linger.ms' : 100,
            #   'delivery.timeout.ms' : 110,
              'max.in.flight.requests.per.connection' : 5,
              'enable.idempotence' : True
})

print("Enter topic : ")
topicfile = input()
file = open('test',"r")
lines = file.readlines()

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

p.init_transactions()
starttime = datetime.datetime.now()
for loop in range(65536):
    p.begin_transaction()
    p.produce(topicfile,lines[0])
    p.commit_transaction()
endtime = datetime.datetime.now()

# time.sleep(5)

# for loop in range(1000):
#     p.begin_transaction()
#     p.produce(topicfile, str(datetime.datetime.timestamp(datetime.datetime.now())))
#     p.commit_transaction()
# endtime = datetime.datetime.now()
f = open('./Performance/Throughput','a')
f.write('Time for 64k msgs = ' + str(endtime-starttime) + '\n')
f.close()

p.flush()
