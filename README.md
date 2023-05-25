# Readme

From EDA it became clear that:
* `df.head()`, `df.tail()`, and `df.sample()` show that every item starts with an **@**.
* There are `29156` duplicate tweets according to `df.duplicated().sum()`
* Messages contained various 'useless' characters, such as handles, tags, smileys, or URLs, these can easily be removed, while still keeping the main information of the tweet intact.
* Some messages end with a tag, such as ^, *, or - which often shows who wrote the message. This means that these tags can also be removed from the text.
* Some messages carry very little information due to their word count
* Some messages are in different languages, since NLP is best when looking at english text the different languages can be removed.

## Important Steps for Preprocessing
After the quick round of EDA it is important to look at the data and see what can be removed and/or adapted in order to have clean data to work with. From EDA it became clear that the following had to be done in order to clean the data for the NLP and ML pipeline to work efficiently.
* Look at all the different user tags, and decide which are companies and which are users. For this example it is assumed that the tweets with **@\<numerical\>** are tweets sent by a company to the user with **@\<numerical\>**, so these tweets can be removed. 
* Remove all 'useless' characters using the `DataCleaner.py` script.
* Remove all duplicate tweets.

For this preprocessing step regex was used, since it turned out to be way quicker than cleaning with SpaCy, # How much?, and resulted in a good enough baseline to continue with.