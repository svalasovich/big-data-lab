import requests

from datetime import datetime, timedelta
from .ApiModels import ArticleModel
from .BaseParser import BaseParser


class TheGuardianParser(BaseParser):
    _MAX_PAGE_SIZE = 50
    _API_SOURCE = 'http://content.guardianapis.com/search'
    _API_KEY = '5dd8bff4-9d3a-43c5-8526-5743161d4992'

    def __init__(self):
        print('Create The Guardian Pasrser succ')

    def get_articles(self, tag, count_articles):
        page_count = count_articles // self._MAX_PAGE_SIZE + (count_articles % self._MAX_PAGE_SIZE > 0)
        articles = []

        for page_number in range(1, page_count + 1):
            response = self._get_response(tag, page_number)
            if response['status'] == 'ok':
                for item_article in response['results']:
                    articles.append(self._json_obj_to_article(item_article))
                    count_articles -= 1
                    if count_articles == 0:
                        break
            else:
                break

        return articles

    def get_new_articles(self, tag):
        articles = []
        response = self._get_response_with_time(tag)
        if response['status'] == 'ok':
            if 'results' in response:
                for item_article in response['results']:
                    articles.append(self._json_obj_to_article(item_article))
        return articles

    @staticmethod
    def _json_obj_to_article(item_article):
        new_article = ArticleModel(
            title=item_article['webTitle'],
            article_link=item_article['webUrl'],
            last_update=item_article['webPublicationDate'],
            text=item_article['fields']['bodyText'])

        if 'thumbnail' in item_article['fields']:
            new_article.image_link = item_article['fields']['thumbnail']

        return new_article

    def _get_response_with_time(self, tag):
        return requests.get(
            self._API_SOURCE,
            params={
                "q": tag.name,
                "from-date": (datetime.utcnow() - timedelta(minutes=5)).strftime(ArticleModel.DATETIME_FORMAT),
                "order-by": "newest",
                "show-fields": "bodyText,thumbnail",
                "api-key": self._API_KEY
            }
        ).json()['response']

    def _get_response(self, tag, page):
        return requests.get(
            self._API_SOURCE,
            params={
                "q": tag.name,
                "order-by": "newest",
                "show-fields": "bodyText,thumbnail",
                "page-size": self._MAX_PAGE_SIZE,
                "page": page,
                "show-tags": "contributor",
                "api-key": self._API_KEY
            }
        ).json()['response']
