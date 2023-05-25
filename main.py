"""
This module contains the main functions used to find the relevant topics from customers.
"""
import os

import pandas as pd

from Preprocessor import Preprocessor

import time

ROOT_DIR = os.path.dirname(__file__)
DEBUG = False

if __name__ == '__main__':
    start_time = time.time()
    nrows = 1000 if DEBUG else None
    df = pd.read_csv(f'{ROOT_DIR}\\data\\data.csv', header=None, names=['Text'], nrows=nrows)

    # Create a readable dataframe containing only the username and text.
    df = df['Text'].str.extract(r'(@([a-zA-Z\d]+)([^\S\r\n]))(.*)')
    df = pd.DataFrame(list(zip(df[1], df[3])), columns=['Tag', 'Text']).dropna(subset='Text')

    # Remove all duplicate rows to speed up all further calculations
    df.drop_duplicates()

    preprocessor = Preprocessor(df)

    print(preprocessor.data['Preprocessed'])
    print(f'\n My program took {time.time() - start_time} seconds to run.')
