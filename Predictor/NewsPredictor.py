import os
import joblib
import numpy as np

from PredictedNews import PredictedNews, TagsEnum


class SvmPredictor:
    def __init__(self, tag):
        self._svm = joblib.load(SvmPredictor._get_trained_model_path(tag))

    def predict(self, x):
        return self._svm.predict(np.array(x).reshape(1, -1))

    @staticmethod
    def _get_trained_model_path(tag):
        return os.path.join(os.path.dirname(os.path.realpath(__file__)),
                            "..",
                            "SvmTrainedModels",
                            f"{tag}.pkl")


class NewsPredictor:
    def __init__(self):
        self._svmModels = {}
        for tag in TagsEnum:
            self._svmModels[tag.name] = SvmPredictor(tag.name)

    def predict_news(self, news):
        predicted_news = PredictedNews().apply_predicted_news(news)

        for tag in TagsEnum:
            predictor = self._svmModels[tag.name]
            x_vector = news.learn_vectors[tag.name]
            if predictor.predict(x_vector) == 1:
                predicted_news.tags.append(tag.name)

        if len(predicted_news.tags) == 0:
            predicted_news.tags.append('all')

        return predicted_news
