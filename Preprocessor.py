"""
This module is used for cleaning up the tweets, allowing them to properly be analysed using NLP and ML.
"""
import re

import spacy

at_pattern = '@([^ ]+)'
tag_pattern = '[\^\-\*][A-Z\d]+$'
url_pattern = 'https?://\S+|www\.\S+'
newline_pattern = '\n'
special_pattern = '[#\'\"]'

emoji_pattern = re.compile("["
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           u"\U0001F1E0-\U0001F1FF"
                           u"\U0001F300-\U0001F5FF"
                           u"\U0001F600-\U0001F64F"
                           u"\U0001F680-\U0001F6FF"
                           u"\U0001F700-\U0001F77F"
                           u"\U0001F780-\U0001F7FF"
                           u"\U0001F800-\U0001F8FF"
                           u"\U0001F900-\U0001F9FF"
                           u"\U0001FA00-\U0001FA6F"
                           u"\U0001FA70-\U0001FAFF"
                           "]+", flags=re.UNICODE)

generic_re = re.compile('|'.join([at_pattern, tag_pattern, url_pattern, newline_pattern, special_pattern]))


class Preprocessor:
    """
    This class prepares the data for the Machine Learning algorithms that can be used to determine the top 10 topics.
    """

    def __init__(self, df):
        self.model = spacy.load('en_core_web_sm')
        self.data = df

        self.clean_df()

    def clean_df(self):
        self.data['Clean'] = self.data['Text'].apply(clean_text)

        print('Done Cleaning')

        # Check if a username is related to a company or a customer, only keep customers.
        self.data['Is_Employee'] = self.data['Tag'].str.isnumeric()
        self.data = self.data[~self.data['Is_Employee']]

        print('Done Checking Employees')

        # Count the words, and only keep relevant text by removing short tweets.
        min_count = 3
        self.data = self.data[self.data['Clean'].str.split(' ').str.len() > min_count]

        print('Done Checking Word Count')

        # Pre-process the data using Spacy
        self.data['Preprocessed'] = self.preprocess(self.data['Clean'])

        print('Done Preprocessing the data')

    def preprocess(self, text):
        docs = self.model.pipe(text, n_process=10)
        output = []

        for doc in docs:
            lemma = " ".join(
                token.lemma_.strip() for token in doc if (token.pos_ in ['PROPN', 'NOUN', 'VERB']
                                                          and token not in self.model.Defaults.stop_words))
            output.append(lemma.lower())
        return output


def clean_text(text):
    """
    Combines all regex for one cleaning method.
    :param text: The text to check.
    :return: The fully cleaned text.
    """
    # Remove any twitter_handles, tags, urls, newlines, and other special characters.
    text = generic_re.sub(r'', text)

    # Remove any emoji's that can be found in the text.
    text = emoji_pattern.sub(r'', text)

    # Now we want to remove all the other unnecessary characters within the text.
    # Note, this also remove all emojis.
    text = re.findall(r'[^\W\d]+', text)

    return ' '.join(text)
