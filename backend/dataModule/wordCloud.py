import pandas as pd
import operator
import json
from dataModule import nlp
import nltk
import os


def getDFbyDate(start_date, end_date, symbol):
    # get news within specified time span
    df = pd.read_csv('./dataset/news sentiment/' +
                     symbol + '_news_sentiment.csv')

    # drop datetime whose value is NaN
    df = df.dropna(subset=['datetime'])

    # clean datetime
    df['datetime'] = df['datetime'].apply(lambda x: x[:10])

    # preporcess title: remove stop words, and lemmentaize
    df['title'] = df['title'].apply(nlp.preprocess)

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
                if t in frequency:
                    frequency[t] += 1
                else:
                    frequency[t] = 1
        elif polarity < 0:
            for t in title:
                if t in frequency:
                    frequency[t] -= 1
                else:
                    frequency[t] = -1

    # Sort the frequency dict by freq in descending order
    sorted_freq = dict(
        sorted(frequency.items(), key=operator.itemgetter(1), reverse=True))

    # convert to list of dictionaries
    data = [{'name': k, 'value': v} for k, v in sorted_freq.items()]
    # write to json
    with open('./dataset/wordcloud.json', 'w+') as f:
        json.dump(data, f, indent=2)


# testing
# start_date = "2020-01-01"
# end_date = "2022-01-01"
# symbol = 'AAPL'
# getWordCloud(start_date, end_date, symbol)
