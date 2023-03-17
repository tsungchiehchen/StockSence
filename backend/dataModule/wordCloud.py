import pandas as pd
import operator
import json
import re
from nltk.corpus import stopwords
import itertools


def preprocess(raw_text: str):
    stop_words = set(stopwords.words('english'))

    # Step 1: remove non-letter characters and convert the string to lower case
    letters_only_text: str = re.sub("[^a-zA-Z]", " ", raw_text)
    letters_only_text: str = letters_only_text.lower()

    # Step 2: tokenization -- split into words -> convert string into list ( 'hello world' -> ['hello', 'world'])
    words: list[str] = letters_only_text.split()

    # Step 3: remove stopwords
    cleaned_words = []
    for word in words:
        if word not in stop_words:
            cleaned_words.append(word)

    return " ".join(cleaned_words)


def getDFbyDate(start_date, end_date, symbol):
    # get news within specified time span
    df = pd.read_csv('./dataset/news sentiment/' +
                     symbol + '_news_sentiment.csv')

    # drop datetime whose value is NaN
    df = df.dropna(subset=['datetime'])

    # clean datetime
    df['datetime'] = df['datetime'].apply(lambda x: x[:10])

    # preporcess title: remove stop words, and lemmentaize
    df['title'] = df['title'].apply(preprocess)

    # filter rows based on datetime
    filtered_df = df[(df['datetime'] >= start_date)
                     & (df['datetime'] <= end_date)]

    filtered_df = filtered_df.loc[:, ["title", "datetime", "link", "Compound"]]

    return filtered_df


def getWordCloud(start_date, end_date, symbol):
    df = getDFbyDate(start_date, end_date, symbol)

    # Count the word frequency
    frequency = {}
    for i in range(len(df)):
        title = df.iloc[i]['title'].split()
        polarity = df.iloc[i]['Compound']

        if polarity > 0:
            for t in title:
                if len(t) > 2:
                    if t in frequency:
                        frequency[t] += 1
                    else:
                        frequency[t] = 1
        elif polarity < 0:
            for t in title:
                if len(t) > 2:
                    if t in frequency:
                        frequency[t] -= 1
                    else:
                        frequency[t] = -1

    # assign '+' or '-' based on the value
    modified_freq = {}
    for key, value in frequency.items():
        if value < 0:
            key += '-'
            modified_freq[key] = value * -1
        else:
            key += '+'
            modified_freq[key] = value

    # Sort the frequency dict by freq in descending order
    sorted_freq = dict(
        sorted(modified_freq.items(), key=operator.itemgetter(1), reverse=True))
    # get at most 150 items
    if len(sorted_freq) > 150:
        sorted_freq = dict(itertools.islice(sorted_freq.items(), 150))

    # convert to list of dictionaries
    data = [{'name': k, 'value': v} for k, v in sorted_freq.items()]
    # write to json
    with open('./dataset/wordcloud.json', 'w') as f:
        json.dump(data, f, indent=2)


# testing
# start_date = "2020-01-01"
# end_date = "2022-01-01"
# symbol = 'AAPL'
# getWordCloud(start_date, end_date, symbol)
