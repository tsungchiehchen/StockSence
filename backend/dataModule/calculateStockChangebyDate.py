import pandas as pd
import csv
import json
import time


def getdataframe():
    df = pd.read_csv('./dataset/Stocks Symbols.csv')

    # select mid, large, and mega market cap
    df = df.loc[df['Market_Cap'] > 2000000000.00]

    # get columns name: Symbol, Market_Cap, Sector
    df = df.loc[:, ["Symbol", "Market_Cap", "Sector"]]

    return df


def getStocksChange(symbol, start_date, end_date):
    df = pd.read_csv('./dataset/Historical Price/' + symbol + '.csv')

    try:
        start_price = float(df.loc[df["Date"] == start_date]["Close"])
        end_price = float(df.loc[df["Date"] == end_date]["Close"])

        change = round(((end_price - start_price) / start_price) * 100, 2)
    except:
        change = None

    return change


def writetoCSV(objects):
    # field names
    fields = ['sector', 'name', 'rate', 'market cap']
    filename = "./dataset/stockData.csv"

    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)

        writer.writeheader()

        writer.writerows(objects)


def convertCSVtoJSON():
    df = pd.read_csv('./dataset/stockData.csv')

    tech_children = []
    consumer_discretionary_children = []
    health_care_children = []
    finance_children = []
    industrials_children = []
    consumer_staples_children = []
    utilities_children = []
    energy_children = []
    telecommunications_children = []
    real_estate_children = []
    miscellaneous_children = []
    basic_materials_children = []

    # process children in each sector
    for i in range(len(df)):
        sector = df.iloc[i]["sector"]
        name = df.iloc[i]["name"]
        rate = df.iloc[i]["rate"]
        value = df.iloc[i]["market cap"]
        d = {}
        d['rate'] = rate
        d['name'] = name
        d['value'] = value

        if sector == "Technology":
            tech_children.append(d)
        elif sector == "Health Care":
            health_care_children.append(d)
        elif sector == "Consumer Discretionary":
            consumer_discretionary_children.append(d)
        elif sector == "Finance":
            finance_children.append(d)
        elif sector == "Industrials":
            industrials_children.append(d)
        elif sector == "Consumer Staples":
            consumer_staples_children.append(d)
        elif sector == "Utilities":
            utilities_children.append(d)
        elif sector == "Energy":
            energy_children.append(d)
        elif sector == "Telecommunications":
            telecommunications_children.append(d)
        elif sector == "Real Estate":
            real_estate_children.append(d)
        elif sector == "Miscellaneous":
            miscellaneous_children.append(d)
        elif sector == "Basic Materials":
            basic_materials_children.append(d)

    # add each sector name to its children
    tech_sector_result = {}
    tech_sector_result["name"] = "Technology"
    tech_sector_result["children"] = tech_children

    consumer_disct_result = {}
    consumer_disct_result["name"] = "Consumer Discretionary"
    consumer_disct_result["children"] = consumer_discretionary_children

    health_care_result = {}
    health_care_result["name"] = "Health Care"
    health_care_result["children"] = health_care_children

    finance_result = {}
    finance_result["name"] = "Finance"
    finance_result["children"] = finance_children

    industrials_result = {}
    industrials_result["name"] = "Industrials"
    industrials_result["children"] = industrials_children

    consumer_staples_result = {}
    consumer_staples_result["name"] = "Consumer Staples"
    consumer_staples_result["children"] = consumer_staples_children

    utilities_result = {}
    utilities_result["name"] = "Utilities"
    utilities_result["children"] = utilities_children

    energy_result = {}
    energy_result["name"] = "Energy"
    energy_result["children"] = energy_children

    telecommunications_result = {}
    telecommunications_result["name"] = "Telecommunications"
    telecommunications_result["children"] = telecommunications_children

    real_estate_result = {}
    real_estate_result["name"] = "Real Estate"
    real_estate_result["children"] = real_estate_children

    miscellaneous_result = {}
    miscellaneous_result["name"] = "Miscellaneous"
    miscellaneous_result["children"] = miscellaneous_children

    basic_materials_result = {}
    basic_materials_result["name"] = "Basic Materials"
    basic_materials_result["children"] = basic_materials_children

    # add all sector to overall market
    overall_market = {}

    overall_market_children = []
    overall_market_children.append(tech_sector_result)
    overall_market_children.append(consumer_disct_result)
    overall_market_children.append(health_care_result)
    overall_market_children.append(finance_result)
    overall_market_children.append(industrials_result)
    overall_market_children.append(consumer_staples_result)
    overall_market_children.append(utilities_result)
    overall_market_children.append(energy_result)
    overall_market_children.append(telecommunications_result)
    overall_market_children.append(real_estate_result)
    overall_market_children.append(miscellaneous_result)
    overall_market_children.append(basic_materials_result)

    overall_market["name"] = "MARKET"
    overall_market["children"] = overall_market_children

    return json.dumps(overall_market, indent=4)


def processAllStocksChange(start_date, end_date):
    df = getdataframe()

    all_changes = []
    for i in range(len(df)):
        symbol = df.iloc[i]["Symbol"]
        sector = df.iloc[i]["Sector"]
        marketCap = df.iloc[i]["Market_Cap"]

        change = getStocksChange(symbol, start_date, end_date)

        if change != None:
            # store in dict
            d = {}
            d['sector'] = sector
            d['name'] = symbol
            d['rate'] = change
            # normalize Market_Cap by dividing 10^9
            d['market cap'] = marketCap / (10 ** 9)
            all_changes.append(d)

    print("Stock Change Calculated")
    writetoCSV(all_changes)
    change_in_json = convertCSVtoJSON()
    file = open('../frontend/flask/static/stockData.json', 'w')
    file.write(change_in_json)
    file.close()


# testing
# start_date = "2017-01-03"
# end_date = "2018-01-02"

# jsonFile = processAllStocksChange(start_date, end_date)

# file = open('stock_price_changes.json', 'w')
# file.write(jsonFile)
# file.close()
