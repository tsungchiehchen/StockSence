from FetchNews import GoogleNews
import time
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from random import randint
import csv
import pandas as pd

# read csv file
df = pd.read_csv('./dataset/MegaCap Stock Symbols.csv')
stockSymbols = list(df["Symbol"])

for stockSymbol in stockSymbols:
    f = open('./dataset/news/' + str(stockSymbol) + '.csv', 'w')
    writer = csv.writer(f)
    header = ['title', 'datetime', 'link']
    writer.writerow(header)

    def datespan(startDate, endDate, delta=timedelta(days=1)):
        currentDate = startDate
        while currentDate < endDate:
            yield currentDate
            currentDate += delta

    for month in datespan(date(2020, 1, 1), date(2023, 3, 1), delta=relativedelta(months=1)):
        endMonth = month + relativedelta(day=31)
        if int(month.month) % 2 == 0:
            https = True
        else:
            https = False
        googlenews = GoogleNews(lang='en', region='US', start=str(month.strftime(
            "%m/%d/%Y")), end=str(endMonth.strftime("%m/%d/%Y")), https=https)
        googlenews.get_news(str(stockSymbol))
        results = googlenews.results()
        for result in results:
            dateResult = []
            dateResult.append(str(result['title']))
            dateResult.append(result['datetime'])
            dateResult.append("https://" + str(result['link']))
            writer.writerow(dateResult)
        # time.sleep(randint(50, 65))
