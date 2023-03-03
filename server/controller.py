import pandas as pd
from resources.textProcessing import preprocess
import json
from collections import defaultdict
import sys


def process(titlesPath, journalsPath):
    covid19Data = pd.read_csv("../server/data/COVID-19.csv")

    # 處理 abstract
    abstracts = preprocess(covid19Data['abstract'])
    abstracts = dict(sorted(abstracts.items(), key=lambda item: item[1], reverse=True))
    abstractsSliced = {a: abstracts[a] for a in list(abstracts)[:300]}  # 取出次數前三百名

    # 處理 publish time
    yearMonth = defaultdict(int)
    for time in covid19Data['publish_time']:
        if str(time).split('-')[0] != "nan":
            timeSplit = str(time).split('-')
            if len(timeSplit) > 1 and 2019 <= int(timeSplit[0]) < 2024:
                if (int(timeSplit[0]) == 2019 and int(timeSplit[1]) >= 11) or int(timeSplit[0]) >= 2020:
                    yearMonth[str(timeSplit[0]) + "-" + str(timeSplit[1])] += 1

    # Save processing results into JSON files
    with open(titlesPath, "w") as outputFile:
        json.dump(abstractsSliced, outputFile)
    with open(journalsPath, "w") as outputFile:
        json.dump(yearMonth, outputFile)

