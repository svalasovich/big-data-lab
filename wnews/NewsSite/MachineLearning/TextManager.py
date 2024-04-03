import re
import nltk
import collections
import numpy as np


from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

from ..APIparsers.TheGuardianParser import TheGuardianParser


class TextManager:
    #_parser = TheGuardianParser()

    def get_articles(self, tag, count):
        articles = self._parser.get_articles(tag, count)
        return articles, [article.full_text for article in articles]

    def get_new_articles(self, tag):
        return self._parser.get_new_articles(tag)


class TextProcessor:
    _html_regs = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    _url_regs = re.compile(
        'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)')
    _email_regs = re.compile('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    _number_regs = re.compile('[0-9.]+')
    _text_regs = re.compile('[#&%+:;\[\]/|><=`()@,\'\"!?\-}{*_\-®•“’”…‘–]')

    _porter_stemmer = None
    _stop_worlds = None

    current_counter = collections.Counter()

    def __init__(self):
        #nltk.download('punkt')
        #nltk.download('stopwords')
        self._porter_stemmer = PorterStemmer()
        self._stop_worlds = set(stopwords.words('english'))

    def process_articles(self, articles, vector_size, dictionary=None):
        self.current_counter.clear()
        matrix = [self._convert_article(article) for article in articles]
        current_dict = [t[0] for t in self.current_counter.most_common(vector_size)] if dictionary is None else dictionary
        return np.array([self._get_features_vector(row, current_dict) for row in matrix]), current_dict

    def process_text(self, text, dictionary):
        return self._get_features_vector(self._convert_article(text), dictionary).reshape(1, -1)

    @staticmethod
    def _get_features_vector(words, dictionary):
        vector = np.zeros(len(dictionary))
        for i, key in enumerate(dictionary):
            if key in words:
                vector[i] = 1
        return vector

    def _convert_article(self, article):
        article = re.sub(self._html_regs, '', article.lower())
        article = re.sub(self._url_regs, 'httpaddr', article)
        article = re.sub(self._email_regs, 'emailaddr', article)
        article = re.sub(self._number_regs, ' number ', article)
        article = article.replace('$', 'dollar ')
        article = re.sub(self._text_regs, '', article)

        filtered_worlds = [w for w in nltk.word_tokenize(article) if w not in self._stop_worlds]

        for i, word in enumerate(filtered_worlds):
            filtered_worlds[i] = self._porter_stemmer.stem(word)
            self.current_counter[filtered_worlds[i]] += 1

        return filtered_worlds
