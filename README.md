# Readme

* [Running & Deploying](#running-&-deploying)
* [Exploratory Data Analysis](#exploratory-data-analysis)
    * [Loading in the data](#loading-in-the-data)
    * [Explore summarizing values](#explore-summarizing-values)
    * [Company & Customer information](#company--customer-information)
    * [Relevant Sentences](#relevant-sentences)
    * [Conclusion](#conclusion)
* [Back-End](#back-end)
    * [Pre-Processing](#important-steps-for-pre-processing)
    * [Creating Model](#important-steps-for-creating-model)
    * [New Conversation Classification](#important-steps-for-new-conversation-classification)
* [Front-End](#front-end)
    * [Login Page](#login-page)
    * [Admin Dashboard](#admin-dashboard)
    * [Settings](#settings)
    * [General Implementation Strategy](#general-implementation-strategy)
    * [Database Design](#database-design)

## Running & Deploying
The webapp is currently hosted on [ciphix.hhhserver.online](ciphix.hhhserver.online), this is my own server and can only be accesssed from the Netherlands (so check your VPN). It is not the quickest server, but it should give a proper idea on what the webapp will run like.

In order to run the program you can login with `username: admin` & `password: password`.

### Deploy on your own Server or Machine
The webapp can easily be deployed using [Docker](https://www.docker.com/), first make sure it is installed and added to your PATH variable (if on windows).
After that do the following:
```powershell
docker build -t ciphix-topic
docker run -it -p 8000:8000 ciphix-topic
```
After this the docker container should be running and visible when running `docker ps`. You can now visit `127.0.0.1:8000` and login using the information above.

## Exploratory Data Analysis

In order to get a good idea on how to tackle the implementation of topic classification we have to take a quick look at
what type of data we are currently using.

### Loading in the data

Before exploring the data we first need to load it in.

```python
import pandas as pd
import config

df = pd.read_csv(f'{config.ROOT_DIR}\\data\\data.csv', header=None, names=['Text'])
print(df.head().to_string())  # Also try it with .tail() and .sample()
```

| index | Text                                                                                                                         |
|-------|------------------------------------------------------------------------------------------------------------------------------|
| 0     | @115712 I understand. I would like to assist you. We would need to get you into a private secured link to further assist.    |
| 1     | @sprintcare and how do you propose we do that                                                                                |
| 2     | @sprintcare I have sent several private messages and no one is responding as usual                                           |
| 3     | @115712 Please send us a Private Message so that we can further assist you. Just click ‘Message’ at the top of your profile. |
| 4     | @sprintcare I did.                                                                                                           |

From this information it becomes clear that this dataset contains a plethora of tweets sent between customers and
support staff.

### Explore summarizing values

```python
len(df.index)  # 2811774
df.duplicated().sum()  # 29156
# 2782618 distinct values

df["Wordcount"] = df["Text"].str.split().str.len()
df.describe()
```

| Metric | Wordcount |
|--------|-----------|
| count  | 2811774   |
| mean   | 19.45840  |
| std    | 9.618600  |
| min    | 1.000000  |
| 25%    | 13.00000  |
| 50%    | 19.00000  |
| 75%    | 24.00000  |
| max    | 137.0000  |

### Company & Customer information

Let's look a bit better at what type of information is discussed. By first separating the twitter handles from the
tweets they sent.

```python
twitter_handles = df['Text'].str.extract(r'@(\S+)')[0].values
tweets = df['Text'].str.replace(r'(@\S+)', '', regex=True).values

data = pd.DataFrame(list(zip(twitter_handles, tweets)), columns=['Tag', 'Text']).dropna(subset=['Tag', 'Text'])
``` 

| Twitter Handle | Tweet                                                                                                                |
|----------------|----------------------------------------------------------------------------------------------------------------------|
| 115712         | I understand. I would like to assist you. We would need to get you into a private secured link to further assist.    |
| sprintcare     | and how do you propose we do that                                                                                    |
| sprintcare     | I have sent several private messages and no one is responding as usual                                               |
| 115712         | Please send us a Private Message so that we can further assist you. Just click ‘Message’ at the top of your profile. |
| sprintcare     | I did.                                                                                                               |

After removing the NaN values we are left with `len(data.index)` = 2752066 rows.

From this information we can make up that company tweets are often sent to a `twitter handle` containing only numbers,
*probably to keep it anonymous*. With this information we can filter on customers or support staff should that be needed
by running the following code.

```python
data['Is_Employee'] = data['Tag'].str.isnumeric()

customers = data[~data['Is_Employee']]  # 1084313 Rows
support = data[data['Is_Employee']]  # 1667753 Rows
```

| Index | Tag        | Text                                             | Is_Employee |
|-------|------------|--------------------------------------------------|-------------|
| 1     | sprintcare | and how do you propose we do that                | False       |
| 2     | sprintcare | I have sent several private messages and no o... | False       |
| 4     | sprintcare | I did.                                           | False       |
| 6     | sprintcare | is the worst customer service                    | False       |
| 8     | sprintcare | You gonna magically change your connectivity ... | False       |

| Index | Tag    | Text                                             | Is_Employee |
|-------|--------|--------------------------------------------------|-------------|
| 0     | 115712 | I understand. I would like to assist you. We ... | True        |
| 3     | 115712 | Please send us a Private Message so that we c... | True        |
| 5     | 115712 | Can you please send us a private message, so ... | True        |
| 7     | 115713 | This is saddening to hear. Please shoot us a ... | True        |
| 9     | 115713 | We understand your concerns and we'd like for... | True        |

### Relevant Sentences

Let's figure out what may or may not be relevant to our case. Let's start by looking at the wordcount and decide what
lengths contain relevant information

```python
min_count = 3
max_count = 140

data[data['Text'].str.split(' ').str.len() <= min_count]  # 87178
data[data['Text'].str.split(' ').str.len() >= max_count]  # 26
```

|      | Tag            | Text                                                                                                                                              |
|-----:|:---------------|:--------------------------------------------------------------------------------------------------------------------------------------------------|
|    4 | sprintcare     | I did.                                                                                                                                            |
|   49 | VerizonSupport | Yep                                                                                                                                               |
|  130 | ATVIAssist     | Thanks                                                                                                                                            |
|  157 | AdobeCare      | sure thing                                                                                                                                        |
|  168 | AdobeCare      | ok                                                                                                                                                |
|  182 | AmazonHelp     | ありがとうございます。 今、電話で主人が対応していただいてます。                                                                                                                  |
|  183 | AmazonHelp     | 電話で対応してもらいましたが改良されませんでした。 保証期間も過ぎてるので買い直しになるんでしょうね。                                                                                               |
|  184 | 115770         | カスタマーサービスにてお問い合わせ済みとのことで、お手数をおかけいたしました。リプライいただきありがとうございました。ET                                                                                     |
|  185 | AmazonHelp     | こちらこそありがとうございました。                                                                                                                                 |
|  186 | 115770         | 恐れ入ります。至らない点も多々あるかとは存じますが、今後ともどうぞよろしくお願いします。ET                                                                                                    |
|  234 | 115792         | ご不便をおかけしております。アプリをご利用でしょうか。強制停止&gt;端末の再起動にて改善する場合がございますので、お試しください。改善しない場合は、状況を確認しご案内させていただきますのでこちらからカスタマーサービスまでご連絡ください。https://t.co/NtNAX2Qh2u ET |
|  268 | 115797         | H                                                                                                                                                 |
|  300 | McDonalds      | Treat!                                                                                                                                            |
|  303 | McDonalds      | Treat me!                                                                                                                                         |
|  316 | Delta          | DM sent                                                                                                                                           |
|  384 | 115821         | https://t.co/Gb0beuA3IN                                                                                                                           |
|  399 | AppleSupport   | https://t.co/NV0yucs0lB                                                                                                                           |
|  435 | AppleSupport   | iOS 11.0.3                                                                                                                                        |
|  447 | AppleSupport   | ? hello                                                                                                                                           |
|  489 | Delta          | Via DM?                                                                                                                                           |
|  497 | 115885         | 2/2 https://t.co/6iDGBJAc2m                                                                                                                       |
|  535 | Delta          | 0062395415777                                                                                                                                     |
|  555 | SpotifyCares   | ok thx                                                                                                                                            |
|  589 | comcastcares   | ✔                                                                                                                                                 |
|  637 | TMobileHelp    | https://t.co/tznFggbx3Y                                                                                                                           |
|  647 | VirginTrains   | thanks!                                                                                                                                           |
|  655 | VirginTrains   | Thanks                                                                                                                                            |
|  714 | AskeBay        | Thanks!!                                                                                                                                          |
|  720 | hulu_support   | Thanks                                                                                                                                            |
|  831 | 115980         | 😳 -Becky                                                                                                                                         |
|  833 | 115980         | 🙏 -Becky                                                                                                                                         |
|  840 | 115983         | Agreed. -Becky                                                                                                                                    |
|  902 | AskPlayStation | please help                                                                                                                                       |
|  927 | ChaseSupport   | Thanks guys!                                                                                                                                      |
|  995 | BofA_Help      | Thanks                                                                                                                                            |
| 1066 | GoDaddyHelp    | Thank you!                                                                                                                                        |
| 1070 | GoDaddyHelp    | https://t.co/qbjuBeYovF                                                                                                                           |
| 1092 | 116077         | Thanks!                                                                                                                                           |
| 1175 | AppleSupport   | Awesome, thanks                                                                                                                                   |
| 1197 | AppleSupport   | Worked 👌🏽                                                                                                                                       |
| 1214 | Uber_Support   | https://t.co/Fc42zHkmDA                                                                                                                           |
| 1226 | 116115         | 😂😂🙄                                                                                                                                            |
| 1275 | SpotifyCares   | 1.0.65.320.gac7a8e02                                                                                                                              |
| 1345 | 115911         | https://t.co/zc5zheYczx                                                                                                                           |
| 1361 | TMobileHelp    | Thanks!                                                                                                                                           |
| 1470 | ChipotleTweets | NOOOOOOOOOO https://t.co/MrbjgkVuzy                                                                                                               |
| 1480 | 116194         | Success! -Becky                                                                                                                                   |
| 1492 | ChipotleTweets | https://t.co/iGQf79bF32                                                                                                                           |
| 1500 | ChipotleTweets | BOORITO TIME!                                                                                                                                     |
| 1515 | VerizonSupport | Banking. https://t.co/8535p04F9S                                                                                                                  |
| 1535 | 116212         | We understand. ^JAY                                                                                                                               |
| 1545 | AskPlayStation | Thankx                                                                                                                                            |
| 1553 | AskPlayStation | Thanks !                                                                                                                                          |
| 1578 | ATVIAssist     | ^                                                                                                                                                 |
| 1583 | 115766         | Help                                                                                                                                              |
| 1655 | Morrisons      | Perth.                                                                                                                                            |
| 1660 | Morrisons      | 🎃🎃 https://t.co/biINVTmajm                                                                                                                      |
| 1778 | GloCare        | 08070635658                                                                                                                                       |
| 1819 | 116312         | わざわざご連絡をいただき、ありがとうございます。問題が改善されたようで、何よりでございます。万が一再度お困りのことがございましたら、ご遠慮なくお知らせください🙏 YM                                                              |
| 1820 | AmazonHelp     | 先日教えていただいたように、fireTVstickとルーターの両方を再起動してみたら、前回のようには途切れなくなりました！ありがとうございます😊今の所大丈夫ですが、あとは72時間TV当日に接続が切れてしまわないように祈るのみです...。                           |
|      |                | お礼と報告まで。 https://t.co/hS5VmxuIfX                                                                                                                  |
| 1822 | AmazonHelp     | ご丁寧にありがとうございます！トライしてみて改善されなければCSへご連絡します。返信いただけると思っていなかったので本当に嬉しいです！                                                                               |
| 1824 | AmazonHelp     | ありがとうございます！ テレビにstickを接続しているのですが、WiFi接続がすぐに切れてしまい、数分しか見ることができません。                                                                                 |
| 1825 | 116312         | アマゾンです。お困りの状況が特定できないのですが、エラーメッセージや画面の状況、操作方法など詳しい状況を教えていただけますか。ご利用端末はテレビですかPS4などのゲーム機でしょうか。ET                                                     |
| 1927 | AppleSupport   | 11.0.3                                                                                                                                            |
| 1938 | AppleSupport   | Yes                                                                                                                                               |
| 1942 | AppleSupport   | I did                                                                                                                                             |
| 1962 | CoxHelp        | You may                                                                                                                                           |
| 1992 | Uber_Support   | Just did                                                                                                                                          |
| 2000 | 115877         |                                                                                                                                                   |
| 2093 | 115888         | Why?? https://t.co/YCUDOLf2za                                                                                                                     |
| 2104 | Uber_Support   | Beef^^                                                                                                                                            |
| 2120 | SpotifyCares   | Thanks!                                                                                                                                           |
| 2125 | SpotifyCares   | AC/DC....                                                                                                                                         |
| 2131 | SpotifyCares   | https://t.co/T85iGba29f                                                                                                                           |
| 2175 | 116406         | Stopping                                                                                                                                          |
| 2185 | comcastcares   | Again                                                                                                                                             |
| 2197 | comcastcares   | Thank you!                                                                                                                                        |
| 2208 | AmericanAir    | Like, any?                                                                                                                                        |
| 2213 | AmericanAir    | #stillgoing                                                                                                                                       |
| 2215 | 116415         | jeez!                                                                                                                                             |
| 2234 | VirginTrains   | Night Joel                                                                                                                                        |
| 2262 | 116430         | https://t.co/eQqi9xisXh                                                                                                                           |
| 2295 | sprintcare     | Y’all lie                                                                                                                                         |
| 2298 | sprintcare     | complete ineptness!                                                                                                                               |
| 2328 | Delta          | Ok thanks.                                                                                                                                        |
| 2342 | Delta          | Just did                                                                                                                                          |
| 2347 | Delta          | Thank you.                                                                                                                                        |
| 2355 | 116465         | 😃 *TMB                                                                                                                                           |
| 2356 | Delta          | My pleasure.                                                                                                                                      |
| 2381 | DELTA          |                                                                                                                                                   |
| 2389 | Delta          | Yes, GEX8LD                                                                                                                                       |
| 2393 | Ask_Spectrum   | Thank you                                                                                                                                         |
| 2415 | 116484         | 😇 -Becky                                                                                                                                         |
| 2452 | ChipotleTweets | woohoo! 😍🎉                                                                                                                                      |
| 2490 | AskPlayStation | U positive?                                                                                                                                       |
| 2636 | McDonalds      | Treat                                                                                                                                             |
| 2638 | McDonalds      | Treat #trickortreat                                                                                                                               |
| 2640 | McDonalds      | Treat                                                                                                                                             |
| 2642 | McDonalds      | Treat                                                                                                                                             |
| 2644 | McDonalds      | Treat here                                                                                                                                        |

Quickly looking at a 100 rows shows that using less than 3 words results in irrelevant information for training
purposes.

|         | Tag    | Text                                                                                                                                                                                                                                                                                     |
|--------:|:-------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|  541853 | 264672 | Hi, Bret thank you so much for recognizing our employee. We\'ll be sure to forward your kind words on to Leadership.                                                                                                                             *TDH                                    |
|  602884 | 281343 | We love the chance to make a great first impression, Madison. Have a great day.                                                                                                                                                                                             *TDH         |
|  623602 | 286931 | Can you please DM your SkyMiles number so I can review your account.                                                                                                                                                                        *TDH                                         |
|  624835 | 287320 | That\'s a great picture. Thank you for sharing. We hope you have a fabulous trip.                                                                                                                                                                                            *TDH        |
| 1936495 | 618057 | What are you talking about bro?!?                        All you have to do is                                         Keep writing till you don’t have any             More characters                                               Left                                               |
| 2010963 | 636255 | We hear you. The TSA backup is affecting all of JFK. We hope that you\'ll be able to get on your way soon.                                                                                                                                                                  *TDH         |
| 2042873 | 643835 | Awesome picture. Thank you for sharing. We hope you have a fabulous trip.                                                                                                                                                                                                        *TDH    |
| 2162804 | 454864 | Hi, Jennifer please try and check in again to see if you will be able to get an electronic boarding pass now.                                                                                                                                                                *TDH        |
| 2318719 | 195734 | What an awesome view. Thank you for sharing.                                                                                                                                                                                                                               *TDH          |
| 2318723 | 709802 | Hi, Steven you should be able to locate your Regional Upgrade Certificates under your profile in "MY WALLET."                                                                                                                                                                    ... 1/2 |
| 2323725 | 710940 | Hi Dana I would suggest calling Expedia to help with the name correction.                                                                                                                                                                                                      *TDH      |
| 2374504 | 221368 | Hi Ralph my apology for the seat change. Unfortunately I\'m not showing the reason of the seat change.                                                                                                                                                  *TDH                             |
| 2376744 | 723238 | So sorry for the inconvenience to you. Sometimes we must reallocate our aircraft at the last minute.                                                                                                                                                                                *TDH |
| 2390909 | Delta  | Fuck you                                                                                                                                                                                                                                             your delays are inexcusable.        |
| 2444167 | 409282 | We\'re sorry Daniel. We know how frustrating delays are! We\'ll do our best to get you on your way soon.                                                                                                                                            *TDH                                 |
| 2527393 | 537308 | Have you tried telling the Flight Attendant about the discomfort of the temperature on the plane?                                                                                                                                                                          *TDH          |
| 2587155 | 771888 | Hi, Philip will you clarify how we may help you via Twitter?                                                                                                                                                                                                                *TDH         |
| 2596363 | 773793 | Please DM your confirmation or ticket number so we can review the itinerary.                                                                                                                                                                                                *TDH         |
| 2596365 | 630322 | We\'re disappointed to hear you feel that way. Thank you for your feedback, we\'ll pass it on to our Leadership Team.                                                                                                                                                            *TDH    |
| 2646133 | 124441 | I am getting Data usage warning.  I have the $45 plan Please advise 0 replies 0 retweets 0 likes                                                                                                                                                                                         |
| 2654242 | 787435 | Hi, Rob all Delta deals are located on our website at https://t.co/yQj0bzerMw under Delta fare sales.                                                                                                                                                                        *TDH        |
| 2708309 | 213396 | Thank you James and enjoy your flight.                                                                                                                                                                                                                                     *TDH          |

From this information we can see that even with 140 words the information stays relevant, so we will not remove big
tweets.

### Conclusion

So from this EDA we've learned the following;

* Messages contained various 'useless' characters, such as handles, tags, smileys, or URLs, these can easily be removed,
  while still keeping the main information of the tweet intact.
* Some messages carry very little information due to their word count, so we can remove items with less than 3 words
* Some messages are in different languages, since NLP is best when looking at english text the different languages can
  be removed.

We can use this information for the following steps;

* We have to clean the data before using it
* We can filter based on whether we want Customers, Support Staff, or Everyone
    * `Support Staff` & `Everyone` have a lot of similar topics that have little to do with support questions, so filtering on `Custommers` is the best way to get the best support question topics.
* We have to filter based on word count

## Back-End

In order for the Front-End to properly work it is important to have a fast and responsive Back-End. This Back-End is
used for both training and classification purposes. But since the Front-End focuses on classification, the training has
been done beforehand.

### Important Steps for Pre-Processing

After the quick round of EDA it is important to look at the data and see what can be removed and/or adapted in order to
have clean data to work with. From EDA, it became clear that the following had to be done in order to clean the data for
the NLP and ML pipeline to work efficiently.

* Look at all the different user tags, and decide which are companies and which are users. For this example it is
  assumed that the tweets with **@\<numerical\>** are tweets sent by a company to the user with **@\<numerical\>**.
    * This can be used to train either on customers, support staff, or both.
    * For this example I've trained on ...
* Remove all duplicate tweets.
* Remove all 'useless' characters using the `Preprocessor` class.
    * `clean_text` will remove all the useless characters using Regex
    * `clean_df` will filter employees and message size for training purposes
    * `preprocess` will filter for the important words (mainly `Proper Noun`, `Noun`, and `Verb`), and save the lemma
      for each

For this preprocessing step regex was used, since it turned out to be way quicker than cleaning with SpaCy, and resulted
in a good enough baseline to continue with.

#### Methods for Speeding up the Pre-Processing

* Filter Optimization
    * Using Regex to filter before trying to run Spacy to lemmatize/filter
* Minimize the use of apply (this is often slower than a for loop)

### Important Steps for Creating Model

For creating a model it is very important to understand the various different models that could be used for topic
classification.

First we have to decide on what type of Vectorizer to use, scikit-learn contains various vectorizers, such as:

* `CountVectorizer`, which converts a collection of text documents to a matrix of word counts.
* `TfidfVectorizer`, which converts a collection of text documents to a matrix of TF-IDF features.
* `HashingVectorizer`, which converts a collection of text documents to a matrix of word occurrences.

The `HashingVectorizer` performs best on very large datasets, since it does not rely on a vocabulary (or library) to
count, but this also means that you have no use for the resulting dictionary of tokens. `TF-IDF` penalises the words
that appear more frequent in the entire dataset, but this is not useful when deciding on what terms came across the
most.
Because of these reasons `CountVectorizer` was chosen for this case, since the dataset is not too big, and `TF-IDF` is
not useful because we should be dealing with raw counts; this also became clear when testing, the topics for `TF-IDF`
were less coherent than the topics generated by `CountVector`.

After this we have to decide on what type of model to use for this case, various of these models are described in:
> Egger, R., & Yu, J. (2022). A Topic Modeling Comparison Between LDA, NMF, Top2Vec, and BERTopic to Demystify Twitter
> Posts. In Frontiers in Sociology (Vol. 7). Frontiers Media SA. https://doi.org/10.3389/fsoc.2022.886498

According to this paper it is best to use `NMF`, since both `BERTopic` and `Top2Vec` require prior knowledge of the
dataset ((semi-)supervised learning) and `LDA` performed worse than `NMF` on short tweets and requires a lot of
hyperparameter tuning in order to work optimally.

After creating the model it is important to also save it, so it can be re-used later on for determining the topics of
new conversations, in order to do this the `joblib` package was used, since it is advised to used by the `scikit-learn`
documentation, the other widely used package, `pickle`, often is slower for very large arrays.

#### Methods for Speeding up the Model Creation

* Hyperparameter Tuning

### Important Steps for New Conversation Classification

For predicting topics of new conversations it is important to work with the previously created models. In order to do
this the following steps were taken to predict the topics:

* Load the `joblib` files in order to create the `CountVectorizer` and `NMF` models.
* Initialize the topic keywords, by finding the most important feature names using the `Vectorizer` and `NMF`.
* To predict the eventual topic the following steps were needed:
    * Pre-Process the input
    * Transform the input using the `CountVectorizer` and `NMF`, this gives the eventual weights of each topic in
      relation
      to the conversation.
    * Find the topic with the highest weight, this will be the most likely topic of the conversation.

#### Methods for Speeding up the Classification

* Use as little loops as possible
* Use quick calculations

## Front-End

Before I started working on the implementation of the Fron-End I planned the entire webapp on paper and Figma.

I created a list of requirements on paper:

* The webapp should have the admins login in order to use the service.
* After login the Admin should be shown various information on the models and topics.
* It should be clear without explanation how to (bulk) import new conversations.
* The admin should be able to change the summarised topic names (this might be useful for readability but requires some
  human work/research).
* The admin should be able to quickly see all different types of information in a clean and organized manner.

Using this (short) list of requirements a list of pages was made up and a tree diagram was created on paper:

* Login Page
* Dashboard home screen
    * Show overview of information in a graph
    * Show detailed information in a table
    * Allow admins to upload new conversations
* Settings Screen
    * Should allow to edit topics
    * ~~Create new accounts~~ *This is scrapped because it goes outside the scope of the case. As well as requiring more
      time than allotted to this case.*
    * ~~Upload new dataset to retrain the model~~ *This is scrapped because it goes outside the scope of the case. As well as requiring more time than allotted to this case.*

![design_paper.png](images/design_paper.jpg)

### Login Page

As mentioned previously the admin should be able to securely access the information they require in order to provide the
right type of support. This is why a login page was designed, which should allow everything to be handled securely.

#### Design

For the design it was kept in mind that the eventual page should contain only the necessary information, such as a login
form. A stock image was pulled from the internet and added to the design in order to give it a more modern look.

![login_figma.png](images/login_figma.png)

#### Implementation

The implementation for this page is quite simple, since I do not take a highly secure database for login as an important
aspect for this case. This is why this implementation uses a simple login implementation, which will have to be improved
when used in real life scenarios. This is also the reason why the `Forgot Password?` button is not working.

### Admin Dashboard

On the admin dashboard the admin should be able to have a quick overview of various pieces of information relevant to
the topics of the support questions. For this example I've decided on using the following variables to fill the
dashboard:

* Quick overview area - *These are mostly interesting facts about the data on the dashboard (Note, this is just an
  example)*
    * Total Topics
    * Total Conversations
* Deep Information area - *This is a table with all conversations added by the admin with their topics*
* (Bulk) adding Conversations - *This should be a button that opens a form to upload more data to be processed*

#### Design

This design also was kept to a minimal, it contains only the relevant information and nothing else, because of this it
is very easy for the admins to understand, the graph can be used to see what topics are relevant, and the admin is able
to either manually copy and paste conversations, or upload a csv to add conversations in bulk.

![img.png](images/dashboard_figma.png)

#### Implementation

The implementation for this is relatively simple, the graph shows an image of `matplotlib` plots. And the new
conversation adder links directly to the backend. The text based adding is directly added into the backend, while the
bulk csv uploading requires the csv file to be parsed before it can be used.

### Settings

For an admin it is important to have access to some more information on what is shown. Using this setting screen the
admin should be able to add new user accounts, change the topics, and retrain the data.

#### Design

The design is an example of the `settings` screen. It will allow the admin to change the summaries for each topic, so
they are better to understand.

![img.png](images/Settings_figma.png)

### General Implementation Strategy

Since Django is a new framework for me, I've implemented the design using the following steps:

* Implement the pages using basic html (without CSS).
    * Implement simple authentication
    * Implement showing of Graphs using `GraphJS`
    * Implement showing of Table from `sqlite`
    * Implement uploading new data to `sqlite`
    * Implement editing data from `sqlite`
* Design the pages by creating CSS based on the `Figma` designs mentioned above.
    * _Note, these designs are a little more simple in the eventual web application due to time constraints._

Each page was first written in plain HTML, after that was all working perfectly, the CSS code was written using both
Bootstrap and Custom CSS to create the look and feel of the application.

### Database Design

In order to store all the information that is needed to get the web application up and running it is important to design
what the database(s) will look like. The following information has to be stored somewhere in order for it to be re-used
on the web application:

* Username / Password
* Conversations / Topics
* Topics / Summary - *Note, this is mainly useful for the readability of the application*

As mentioned previously the databases will be stored using `sqlite`, because it is a relatively lightweight db that is
supported by `django` and allows for quick and easy access/manipulation.