import pandas as pd
import json
from datetime import datetime, timedelta
import zipfile

# from dataModule.calculateStockChangebyDate import getStocksChange


def getDFbyDate(start_date, end_date, symbol):
    # # Uncomment below to use unzip
    # # specify the path to the zip file
    # zip_file_path = './dataset/test/news sentiment.zip'

    # # open the zip file and extract its contents
    # with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    #     zip_ref.extractall('./dataset/test/news sentiment')

    # # get news within specified time span
    # df = pd.read_csv('./dataset/test/news sentiment/' +
    #                  symbol + '_news_sentiment.csv')

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
    json_list = json.dumps(results)

    # write the json array to a file
    with open('./dataset/NewsSentimentList.json', 'w') as f:
        f.write(json_list)


def get_news_sentiment(start_date, end_date, symbol):
    df = getDFbyDate(start_date, end_date, symbol)
    df = df.sort_values('datetime', ascending=False)
    # compound_score_threshold = 0.5 if len(df) > 150 else 0.3
    # change = getStocksChange(symbol, start_date, end_date)

    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    results = []
    for i in range((end_date - start_date).days + 1):
        current_date = start_date + timedelta(days=i)
        current_date = current_date.strftime('%Y-%m-%d')

        mask = (df['datetime'] == current_date)
        selected_rows = df.loc[mask]

        # sort if the news item in that day is more than 10
        if len(selected_rows) > 10:
            selected_rows.sort_values('Compound', ascending=True, inplace=True)

            # get positive
            for i in range(len(selected_rows)-1, len(selected_rows) - 6, -1):
                result = {}
                result['title'] = selected_rows.iloc[i]['title']
                result['datetime'] = selected_rows.iloc[i]['datetime']
                result['link'] = selected_rows.iloc[i]['link']
                result['Sentiment'] = "Positive" if selected_rows.iloc[i]['Compound'] > 0 else "Neutral"
                results.append(result)

            # get negative
            for i in range(0, 5, 1):
                result = {}
                result['title'] = selected_rows.iloc[i]['title']
                result['datetime'] = selected_rows.iloc[i]['datetime']
                result['link'] = selected_rows.iloc[i]['link']
                result['Sentiment'] = "Negative" if selected_rows.iloc[i]['Compound'] < 0 else "Neutral"
                results.append(result)
        else:
            for i in range(len(selected_rows)):
                result = {}
                result['title'] = selected_rows.iloc[i]['title']
                result['datetime'] = selected_rows.iloc[i]['datetime']
                result['link'] = selected_rows.iloc[i]['link']
                if selected_rows.iloc[i]['Compound'] < 0:
                    result['Sentiment'] = "Negative"
                elif selected_rows.iloc[i]['Compound'] > 0:
                    result['Sentiment'] = "Positive"
                else:
                    result['Sentiment'] = "Neutral"
                results.append(result)
    writetoJSON(results)


# testing
start_date = "2019-08-01"
# end_date = "2020-01-01"
end_date = "2019-08-02"
symbol = 'AAPL'
get_news_sentiment(start_date, end_date, symbol)
