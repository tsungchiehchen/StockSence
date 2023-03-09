import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import re


def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)


def preprocess(raw_text: str) -> str:
    stop_words_file = './dataset/nlp/SmartStoplist.txt'
    # load stop_words dictionary
    stop_words = []
    with open(stop_words_file, "r") as f:
        for line in f:
            stop_words.extend(line.split())

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
        if word in lm_dict:
            new_lexicon[word]['pos'] *= 2
            new_lexicon[word]['neg'] *= 2
    for word, scores in lm_dict.items():
        if word not in new_lexicon:
            new_lexicon[word] = {'pos': 0.0, 'neg': 0.0, 'neu': 1.0}
            if scores['Positive'] > scores['Negative']:
                new_lexicon[word]['pos'] = scores['Positive'] + 1
            elif scores['Positive'] < scores['Negative']:
                new_lexicon[word]['neg'] = scores['Negative'] + 1
            else:
                new_lexicon[word]['pos'] = 1.0
                new_lexicon[word]['neg'] = 1.0
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


def get_sentiment_as_dataframe(symbol):
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

    # get sentiment score on each title
    scores = get_sentiment_score(combined_df['title'])
    combined_df['Score'] = scores

    return combined_df


# testing
symbol = 'AAPL'
df = get_sentiment_as_dataframe(symbol)
print(df)
