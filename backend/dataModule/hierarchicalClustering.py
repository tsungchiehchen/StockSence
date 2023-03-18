import pandas as pd
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re
import numpy as np
from itertools import islice

# import hierarchical clustering libraries
import scipy.cluster.hierarchy as sch
from sklearn.cluster import AgglomerativeClustering
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from scipy.spatial.distance import squareform
from scipy.spatial.distance import pdist
from ete3 import Tree
from skbio.tree import nj
from skbio import DistanceMatrix


def fundamental_metric(soup, metric):
    float_pattern = r'^\d+\.\d+$'
    float_pattern_with_percent = r'^-?\d+\.\d+%$'
    million_pattern = r'^\d+\.\d+M'
    thousand_pattern = r'^\d+\.\d+K'
    value = soup.find(text=metric).find_next(class_='snapshot-td2').text

    # classify value to categories
    if re.match(float_pattern, value):
        return float(value)
    elif re.match(float_pattern_with_percent, value):
        # value = float(value[-1])/100  # if want to discard %, use this line
        return float(value[:-1])
    elif re.match(million_pattern, value):
        return float(value[:-1]) * (10 ** 6)
    elif re.match(thousand_pattern, value):
        return float(value[:-1]) * (10 ** 3)
    elif '/' in value:
        short_float, short_ratio = value.split('/')
        # if want to discard %, use this line
        # short_float = float(short_float[-1]) / 100
        return float(short_float[:-2]), float(short_ratio)


def get_fundamental_data(df):
    for idx, symbol in enumerate(df['Symbol']):
        try:
            url = ("http://finviz.com/quote.ashx?t=" + symbol.lower())
            req = Request(url=url, headers={
                          'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'})
            response = urlopen(req)
            soup = BeautifulSoup(response, "html.parser")

            metrics = df.columns.tolist()
            metrics.remove('Symbol')
            for m in metrics:
                # special case: containing two variables in one
                if m == "Short Float / Ratio":
                    s_float, s_ratio = fundamental_metric(soup, m)
                    df.iloc[idx]['Short Float'] = s_float
                    df.iloc[idx]['Short Ratio %'] = s_ratio

                val = fundamental_metric(soup, m)
                df.iloc[idx][m] = val if val != None else np.nan
                print("Finished fetching: ", symbol)
        except Exception as e:
            print(symbol, 'not found')
    return df


def get_all_stocks_fundamental_data(metrics):
    stocks = pd.read_csv('./dataset/Stocks Symbols.csv')
    stocks = stocks.loc[stocks['Market_Cap'] > 2000000000.00]
    stock_list = stocks["Symbol"].to_list()

    df = pd.DataFrame(columns=metrics)
    df['Symbol'] = stock_list
    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]

    df = get_fundamental_data(df)
    df.to_csv('./financial_indicators.csv', index=False)


def clean_financial_indicators_df(df):
    # Seperate column "Short Float / Ratio" to two columns
    # create two new columns with default value NaN
    df["Short Float"] = np.nan
    df["Short Ratio"] = np.nan

    # loop through each row and extract the values
    for i in range(len(df)):
        # use eval() to convert the string tuple into a tuple of floats
        if not isinstance(df.iloc[i]["Short Float / Ratio"], str):
            continue
        else:
            # print(i, df.iloc[i]["Short Float / Ratio"])
            value = eval(df.iloc[i]["Short Float / Ratio"])
            if pd.notna(value):
                short_float, short_ratio = value
                df.at[i, "Short Float"] = short_float
                df.at[i, "Short Ratio"] = short_ratio
    # drop the original column
    df.drop(columns=["Short Float / Ratio"], inplace=True)


def get_json(node):
    node.name = node.name.replace("'", '')

    json = {"name": node.name}
    if node.children:
        json["children"] = []
        for ch in node.children:
            json["children"].append(get_json(ch))
    return json


