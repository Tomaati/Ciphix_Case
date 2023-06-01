"""
This module contains the predictor class, which can predict the topic of new conversations using the models created
in model.py
"""
import joblib
import numpy as np

import config
from Backend.Preprocessor import Preprocessor

cleaner = Preprocessor()


class TopicPredictor:
    """
    This class holds the predictor created from the Models as described in Model.py,
    and will allow the users to predict the topics of new conversations.
    """

    def __init__(self, topic_count=10):
        self.topic_count = topic_count
        self.nmf = joblib.load(f'{config.ROOT_DIR}/models/nmf.joblib')
        self.vector = joblib.load(f'{config.ROOT_DIR}/models/vector.joblib')

        self.topics = []
        self.init_topics()

    def init_topics(self):
        for topic in self.nmf.components_:
            # Sort the topics in reversed order to get the most important first
            reverse_sorted = topic.argsort()[::-1][:self.topic_count]
            # Map to the correct words from the vector
            important_features = [self.vector.get_feature_names_out()[i] for i in reverse_sorted]

            # Add the string to the final result
            self.topics.append(' '.join(important_features))

    def predict_topic(self, data):
        data = cleaner.preprocess_solo(data.strip())
        vector = self.vector.transform(data)
        nmf = self.nmf.transform(vector)

        topic = np.argmax(nmf)

        return topic

    def predict(self, text):
        return text, self.predict_topic(text)

    def predict_list(self, text_list):
        return [self.predict(x) for x in text_list]
