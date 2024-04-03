import os
import joblib
import numpy as np

from sklearn import svm

from .DatabaseManager import DatabaseManager
from .TextManager import TextProcessor, TextManager
from ..APIparsers.ApiModels import ArticleTagsEnum


class SvmManager:
    _tags = None
    _adapters = None
    _c_vector = None
    _sigma_vector = None
    _precision_vector = None

    _text_processor = TextProcessor()
    _text_manager = TextManager()
    _database_manager = DatabaseManager()

    def __init__(self, *args):
        self._tags = args
        self._adapters = [SvmAdapter(tag) for tag in args]

        self._c_vector = np.zeros(len(args))
        self._sigma_vector = np.zeros(len(args))
        self._precision_vector = np.zeros(len(args))

        self._database_manager.create_connection("localhost", "root", "123qwe!", "newsbase")
        self.create_tables()
        print('SvmManager has been creating')

    def get_train_data(self, articles_count, features_count, shift_articles=0, save=False, dicts=None):
        X = None
        Y = None

        for tag, adapter, dict in zip(self._tags, self._adapters, dicts):
            print(tag, articles_count)
            _, texts = self._text_manager.get_articles(tag, articles_count)
            new_x, current_dict = self._text_processor.process_articles(texts[shift_articles:], features_count, dict)
            new_y = adapter.get_label_matrix(new_x, len(ArticleTagsEnum))
            X = self.add_rows(X, new_x)
            Y = self.add_rows(Y, new_y)

            if save:
                np_texts_array = np.array_split(np.array(texts), 50)
                np_x_array = np.array_split(new_x, 50)
                np_y_array = np.array_split(new_y, 50)

                #adapter.save_dictionary(current_dict)

                for nt, nx, ny in zip(np_texts_array, np_x_array, np_y_array):
                    self._database_manager.add_new_articles(tag, nt, nx, ny)

        return X, Y

    def train_adapters(self, X, Y, C_coef, sigma_arr):
        for tag, adapter, sigma_coef in zip(self._tags, self._adapters, sigma_arr):
            adapter.train_svm(X, Y[:, tag.value], C_coef, sigma_coef)
            print("Adapter {} has been fitting".format(tag))

    def check_train_adapters(self, Xval, Yval):
        for i, adapter in enumerate(self._adapters):
            current_precision = adapter.check_validation_svm(Xval, Yval[:, self._tags[i].value])
            if self._precision_vector[i] < current_precision:
                self._precision_vector[i] = current_precision
                self._c_vector[i] = adapter.C_coef
                self._sigma_vector[i] = adapter.sigma_coef

    def predict_article(self, text, dicts):
        answer = ArticleTagsEnum.all
        for tag, adapter, current_dict in zip(self._tags, self._adapters, dicts):
            x = self._text_processor.process_text(text, current_dict)
            if adapter.predict(x) == 1:
                answer = tag
        return answer

    def save_all_states(self):
        for adapter in self._adapters:
            adapter.save_svm_state()

    def load_all_svm_states(self):
        for adapter in self._adapters:
            adapter.load_svm_state()

    def load_add_svm_dicts(self):
        return [adapter.load_dictionary() for adapter in self._adapters]

    def create_tables(self):
        for tag in self._tags:
            self._database_manager.create_table(tag)

    @staticmethod
    def add_rows(matrix, new_matrix):
        return new_matrix if matrix is None else np.vstack([matrix, new_matrix])


class SvmAdapter:
    _svm = None
    _current_tag = ArticleTagsEnum.all

    C_coef = 0
    sigma_coef = 0

    def __init__(self, tag):
        self._current_tag = tag

    def train_svm(self, x, y, C_coef, sigma_coef):
        self.C_coef = C_coef
        self.sigma_coef = sigma_coef
        self._svm = svm.SVC(C=C_coef, gamma=sigma_coef)
        self._svm.fit(x, y)
        return self._svm

    def check_validation_svm(self, x, y):
        y_predict = self._svm.predict(x)
        good = 0
        for i, predict in enumerate(y_predict):
            if predict == y[i]:
                good += 1
        print("{} SVM Predict: ".format(self._current_tag), good, "Total: ", len(y), "{}%".format(good / len(y) * 100.0))
        return good / len(y) * 100

    def predict(self, x):
        return self._svm.predict(x)

    def get_label_matrix(self, matrix, labels_count):
        label_matrix = np.zeros((len(matrix), labels_count))
        label_matrix[:, self._current_tag.value] = 1
        return label_matrix

    def save_svm_state(self):
        joblib.dump(self._svm, self.get_cache_path(self._current_tag))

    def save_dictionary(self, dictionary):
        joblib.dump(dictionary, self.get_dictionary_path(self._current_tag))

    def load_svm_state(self):
        self._svm = joblib.load(self.get_cache_path(self._current_tag))

    def load_dictionary(self):
        return joblib.load(self.get_dictionary_path(self._current_tag))

    @staticmethod
    def get_dictionary_path(tag):
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), "CacheModels", "Dictionaries", "{}_dict.plk".format(tag.name))

    @staticmethod
    def get_cache_path(tag):
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), "CacheModels", "{}.pkl".format(tag.name))
