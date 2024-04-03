import sys
import datetime
import time

from kafka import KafkaProducer
from json import dumps

args = sys.argv[1:]
feederName = args[0]

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: dumps(x).encode('utf-8'))

while True:
    message = f'{feederName} {datetime.datetime.now()}'
    kafka_massage = f'{feederName}: {message}'
    producer.send('TestRawData', value=kafka_massage)

    print(message)
    time.sleep(30)
