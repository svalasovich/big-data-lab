import requests
from datetime import datetime, timedelta
from BaseFeeder import BaseFeeder
from Models.Models import RawNews


class TheGuardianFeeder(BaseFeeder):
    _API_SOURCE = 'http://content.guardianapis.com/search'
    _API_KEY = '5dd8bff4-9d3a-43c5-8526-5743161d4992'
    _SOURCE_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    def request_to_source(self):
        return requests.get(
            self._API_SOURCE,
            params={
                "api-key": self._API_KEY,
                #"from-date": (datetime.utcnow() - timedelta(seconds=self._update_time)).strftime(self._SOURCE_DATETIME_FORMAT),
                "order-by": "newest",
                "show-fields": "bodyText,thumbnail",
                "page-size": 100,
                "page": 1,
            }
        ).json()['response']

    def get_news_items(self, response):
        return response['results'] if 'results' in response else None

    def convert_to_raw_news(self, source_response):
        news = []
        for item in source_response:
            n = RawNews(source="TheGuardian",
                        title=item['webTitle'],
                        link=item['webUrl'],
                        text=item['fields']['bodyText'],
                        image=item['fields']['thumbnail'],
                        time=item['webPublicationDate'][:-1],)
            news.append(n)
        return news


guardianFeeder = TheGuardianFeeder(update_time=60)
guardianFeeder.start()
