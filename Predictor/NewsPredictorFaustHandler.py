import faust
import logging

from PredictedNews import PredictedNews, ProcessedNews
from Predictor import NewsPredictor


app = faust.App('news_predictor', broker='kafka://localhost:9092', key_serializer='json', value_serializer='json')
log = logging.getLogger(__name__)

base_topic = app.topic('ProcessedNewsCollection', value_type=ProcessedNews)
destination_topic = app.topic('PredictedNewsCollection', value_type=PredictedNews)

news_predictor = NewsPredictor()


@app.agent(base_topic, sink=[destination_topic])
async def news_processing(messages):
    async for processed_news in messages:
        # log.info(processed_news)
        predicted_news = news_predictor.predict_news(processed_news)
        log.info(predicted_news)
        yield predicted_news
