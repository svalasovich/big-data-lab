import time

from kafka import KafkaConsumer
from json import loads

consumer = KafkaConsumer('PredictedNewsCollection',
                         bootstrap_servers=['localhost:9092'],
                         auto_offset_reset='earliest',
                         enable_auto_commit=True,
                         group_id='console_client',
                         value_deserializer=lambda x: loads(x.decode('utf-8')))

while True:
    for message in consumer:
        if message is not None:
            print(message.value)
        else:
            print('.')
    time.sleep(10)
