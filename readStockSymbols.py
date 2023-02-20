import pandas as pd

df = pd.read_csv('./dataset/Stocks Symbols.csv')

# Drop "Last Sale", "Net Change", "%Change", "IPO Year"
df = df.drop(["Last Sale", "Net Change", "% Change",
             "IPO Year"], axis='columns')

# sort df by "Market Cap"
df = df.sort_values("Market_Cap", ascending=False)

# print(df.head(10))
# print(len(df))

# split whole NASDAQ into mega, large, and mid cap dataframe

# mega
mega_cap_df = df.query('Market_Cap > 200*(10**9)')
mega_cap_df.to_csv("./dataset/MegaCap Stock Symbols.csv", index=False)
print(mega_cap_df.head())
print(len(mega_cap_df))


# large
large_cap_df = df.query('10 * (10**9) < Market_Cap < 200*(10**9)')
large_cap_df.to_csv("./dataset/LargeCap Stock Symbols.csv", index=False)
print(large_cap_df.head())
print(len(large_cap_df))


# mid
mid_cap_df = df.query('2 * (10**9) < Market_Cap < 200*(10**9)')
mid_cap_df.to_csv("./dataset/MidCap Stock Symbols.csv", index=False)
print(mid_cap_df.head())
print(len(mid_cap_df))
