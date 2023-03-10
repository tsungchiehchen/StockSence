import pandas as pd
import re


def get_dataframe(symbol):
    # get the news from using stock symbol
    symbol_news_df = pd.read_csv('./dataset/news/' + symbol + '.csv')

    # get the news from using company name
    comp_name_news_df = pd.read_csv(
        './dataset/news-company-name/' + symbol + '.csv')

    # combine news scrape with stock symbols and company's name
    combined_df = pd.concat([symbol_news_df, comp_name_news_df], axis=0)
    # reset the index of the combined dataframe
    combined_df = combined_df.reset_index(drop=True)

    # sort news datetime with ascending order
    combined_df = combined_df.sort_values('datetime', ascending=True)
    combined_df = combined_df.reset_index(drop=True)

    return combined_df


def drop_NaN_date(df):

    return df


# testing
symbol = 'AAPL'
df = get_dataframe(symbol)

# clean datetime (~1070 total)
df = drop_NaN_date(df)

datetime_missing = df['datetime'].isnull().sum()
print(datetime_missing)

# clean title (~ 3004 total)
incomplete_title_missing = (df["title"].str.contains(re.escape("..."))).sum()
print(incomplete_title_missing)
print()

# news classified as Neutral (~7512 total AAPL)
df = pd.read_csv('./dataset/news sentiment/AAPL_news_sentiment.csv')
print(len(df[df["Compound"] != 0]))
print(len(df[df["Compound"] == 0]))
print()

# news classified as Neutral (~7512 total TSLA)
df = pd.read_csv('./dataset/news sentiment/TSLA_news_sentiment.csv')
print(len(df))
print(len(df[df["Compound"] != 0]))
print(len(df[df["Compound"] == 0]))
print()

# news classified as Neutral (~3x total AACG)
df = pd.read_csv('./dataset/news sentiment/AACG_news_sentiment.csv')
print(len(df[df["Compound"] != 0]))
print(len(df[df["Compound"] == 0]))
print()
