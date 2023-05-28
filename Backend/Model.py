"""
This module allows for the modeling of the data, which can later be used for predicting important topics.
"""
import joblib
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import CountVectorizer

import config
from Backend.Preprocessor import Preprocessor


class TopicModel:
    """
    This class creates a Model based on the data provided by Ciphix.
    """
    def __init__(self, df, topic_count=10):
        self.df = Preprocessor(df).data
        self.topic_count = topic_count
        self.nmf = NMF(n_components=self.topic_count)
        self.vector = CountVectorizer(min_df=5, max_df=0.9, stop_words='english')

        self.data_vector = self.vector.fit_transform(self.df['Preprocessed'])
        self.data_nmf = self.nmf.fit_transform(self.data_vector)

    def save_model(self):
        joblib.dump(self.nmf, f'{config.ROOT_DIR}\\models\\nmf.joblib')
        joblib.dump(self.vector, f'{config.ROOT_DIR}\\models\\vector.joblib')
