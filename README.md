# Readme

## Exploratory Data Analysis
From Exploratory Data Analysis it became clear that:
* `df.head()`, `df.tail()`, and `df.sample()` shows that the items represented in the dataset are tweets sent between customers and a company's support team.
* There are `29156` duplicate tweets according to `df.duplicated().sum()`
* Messages contained various 'useless' characters, such as handles, tags, smileys, or URLs, these can easily be removed, while still keeping the main information of the tweet intact.
* Some messages end with a tag, such as ^, *, or - which often shows who wrote the message. This means that these tags can also be removed from the text.
* Some messages carry very little information due to their word count
* Some messages are in different languages, since NLP is best when looking at english text the different languages can
  be removed.

## Front-End

## Back-End
In order for the Front-End to properly work it is important to have a fast and responsive Back-End. This Back-End is used for both training and classification purposes. But since the Front-End focuses on classification, the training has been done beforehand.
### Important Steps for Pre-Processing
After the quick round of EDA it is important to look at the data and see what can be removed and/or adapted in order to
have clean data to work with. From EDA it became clear that the following had to be done in order to clean the data for
the NLP and ML pipeline to work efficiently.

* Look at all the different user tags, and decide which are companies and which are users. For this example it is
  assumed that the tweets with **@\<numerical\>** are tweets sent by a company to the user with **@\<numerical\>**, so
  these tweets can be removed.
* Remove all 'useless' characters using the `DataCleaner.py` script.
* Remove all duplicate tweets.

For this preprocessing step regex was used, since it turned out to be way quicker than cleaning with SpaCy, # How much?,
and resulted in a good enough baseline to continue with.

#### Methods for Speeding up the Pre-Processing
* Filter Optimization
    * Using Regex to filter before trying to run Spacy to lemmatize/filter
* Minimize the use of apply
* ...

### Important Steps for Creating Model
For creating a model it is very important to understand the various different models that could be used for topic classification.

First we have to decide on what type of Vectorizer to use, scikit-learn contains various vectorizers, such as:
* `CountVectorizer`, which converts a collection of text documents to a matrix of word counts.
* `TfidfVectorizer`, which converts a collection of text documents to a matrix of TF-IDF features.
* `HashingVectorizer`, which converts a collection of text documents to a matrix of word occurences.

The `HashingVectorizer` performs best on very large datasets, since it does not rely on a vocabulary (or library) to count, but this also means that you have no use for the resulting dictionary of tokens. `TF-IDF` penalises the words that appear more frequent in the entire dataset, but this is not useful when deciding on what terms came across the most.
Because of these reasons `CountVectorizer` was chosen for this case, since the dataset is not too big, and `TF-IDF` is not useful because we should be dealing with raw counts.

After this we have to decide on what type of model to use for this case, various of these models are described in:
>Egger, R., & Yu, J. (2022). A Topic Modeling Comparison Between LDA, NMF, Top2Vec, and BERTopic to Demystify Twitter Posts. In Frontiers in Sociology (Vol. 7). Frontiers Media SA. https://doi.org/10.3389/fsoc.2022.886498 

According to this paper it is best to use `NMF`, since both `BERTopic` and `Top2Vec` require prior knowledge of the dataset ((semi-)supervised learning) and `LDA` performed worse than `NMF` on short tweets and requires a lot of hyperparameter tuning in order to work optimally.

After creating the model it is important to also save it, so it can be re-used later on for determining the topics of new conversations, in order to do this the `joblib` package was used, since it is advised to used by the `scikit-learn` documentation because the other widely used package `pickle` often is slower for very large arrays.

#### Methods for Speeding up the Model Creation
* Hyperparameter Tuning

### Important Steps for New Conversation Classification

#### Methods for Speeding up the Model Creation