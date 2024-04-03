import random
import faust
import logging

app = faust.App('message_predictor', broker='kafka://localhost:9092', key_serializer='json', value_serializer='json')

log = logging.getLogger(__name__)


class PredictedMessage(faust.Record, serializer='json'):
    msg: str
    type: str


topic = app.topic('TestProcessedData')
destination_topic = app.topic('TestPredictedData', value_type=PredictedMessage)


@app.agent(topic, sink=[destination_topic])
async def hello(messages):
    async for message in messages:
        msg_type = 'music' if random.random() > 0.5 else 'sport'
        data = PredictedMessage(msg=message, type=msg_type)
        log.info(message + ' ' + msg_type)
        yield data

'''
@app.timer(interval=5.0)
async def example_sender():
    await hello.send(
        value=Test(msg='Hello World!'),
    )
'''

if __name__ == '__main__':
    app.main()