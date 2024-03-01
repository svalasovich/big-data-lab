from pprint import pprint
from enum import Enum
from pymongo import MongoClient
from datetime import datetime


class TagsEnum(Enum):
    all = 0,
    sport = 1,
    economy = 2,
    science = 3,
    musics = 4,
    films = 5,
    politics = 6


class DatabaseClient:
    _CONNECTION_STRING = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"

    def __init__(self):
        self._db_client = MongoClient(self._CONNECTION_STRING)
        self._news_collection = self._db_client['wnews_db']['predicted_news']

    def load_news(self, feeder_name, tag='all', count=100):
        query = {
            'source': feeder_name,
            'tags': {"$in": [tag]}
        }
        articles = self._news_collection.find(query).limit(count)
        return [ArticleModel(item) for item in articles]


class ArticleModel:
    _DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"

    def __init__(self, db_item):
        self.title = db_item['title']
        self.text = db_item['text']
        self.article_link = db_item['web_link']
        self.image_link = db_item['image_link']
        self.last_update = datetime.strptime(db_item['news_time'], self._DATETIME_FORMAT)
