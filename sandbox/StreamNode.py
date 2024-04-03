import faust
import logging
from asyncio import sleep

log = logging.getLogger(__name__)


class Test(faust.Record):
    msg: str


app = faust.App('StreamNode', broker='kafka://localhost:9092')
source_topic = app.topic('TestTopic', value_type=Test)
destination_topic = app.topic('test_2_topic', value_type=Test)


# specify the source_topic and destination_topic to the agent
@app.agent(source_topic, sink=[destination_topic])
async def hello(messages):
    async for message in messages:
        if message is not None:
            log.info(message.msg)

            # the yield keyword is used to send the message to the destination_topic
            yield Test(msg='This message is from the AGENT')

            # sleep for 2 seconds
            await sleep(2)
        else:
            log.info('No message received')


if __name__ == '__main__':
    app.main()