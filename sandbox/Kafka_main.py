# -*- coding: cp1251 -*-
#!/usr/bin/env python3

from kafka import KafkaProducer, KafkaConsumer
from json import dumps, loads
import faust
import asyncio
from asyncio import sleep as asleep
import time

async def producer_main():
    '''
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                             value_serializer=lambda x: dumps(x).encode('utf-8'))

    data = {'app-data1': 'test app consumer'}
    producer.send('TestTopic', value=data)
    producer.close()
    print('Finish producer')'''


    class Test(faust.Record):
        msg: str

    app = faust.App('myapp', broker='localhost:9092')
    source_topic = app.topic('TestTopic', value_type=Test)
    destination_topic = app.topic('test_2_topic', value_type=Test)

    @app.agent(source_topic, sink=[destination_topic])
    async def hello(messages):
        async for message in messages:
            if message is not None:
                print(f'Get stream message = {message}')
                # the yield keyword is used to send the message to the destination_topic
                yield Test(msg='This message is from the AGENT')

                # sleep for 2 seconds
                await asleep(2)

    while True:
        print('Iteration')
        await asleep(10)

    '''
    consumer = KafkaConsumer('test_2_topic', bootstrap_servers=['localhost:9092'],
                             auto_offset_reset='earliest',
                             enable_auto_commit=True,
                             group_id='TestGroupApp')

    for message in consumer:
        if message is not None:
            print(f'Final message {message}')

    consumer.close()'''
    print('Finish')


if __name__ == '__main__':
    app.main()
