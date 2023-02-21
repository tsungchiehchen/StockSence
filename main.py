from FetchNews import GoogleNews
import time
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from random import randint
import csv
import pandas as pd
import urllib
import json
from multiprocessing import Pool, Manager
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map
import os


def getCompanyName(symbol):
    while True:
        try:
            response = urllib.request.urlopen(f'https://query2.finance.yahoo.com/v1/finance/search?q={symbol}')
            content = response.read()
            data = json.loads(content.decode('utf8'))['quotes'][0]['shortname']
            companyNames[str(symbol)] = str(data)
        except Exception:
            #tqdm.write("Error on %s retrying" % symbol)
            continue
        break

def datespan(startDate, endDate, delta=timedelta(days=1)):
        currentDate = startDate
        while currentDate < endDate:
            yield currentDate
            currentDate += delta


if __name__ == '__main__':
    # read csv file
    stockSymbol = pd.read_csv('./dataset/MidCap Stock Symbols.csv')
    stockSymbols = list(stockSymbol["Symbol"])

    # Get all company names
    print("Fetch all company names")
    manager = Manager()
    companyNames = manager.dict()
    process_map(getCompanyName, stockSymbols, max_workers=os.cpu_count()-1)
    #print(companyNames)

    # Get news from Google News
    print("\nStart getting news")
    for stockSymbol in stockSymbols:
        companyName = companyNames[stockSymbol]
        f = open('./dataset/news-company-name/' + str(stockSymbol) + '.csv', 'w')
        writer = csv.writer(f)
        header = ['title', 'datetime', 'link']
        writer.writerow(header)

        for month in datespan(date(2020, 1, 1), date(2023, 3, 1), delta=relativedelta(months=1)):
            endMonth = month + relativedelta(day=31)
            if int(month.month) % 2 == 0:
                https = True
            else:
                https = False
            googlenews = GoogleNews(lang='en', region='US', start=str(month.strftime(
                "%m/%d/%Y")), end=str(endMonth.strftime("%m/%d/%Y")), https=https)
            googlenews.get_news(str(companyName))
            results = googlenews.results()
            print("number of results", len(results))
            for result in results:
                dateResult = []
                dateResult.append(str(result['title']))
                dateResult.append(result['datetime'])
                dateResult.append("https://" + str(result['link']))
                writer.writerow(dateResult)
            # time.sleep(randint(50, 65))