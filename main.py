"""
This module contains the main functions used to find the relevant topics from customers.
"""
import time

import pandas as pd
from pick import pick

import config
from Backend.Model import TopicModel
from Backend.Predictor import TopicPredictor
from Backend.Preprocessor import Preprocessor, clean_text


def pre_process_df(data):
    """
    This method prepares the data for training and modeling.
    :param data: The data to process.
    :return: The processed data.
    """
    twitter_handles = data['Text'].str.extract(r'@(\S+)')[0].values
    tweets = data['Text'].str.replace(r'(@\S+)', '', regex=True).values

    data = pd.DataFrame(list(zip(twitter_handles, tweets)), columns=['Tag', 'Text']).dropna(subset=['Tag', 'Text'])

    # Remove useless punctuation from the username
    data['Tag'] = data['Tag'].str.replace(r'[^\w\s]', '', regex=True)

    # Remove all duplicate rows to speed up all further calculations
    data.drop_duplicates()

    return Preprocessor().clean_df(data)


def train_model(data):
    """
    This method trains a model for predicting the top 10 topics from the dataset.
    :param data: The data to process.
    """
    modeller = TopicModel(data)
    # Save the model
    if not config.DEBUG:
        modeller.save_model()


def pre_process(text):
    return Preprocessor().preprocess([clean_text(text)])


def predict(text):
    """
    This method predicts the topics of new conversations.
    :param text: The data to process.
    """
    return text, TopicPredictor().predict_topic(pre_process(text))


def predict_list(text_list):
    processed = [clean_text(text) for text in text_list]
    return text_list, TopicPredictor().predict_list_topic(Preprocessor().preprocess(processed))


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
        pre_process(df)

    # Model the data
    if index == 1:
        nrows = 1000 if config.DEBUG else None
        df = pd.read_csv(f'{config.ROOT_DIR}\\data\\data.csv', header=None, names=['Text'], nrows=nrows)
        train_model(df)

    # Predict new data
    if index == 2:
        text = input('What text do you want to check? ')
        predict(text)

    print(f'\nMy program took {time.time() - start_time} seconds to run.')
