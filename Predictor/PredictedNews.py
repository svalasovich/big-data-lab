import faust

from enum import Enum
from typing import Dict, List
from faust.models.fields import IntegerField


class TagsEnum(Enum):
    sport = 0,
    economy = 1,
    science = 2,
    musics = 3,
    films = 4,
    politics = 5


class PredictedNews(faust.Record, serializer='json'):
    source: str = None
    title: str = None
    web_link: str = None
    text: str = None
    news_time: str = None
    received_time: str = None
    image_link: str = None
    tags: List[str] = []

    def apply_predicted_news(self, predicted_news):
        self.source = predicted_news.source
        self.title = predicted_news.title
        self.web_link = predicted_news.web_link
        self.text = predicted_news.text
        self.news_time = predicted_news.news_time
        self.received_time = predicted_news.received_time
        self.image_link = predicted_news.image_link
        self.tags = []
        return self


class ProcessedNews(faust.Record, serializer='json'):
    _SHORT_TEXT_LENGTH: int = IntegerField(default=200, exclude=True, required=False)

    source: str = None
    title: str = None
    web_link: str = None
    text: str = None
    news_time: str = None
    received_time: str = None
    image_link: str = None
    learn_vectors: Dict[str, List[bool]] = {}