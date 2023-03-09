import yfinance as yf
import datetime
import pandas as pd

start = datetime.datetime(2017, 1, 1)
end = datetime.datetime(2023, 3, 1)

df = pd.read_csv('../dataset/Stocks Symbols.csv')

# select mid, large, and mega market cap
df = df.loc[df['Market_Cap'] > 2000000000.00]

for idx, stockSymbol in enumerate(df["Symbol"]):
    stock = yf.download(stockSymbol, start=start, end=end, progress=False)
    stock.to_csv("../dataset/Historical Price/" +
                 stockSymbol + ".csv", index=True)

    print(str(idx) + ": Finished getting " + stockSymbol)
