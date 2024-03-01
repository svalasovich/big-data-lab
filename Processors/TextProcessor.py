import os
import re
import joblib
import nltk
import numpy as np


from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

from ProcessedNews import ProcessedNews, TagsEnum


class TextProcessor:
    _html_regs = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    _url_regs = re.compile(
        'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)')
    _email_regs = re.compile('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    _number_regs = re.compile('[0-9.]+')
    _text_regs = re.compile('[#&%+:;\[\]/|><=`()@,\'\"!?\-}{*_\-®•“’”…‘–]')

    def __init__(self):
        #nltk.download('punkt')
        #nltk.download('stopwords')
        self._porter_stemmer = PorterStemmer()
        self._stop_worlds = set(stopwords.words('english'))

        self._word_dict = {}
        for tag in TagsEnum:
            self._word_dict[tag.name] = TextProcessor._load_word_dictionary(tag)

    def process_raw_news(self, raw_news):
        news = ProcessedNews().apply_raw_news(raw_news)
        processed_text = self._text_stemming(raw_news['text'])

        for tag in TagsEnum:
            news.add_learn_vector(tag.name, self._build_features_vector(processed_text, tag))

        return news

    def _build_features_vector(self, text, tag):
        cur_dict = self._word_dict[tag.name]
        vector = np.zeros(len(cur_dict))
        for i, key in enumerate(cur_dict):
            if key in text:
                vector[i] = 1
        return vector

    def _text_stemming(self, text):
        text = re.sub(self._html_regs, '', text.lower())
        text = re.sub(self._url_regs, 'httpaddr', text)
        text = re.sub(self._email_regs, 'emailaddr', text)
        text = re.sub(self._number_regs, ' number ', text)
        text = text.replace('$', 'dollar ')
        text = re.sub(self._text_regs, '', text)

        simplify_text = [w for w in nltk.word_tokenize(text) if w not in self._stop_worlds]

        for i, word in enumerate(simplify_text):
            simplify_text[i] = self._porter_stemmer.stem(word)

        return simplify_text

    @staticmethod
    def _load_word_dictionary(tag):
        return joblib.load(TextProcessor._get_dictionary_path(tag))

    @staticmethod
    def _get_dictionary_path(tag):
        return os.path.join(os.path.dirname(os.path.realpath(__file__)),
                            "..",
                            "NewsTagDictionaries",
                            f"{tag.name}_dict.plk")
