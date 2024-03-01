import json
from datetime import datetime


class RawNews:
    title = None
    text = None
    web_link = None
    source = None
    news_time = None
    received_time = None
    image_link = None

    def __init__(self, source, title, link, text, time, image):
        self.source = source
        self.title = title
        self.web_link = link
        self.text = text
        self.news_time = time
        self.received_time = str(datetime.utcnow())
        self.image_link = image

    def __str__(self):
        return f'{self.source} {self.title} {self.received_time} {self.news_time} {self.web_link} {self.text}'

    def __repr__(self):
        return str(self)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)
