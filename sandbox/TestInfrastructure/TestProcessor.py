import faust
import logging

app = faust.App('message_processor', broker='kafka://localhost:9092', key_serializer='json', value_serializer='json')

log = logging.getLogger(__name__)


class Test(faust.Record):
    msg: str


topic = app.topic('TestRawData')
destination_topic = app.topic('TestProcessedData')


@app.agent(topic, sink=[destination_topic])
async def hello(messages):
    async for message in messages:
        new_message = f'{message}+record has been processed!!!'
        log.info(new_message)
        #await destination_topic.send(value=new_message)
        yield new_message

'''
@app.timer(interval=5.0)
async def example_sender():
    await hello.send(
        value=Test(msg='Hello World!'),
    )
'''

if __name__ == '__main__':
    app.main()