"""
This module contains the main functions used to find the relevant topics from customers.
"""
import time

import pandas as pd

import config
from Model import TopicModel
from Preprocessor import Preprocessor

if __name__ == '__main__':
    start_time = time.time()
    nrows = 1000 if config.DEBUG else None
    df = pd.read_csv(f'{config.ROOT_DIR}\\data\\data.csv', header=None, names=['Text'], nrows=nrows)

    # Create a readable dataframe containing username and text
    df = df['Text'].str.extract(r'@([^ ]+)(.*)')
    df = pd.DataFrame(list(zip(df[0], df[1])), columns=['Tag', 'Text']).dropna(subset='Text')

    # Remove useless punctuation from the username
    df['Tag'] = df['Tag'].str.replace(r'[^\w\s]', '', regex=True)

    # Remove all duplicate rows to speed up all further calculations
    df.drop_duplicates()

    preprocessor = Preprocessor(df)

    print(preprocessor.data['Preprocessed'])

    modeller = TopicModel(preprocessor.data)
    topic_classes = modeller.find_topics()

    print(topic_classes)
    print(f'\n My program took {time.time() - start_time} seconds to run.')
