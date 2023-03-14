import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import re
import time
import itertools
import csv


def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)


def preprocess(raw_text: str) -> str:
    stop_words = set(stopwords.words('english'))

    # Step 1: remove non-letter characters and convert the string to lower case
    letters_only_text: str = re.sub("[^a-zA-Z]", " ", raw_text)
    letters_only_text: str = letters_only_text.lower()

    # Step 2: tokenization -- split into words -> convert string into list ( 'hello world' -> ['hello', 'world'])
    words: list[str] = letters_only_text.split()

    # Step 3: remove stopwords
    cleaned_words = []
    for word in words:
        if word not in stop_words:
            cleaned_words.append(word)

    # Step 4: lemmatise words
    lemmas = []
    lemmatizer = WordNetLemmatizer()
    for word in cleaned_words:
        lemma = lemmatizer.lemmatize(word, get_wordnet_pos(word))
        lemmas.append(lemma)

    # Step 5: converting list back to string and return
    return " ".join(lemmas)


def merge_lexicons(vader, lm_dict):
    new_lexicon = {}
    for word, scores in vader.items():
        new_lexicon[word] = scores
        if word.upper() in lm_dict:
            new_lexicon[word] *= 2
    for word, scores in lm_dict.items():
        word = word.lower() if isinstance(word, str) else word
        if word not in new_lexicon:
            if scores['Positive'] > 0:
                new_lexicon[word] = 4
            elif scores['Negative'] > 0:
                new_lexicon[word] = -4
            else:
                new_lexicon[word] = 0

    return new_lexicon


def get_sentiment_score(texts):
    scores = []

    vader = SentimentIntensityAnalyzer().lexicon
    lm_dict = pd.read_csv('./dataset/nlp/Loughran-McDonald_MasterDictionary_1993-2021.csv').set_index(
        'Word').to_dict('index')

    new_lexicon = merge_lexicons(vader, lm_dict)

    analyzer = SentimentIntensityAnalyzer()
    analyzer.lexicon = new_lexicon

    for text in texts:
        processed_text = preprocess(text)
        score = analyzer.polarity_scores(processed_text)
        scores.append(score)

    return scores


def drop_row_with_duplicate(df):
    df.drop_duplicates(keep='first', inplace=True)
    return df


def get_sentiment_as_dataframe(symbol):
    # get the news from using stock symbol
    try:
        symbol_news_df = pd.read_csv('./dataset/news/' + symbol + '.csv')
    except:
        symbol_news_df = pd.DataFrame()

    # get the news from using company name
    try:
        comp_name_news_df = pd.read_csv(
            './dataset/news-company-name/' + symbol + '.csv')
    except:
        comp_name_news_df = pd.DataFrame()

    # combine news scrape with stock symbols and company's name
    combined_df = pd.concat([symbol_news_df, comp_name_news_df], axis=0)
    # reset the index of the combined dataframe
    combined_df = combined_df.reset_index(drop=True)

    # sort news datetime with ascending order
    combined_df = combined_df.sort_values('datetime', ascending=True)
    combined_df = combined_df.reset_index(drop=True)

    # drop duplicates
    combined_df.drop_duplicates(keep='first', inplace=True)
    combined_df.to_csv(
        './dataset/combine news/combined_news_' + symbol + '.csv', index=False)

    df = pd.read_csv('./dataset/combine news/combined_news_' + symbol + '.csv')

    # get sentiment score on each title
    scores = get_sentiment_score(df['title'])

    for i in range(len(scores)):
        df.loc[i, 'Negative'] = scores[i]['neg']
        df.loc[i, 'Neutral'] = scores[i]['neu']
        df.loc[i, 'Positive'] = scores[i]['pos']
        df.loc[i, 'Compound'] = scores[i]['compound']

    df.to_csv('./dataset/news sentiment/' + symbol +
              '_news_sentiment.csv', index=False)


# df = pd.read_csv('./dataset/Stocks Symbols.csv')
# df = df.loc[df['Market_Cap'] > 2000000000.00]
# symbols = df['Symbol'].tolist()

# for symbol in symbols:
#     start = time.time()
#     get_sentiment_as_dataframe(symbol)
#     end = time.time()
#     print("Finished " + symbol + " in ", end-start, " Seconds")
