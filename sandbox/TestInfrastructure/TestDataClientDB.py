import time
import json

from kafka import KafkaConsumer
from pymongo import MongoClient


CONNECTION_STRING = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"

consumer = KafkaConsumer('TestPredictedData', bootstrap_servers=['localhost:9092'],
                         enable_auto_commit=True,
                         group_id='Client_DB',
                         value_deserializer=lambda x: x.decode('utf-8'))

db_client = MongoClient(CONNECTION_STRING)
test_collections = db_client['test_db']['test_collection']

test_collections.delete_many({})

while True:
    for message in consumer:
        if message is not None:
            print(message.value)
            test_collections.insert_one(json.loads(message.value))
            #data = message.value.split(':')
            #print(f'Data received: {data}')
            #test_collections.insert_one({
            #    'instance': data[0],
            #    'message': ''.join(str(x) for x in data[1:]),
            #})

    time.sleep(10)
    print('.')
