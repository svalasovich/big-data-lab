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

    def apply_raw_news(self, raw_news):
        self.source = raw_news['source']
        self.title = raw_news['title']
        self.web_link = raw_news['web_link']
        self.text = raw_news['text'][:self._SHORT_TEXT_LENGTH] + '...'
        self.news_time = raw_news['news_time']
        self.received_time = raw_news['received_time']
        self.image_link = raw_news['image_link']
        return self

    def add_learn_vector(self, tag, vector):
        self.learn_vectors[tag] = list(vector)
