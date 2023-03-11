import pandas as pd
import time
import json
from json import JSONEncoder
import numpy as np

# get stock symbols list
df = pd.read_csv('./dataset/Stocks Symbols.csv')
df = df.loc[df['Market_Cap'] > 2000000000.00]


for symbol in df['Symbol'].to_list():
    hist_price_df = pd.read_csv(
        './dataset/Historical Price/' + symbol + '.csv')

    results = []
    for i in range(len(hist_price_df)):
        milliseconds = time.mktime(time.strptime(
            hist_price_df.loc[i, 'Date'], "%Y-%m-%d")) * 1000
        date = milliseconds
        open_price = float(hist_price_df.loc[i, 'Open'])
        high = float(hist_price_df.loc[i, 'High'])
        low = float(hist_price_df.loc[i, 'Low'])
        close = float(hist_price_df.loc[i, 'Close'])
        volume = float(hist_price_df.loc[i, 'Volume'])
        results.append([date, open_price, high, low, close, volume])

    # Dump the results as a JSON file
    with open("./dataset/price display/" + symbol + ".json", "w") as f:
        json.dump(results, f)
