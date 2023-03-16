# For data manipulation
import pandas as pd
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re
import numpy as np

# import hierarchical clustering libraries
import scipy.cluster.hierarchy as sch
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt


def fundamental_metric(soup, metric):
    float_pattern = r'^\d+\.\d+$'
    float_pattern_with_percent = r'^-?\d+\.\d+%$'
    million_pattern = r'^\d+\.\d+M'
    thousand_pattern = r'^\d+\.\d+K'
    value = soup.find(text=metric).find_next(class_='snapshot-td2').text

    # classify value to categories
    if re.match(float_pattern, value):
        return float(value)
    elif re.match(float_pattern_with_percent, value):
        # value = float(value[-1])/100  # if want to discard %, use this line
        return float(value[:-1])
    elif re.match(million_pattern, value):
        return float(value[:-1]) * (10 ** 6)
    elif re.match(thousand_pattern, value):
        return float(value[:-1]) * (10 ** 3)
    elif '/' in value:
        short_float, short_ratio = value.split('/')
        # if want to discard %, use this line
        # short_float = float(short_float[-1]) / 100
        return float(short_float[:-2]), float(short_ratio)


def get_fundamental_data(df):
    for idx, symbol in enumerate(df['Symbol']):
        try:
            url = ("http://finviz.com/quote.ashx?t=" + symbol.lower())
            req = Request(url=url, headers={
                          'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'})
            response = urlopen(req)
            soup = BeautifulSoup(response, "html.parser")

            metrics = df.columns.tolist()
            metrics.remove('Symbol')
            for m in metrics:
                # special case: containing two variables in one
                if m == "Short Float / Ratio":
                    s_float, s_ratio = fundamental_metric(soup, m)
                    df.iloc[idx]['Short Float'] = s_float
                    df.iloc[idx]['Short Ratio %'] = s_ratio

                val = fundamental_metric(soup, m)
                df.iloc[idx][m] = val if val != None else np.nan
        except Exception as e:
            print(symbol, 'not found')
    return df


def get_all_stocks_fundamental_data(metrics):
    # stocks = pd.read_csv('./server/data/Stocks Symbols.csv')
    # stocks = stocks.loc[stocks['Market_Cap'] > 2000000000.00]
    # stock_list = stocks["Symbol"].to_list()

    # testing only two stocks
    stock_list = ['AAPL', 'MSFT', 'GOOG',
                  'AMZN', 'PCAR', 'TSLA',
                  'NVDA', 'META', 'ASML',
                  'AVGO', 'PEP', 'COST',
                  'AZN', 'CSCO']

    df = pd.DataFrame(columns=metrics)
    df['Symbol'] = stock_list
    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]

    df = get_fundamental_data(df)
    df.to_csv('./server/financial_indicators.csv', index=False)
    print(df)


def clean_financial_indicators_df(df):

    # 1. Seperate column "Short Float / Ratio" to two columns
    # create two new columns with default value NaN
    df["Short Float"] = np.nan
    df["Short Ratio"] = np.nan

    # loop through each row and extract the values
    for i in range(len(df)):
        # use eval() to convert the string tuple into a tuple of floats
        value = eval(df.iloc[i]["Short Float / Ratio"])
        if pd.notna(value):
            short_float, short_ratio = value
            df.at[i, "Short Float"] = short_float
            df.at[i, "Short Ratio"] = short_ratio
    # drop the original column
    df.drop(columns=["Short Float / Ratio"], inplace=True)

    # 2. Perform operations on missing value, NaN


def perform_heirarchical_cluster():
    df = pd.read_csv('./server/financial_indicators.csv')

    clean_financial_indicators_df(df)

    print(df)
    return None


metrics = [
    'P/B',
    'P/E',
    'Forward P/E',
    'PEG',
    'Debt/Eq',
    'EPS (ttm)',
    'Dividend %',  # is %
    'ROE',  # is %
    'ROI',  # is %
    'EPS Q/Q',  # is %
    'Insider Own',  # is %
    'Beta',
    'Short Float / Ratio',  # is % / not %
    'Profit Margin',  # is %
    'Avg Volume'
]

# run this to fetch metrics for all stocks
# get_all_stocks_fundamental_data(metrics)
perform_heirarchical_cluster()