def perform_hierarchical_cluster(symbol):
    fi_data = pd.read_csv('./dataModule/financial_indicators.csv')
    stock_list = fi_data['Symbol'].to_list()
    data = fi_data.drop('Symbol', axis='columns', inplace=False)

    clean_financial_indicators_df(data)

    # Define the imputer object
    imputer = IterativeImputer()

    # Use the imputer object to fill in missing values in the dataframe
    data = pd.DataFrame(imputer.fit_transform(data), columns=data.columns)

    # perform normalization
    normalized_data = (
        data.loc[:, metrics] - data.loc[:, metrics].mean()) / data.loc[:, metrics].std()

    # Perform hierarchical clustering on the imputed data
    cluster = AgglomerativeClustering(
        n_clusters=3, affinity='euclidean', linkage='ward')
    labels = cluster.fit_predict(normalized_data)

    # add cluster labels to data dataframe
    data['Cluster Label'] = labels

    distance_matrix = pd.DataFrame(
        squareform(pdist(normalized_data)),
        columns=[stock_list],
        index=stock_list
    )

    # sort distance matrix by value in ascending order
    dist = distance_matrix[symbol].to_dict()[(symbol,)]
    sorted_dist = dict(sorted(dist.items(), key=lambda item: item[1]))
    # get the first 20 elements
    resulting_dist = dict(islice(sorted_dist.items(), 21))

    if len(resulting_dist) < 3:
        with open('./dataset/stockRecommendation.json', 'w') as f:
            f.write("{}")
    else:
        subset_stock_list = list(resulting_dist.keys())

        data['Symbol'] = fi_data['Symbol']
        kept_idx = []
        for x in subset_stock_list:
            kept_idx.append(data.loc[data['Symbol'] == x].index[0])

        subset_normalized_data = normalized_data.iloc[kept_idx]
        distance_matrix = pd.DataFrame(
            squareform(pdist(subset_normalized_data)),
            columns=[subset_stock_list],
            index=subset_stock_list
        )

    # get subset of distance matrix whose distance is less than 5
    # temp = distance_matrix[symbol]
    # kept_idx = []
    # for i in range(len(temp)):
    #     if temp.iloc[i][0] < 5:
    #         kept_idx.append(i)

    # # get new distance matrix on new subset of data
    # subset_distance_matrix = distance_matrix[symbol].iloc[kept_idx]
    # subset_stock_list = list(subset_distance_matrix.index)

    # if len(kept_idx) < 3:
    #     with open('./dataset/stockRecommendation.json', 'w') as f:
    #         f.write("{}")
    # else:
    #     subset_normalized_data = normalized_data.iloc[kept_idx]
    #     distance_matrix = pd.DataFrame(
    #         squareform(pdist(subset_normalized_data)),
    #         columns=[subset_stock_list],
    #         index=subset_stock_list
    #     )

        # convert to tree structure acceptable datatype
        ids = subset_stock_list
        dm = DistanceMatrix(distance_matrix, ids)
        newick_str = nj(dm, result_constructor=str)
        t = Tree(newick_str)

        with open('./dataset/stockRecommendation.json', 'w') as f:
            f.write(str(get_json(t)).replace("'", '"'))


metrics = [
    'P/B',
    'P/E',
    'Forward P/E',
    'PEG',
    'Debt/Eq',
    'EPS (ttm)',
    'Dividend %',  # is %
    'ROE',  # is %
    'ROI',  # is %
    'EPS Q/Q',  # is %
    'Insider Own',  # is %
    'Beta',
    'Profit Margin',  # is %
    'Avg Volume',
    # 'Short Float / Ratio' # uncomment when run get_all_stocks_fundamental_data(), and comment below 2
    'Short Float',  # is %
    'Short Ratio'  # not %
]

# run this to fetch metrics for all stocks
# uncomment below when want to get fundamental data
# get_all_stocks_fundamental_data(metrics)

# testing
symbol = 'TSLA'
# symbol = 'AAPL'
# symbol = 'MSFT'
perform_hierarchical_cluster(symbol)
