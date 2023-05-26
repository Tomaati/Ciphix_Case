"""
This module contains the main functions used to find the relevant topics from customers.
"""
import time

import pandas as pd
from pick import pick

import config
from Model import TopicModel
from Predictor import TopicPredictor
from Preprocessor import Preprocessor


def pre_process(data):
    """
    This method prepares the data for training and modeling.
    :param data: The data to process.
    :return: The processed data.
    """
    data = data['Text'].str.extract(r'@([^ ]+)(.*)')
    data = pd.DataFrame(list(zip(data[0], data[1])), columns=['Tag', 'Text']).dropna(subset='Text')

    # Remove useless punctuation from the username
    data['Tag'] = data['Tag'].str.replace(r'[^\w\s]', '', regex=True)

    # Remove all duplicate rows to speed up all further calculations
    data.drop_duplicates()

    preprocessor = Preprocessor(data)

    print(preprocessor.data['Preprocessed'])

    return preprocessor.data


def train_model(data):
    """
    This method trains a model for predicting the top 10 topics from the dataset.
    :param data: The data to process.
    """
    data = pre_process(data)
    modeller = TopicModel(data)
    # Save the model
    if not config.DEBUG:
        modeller.save_model()


if __name__ == '__main__':
    title = 'Please choose what you want to do:'
    options = ['Only Pre-Process', 'Pre-Process and Model', 'Classify Data']
    option, index = pick(options)

    print(f'Okay, starting {option} with debug {"on" if config.DEBUG else "off"}...')

    start_time = time.time()

    # Preprocess the data
    if index == 0:
        nrows = 1000 if config.DEBUG else None
        df = pd.read_csv(f'{config.ROOT_DIR}\\data\\data.csv', header=None, names=['Text'], nrows=nrows)
        df = pre_process(df)

    # Model the data
    if index == 1:
        nrows = 1000 if config.DEBUG else None
        df = pd.read_csv(f'{config.ROOT_DIR}\\data\\data.csv', header=None, names=['Text'], nrows=nrows)
        train_model(df)

    # Predict new data
    if index == 2:
        text = input('What text do you want to check? ')
        df = pre_process(pd.DataFrame([text], dtype=str, columns=['Text']))

        test = TopicPredictor().predict_topic(df)

    print(f'\nMy program took {time.time() - start_time} seconds to run.')
