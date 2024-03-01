import requests
from datetime import datetime, timedelta
from BaseFeeder import BaseFeeder
from Models.Models import RawNews


class TheNYTimesFeeder(BaseFeeder):
    _API_SOURCE = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'
    _API_KEY = 'nQnmGmGuvIhGcnLChoLoKRVRuCuB3buG'
    _SOURCE_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    _page_number = -1

    def request_to_source(self):
        self._page_number += 1
        return requests.get(
            self._API_SOURCE,
            params={
                "api-key": self._API_KEY,
                "source": "The New York Times",
                "sort": "newest",
                "fq": "The New York Times",
                "page": self._page_number
            }
        ).json()

    def get_news_items(self, response):
        return response['response']['docs'] if 'docs' in response['response'] else None

    def convert_to_raw_news(self, source_response):
        news = []
        for item in source_response:
            n = RawNews(source="TheNewYorkTimes",
                        title=item['headline']['main'],
                        link=item['web_url'],
                        text=f'{item["snippet"]} {item["lead_paragraph"]}',
                        time=item['pub_date'][:-5],
                        image=None)
            if 'multimedia' in item and len(item['multimedia']) > 0:
                n.image_link = "https://static01.nyt.com/" + item['multimedia'][0]['url']
            news.append(n)
        return news


timesFeeder = TheNYTimesFeeder(update_time=60)
timesFeeder.start()
