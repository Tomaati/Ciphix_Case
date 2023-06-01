"""
This module contains the main functions used to find the relevant topics from customers.
"""
import time

import pandas as pd

import config
from Backend.Model import TopicModel
from Backend.Predictor import TopicPredictor

if __name__ == '__main__':
    index = int(input('Please decide what you want to do. 1 for Pre-Process and Model, 2 for Classify Data: '))
    start_time = 0

    # Model the data
    if index == 1:
        start_time = time.time()
        df = pd.read_csv(f'{config.ROOT_DIR}\\data\\data.csv', header=None, names=['Text'])
        twitter_handles = df['Text'].str.extract(r'@(\S+)')[0].values
        tweets = df['Text'].str.replace(r'(@\S+)', '', regex=True).values

        data = pd.DataFrame(list(zip(twitter_handles, tweets)), columns=['Tag', 'Text']).dropna(subset=['Tag', 'Text'])

        TopicModel(data).save_model()

    # Predict new data
    if index == 2:
        to_predict = input('What text do you want to check? ')

        start_time = time.time()
        predictor = TopicPredictor()
        text, topic = predictor.predict(to_predict)

        print(f'{text}, has topic {topic}: {predictor.topics[topic]}')

    print(f'\nMy program took {time.time() - start_time} seconds to run.')
