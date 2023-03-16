import pandas as pd
import json

<<<<<<< Updated upstream
from dataModule import calculateStockChangebyDate
=======
from dataModule.calculateStockChangebyDate import getStocksChange
>>>>>>> Stashed changes


def getDFbyDate(start_date, end_date, symbol):
    # get news within specified time span
    df = pd.read_csv('./dataset/news sentiment/' +
                     symbol + '_news_sentiment.csv')

    # drop datetime whose value is NaN
    df = df.dropna(subset=['datetime'])

    # clean datetime
    df['datetime'] = df['datetime'].apply(lambda x: x[:10])

    # filter rows based on datetime
    filtered_df = df[(df['datetime'] >= start_date)
                     & (df['datetime'] <= end_date)]

    filtered_df = filtered_df.loc[:, ["title", "datetime", "link", "Compound"]]

    return filtered_df


def writetoJSON(results):
    json_list = [[{"title": d["title"], "datetime": d["datetime"], "desc": d["link"]}
                  for d in results[k]] for k in results.keys()]

    # write to json
    with open('./dataset/NewsSentimentList.json', 'w') as f:
        json.dump(json_list, f, indent=4)


def get_news_sentiment(start_date, end_date, symbol):
    df = getDFbyDate(start_date, end_date, symbol)

    change = calculateStockChangebyDate.getStocksChange(symbol, start_date, end_date)

    # split df to Positive, Negative, and Neutral
    pos_df = df[df['Compound'] > 0]
    neg_df = df[df['Compound'] < 0]
    neu_df = df[df['Compound'] == 0]

    # sort positive df by descending
    pos_df = pos_df.sort_values('Compound', ascending=False)
    # sort negative df by ascending
    neg_df = neg_df.sort_values('Compound', ascending=True)

    # convert df to dict
    pos = pos_df.to_dict(orient='records')
    neg = neg_df.to_dict(orient='records')
    neu = neu_df.to_dict(orient='records')

    results = {}
    if change > 0:
        results['Positive'] = pos
        results['Neutral'] = neu
        results['Negative'] = neg
        writetoJSON(results)
    else:
        results['Negative'] = neg
        results['Neutral'] = neu
        results['Positive'] = pos
        writetoJSON(results)


# testing
start_date = "2020-01-01"
end_date = "2022-01-01"
symbol = 'AAPL'
get_news_sentiment(start_date, end_date, symbol)
