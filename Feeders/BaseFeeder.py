import time
from abc import ABCMeta, abstractmethod
from kafka import KafkaProducer


class BaseFeeder:
    __metaclass__ = ABCMeta

    def __init__(self, update_time=60):
        self._update_time = update_time
        self._producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                                       value_serializer=lambda x: x.toJSON().encode('utf-8'))

    @abstractmethod
    def request_to_source(self):
        "Запрос к источнику"

    @abstractmethod
    def get_news_items(self, response):
        "Получить массив новостей из запроса"

    @abstractmethod
    def convert_to_raw_news(self, source_response):
        "Перевод полученных данных в NewRaw модель"

    def start(self):
        while True:
            source_response = self.request_to_source()
            if source_response['status'].lower() == 'ok':
                items = self.get_news_items(source_response)
                print(items)
                if items is not None and len(items) > 0:
                    news = self.convert_to_raw_news(items)
                    for ne in news:
                        self._producer.send("RawNewsCollection", value=ne)
            time.sleep(self._update_time)

