import pandas as pd


def getWordCloud(start_date, end_date, symbol):
    # get news within specified time span
    df = pd.read_csv('../dataset/news sentiment/' +
                     symbol + '_news_sentiment.csv')

    # convert datetime column to datetime type
    df['datetime'] = pd.to_datetime(df['datetime'])

    # filter rows based on datetime
    filtered_df = df[(df['datetime'] >= start_date)
                     & (df['datetime'] <= end_date)]

    # display the filtered dataframe
    print(filtered_df)

    # write to json


# testing
start_date = "2020-01-01"
end_date = "2022-01-01"
symbol = 'AAPL'
getWordCloud(start_date, end_date, symbol)
