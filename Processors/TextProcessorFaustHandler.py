import faust
import logging

from ProcessedNews import ProcessedNews
from TextProcessor import TextProcessor


app = faust.App('news_processor', broker='kafka://localhost:9092', key_serializer='json', value_serializer='json')
log = logging.getLogger(__name__)

base_topic = app.topic('RawNewsCollection')
destination_topic = app.topic('ProcessedNewsCollection', value_type=ProcessedNews)

text_processor = TextProcessor()


@app.agent(base_topic, sink=[destination_topic])
async def news_processing(messages):
    async for raw_news in messages:
        processed_news = text_processor.process_raw_news(raw_news)
        log.info(processed_news)
        yield processed_news
