from abc import ABCMeta, abstractmethod


class BaseParser:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_articles(self, tag, count_articles):
        """Постраничное чтение новостей по тегу"""

    @abstractmethod
    def get_new_articles(self, tag):
        """Получение новых статей в риалтайме"""