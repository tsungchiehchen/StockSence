import pandas as pd

df = pd.read_csv('./dataset/Stocks Symbols.csv')

# Drop "Last Sale", "Net Change", "%Change", "IPO Year"
df = df.drop(["Last Sale", "Net Change", "% Change",
             "IPO Year"], axis='columns')

print(df.head(10))
print(len(df))
