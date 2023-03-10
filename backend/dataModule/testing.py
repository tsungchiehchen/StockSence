############################### Below is testing for Regular Expression #########################################
# import re

# testing regex: Only floating point
# pattern = r'^\d+\.\d+$'
# strings = ['3.14', '42.32', '0.5', '7.77', '885954.5', '44']

# for s in strings:
#     if re.match(pattern, s):
#         print(f'{s} is a floating point number')
#     else:
#         print(f'{s} is not a floating point number')


# testing regex: Float with "%"
# pattern = r'-?\d+\.\d+%$'

# float_strs = ['3.14', '-0.1%', '2.5', '10.0%', '3']

# for s in float_strs:
#     if re.match(pattern, s):
#         print(s, 'is a valid floating point number with %')
#     else:
#         print(s, 'is not a valid floating point number with %')


# testing regex: Float with 'M''K'
# pattern = r'\d+\.\d+M'

# float_strs = ['3156.2M', '0.356M', '25.56K', '10.0M', '3.5']

# for s in float_strs:
#     if re.match(pattern, s):
#         print(s, 'is a valid number with M')
#     else:
#         print(s, 'is not a valid number with M')

# testing regex: Float with 'K'
# pattern = r'\d+\.\d+K'

# float_strs = ['3156.2M', '0.356M', '25.56K', '10.0M', '3.5']

# for s in float_strs:
#     if re.match(pattern, s):
#         print(s, 'is a valid number with K')
#     else:
#         print(s, 'is not a valid number with K')
############################### End testing for Regular Expression #########################################

############################### Below is testing for Hierarchical Clustering #########################################
import json
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.cluster import AgglomerativeClustering
import scipy.cluster.hierarchy as sch
import matplotlib.pyplot as plt

# below is for generating distance matrix
from scipy.spatial.distance import squareform
from scipy.spatial.distance import pdist

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
    'Short Float',  # is %
    'Short Ratio'  # not %
]

# Read in the data with missing values
data = pd.read_csv('./server/financial_indicators.csv')
data.drop('Symbol', axis='columns', inplace=True)

data["Short Float"] = np.nan
data["Short Ratio"] = np.nan

# loop through each row and extract the values
for i in range(len(data)):
    # use eval() to convert the string tuple into a tuple of floats
    value = eval(data.iloc[i]["Short Float / Ratio"])
    if pd.notna(value):
        short_float, short_ratio = value
        data.at[i, "Short Float"] = short_float
        data.at[i, "Short Ratio"] = short_ratio
# drop the original column
data.drop(columns=["Short Float / Ratio"], inplace=True)

# Define the imputer object
imputer = IterativeImputer()

# Use the imputer object to fill in missing values in the dataframe
data = pd.DataFrame(imputer.fit_transform(data), columns=data.columns)

# perform normalization
normalized_data = (data.loc[:, metrics] - data.loc[:,
                   metrics].mean()) / data.loc[:, metrics].std()

# Perform hierarchical clustering on the imputed data
# cluster = AgglomerativeClustering(
#     n_clusters=3, affinity='euclidean', linkage='ward')
# labels = cluster.fit_predict(normalized_data)

# add cluster labels to data dataframe
# data['Cluster Label'] = labels
# print(data)
# Print the clustering results
# print(labels)


# # visulaize cluster in scatter plot
# data_X = data.iloc[:, :-1].values
# target = data.iloc[:, -1].values

# plt.figure(figsize=(10, 7))
# plt.scatter(data_X[target == 0, 1], data_X[target == 0, 15],
#             s=100, c='blue', label='Cluster 0')
# plt.scatter(data_X[target == 1, 1], data_X[target == 1, 15],
#             s=100, c='yellow', label='Cluster 1')
# plt.scatter(data_X[target == 2, 1], data_X[target == 2, 15],
#             s=100, c='green', label='Cluster 2')
# plt.legend()
# plt.xlabel('P/B')
# plt.ylabel('Short Ratio')
# plt.show()


# normalized_data.index = ['AAPL', 'MSFT', 'GOOG',
#                          'AMZN', 'PCAR', 'TSLA',
#                          'NVDA', 'META', 'ASML',
#                          'AVGO', 'PEP', 'COST',
#                          'AZN', 'CSCO']

# plot out the dendrogram
# print(sch.linkage(normalized_data, method='ward'))
# sch.dendrogram(sch.linkage(normalized_data, method='ward', metric='euclidean'),
#                labels=normalized_data.index)
# plt.axhline(y=3.5, color='r', linestyle='--')
# plt.ylabel("Euclidean Distance")
# plt.show()


# plot out line graph to indicate how each group fluctuate between variables
# colors = sns.color_palette('bright', n_colors=14)

# for i in range(len(normalized_data)):
#     new_data = pd.Series(
#         normalized_data.iloc[i], index=normalized_data.columns)
#     plt.legend(normalized_data.index, loc='upper left')
#     plt.plot(new_data.T, color=colors[i])

# plt.xticks(rotation=90)
# plt.show()
############################### End testing for Hierarchical Clustering #########################################

############################### Below is testing for generating fake data.json #########################################

# Create hierarchical data in a nested dictionary format
# data = {
#     "name": "Parent",
#     "children": [
#         {
#             "name": "Child 1",
#             "value": 10
#         },
#         {
#             "name": "Child 2",
#             "value": 20
#         }
#     ]
# }

# # Convert the nested dictionary to a JSON string
# json_str = json.dumps(data)

# # Write the JSON string to a file
# with open("data.json", "w") as outfile:
#     outfile.write(json_str)


############################### End testing for generating fake data.json #########################################

############################### Below is testing for calculate distance matrix #########################################
distance_matrix = pd.DataFrame(
    squareform(pdist(normalized_data)),
    columns=[['AAPL', 'MSFT', 'GOOG',
              'AMZN', 'PCAR', 'TSLA',
              'NVDA', 'META', 'ASML',
              'AVGO', 'PEP', 'COST',
              'AZN', 'CSCO']],
    index=['AAPL', 'MSFT', 'GOOG',
           'AMZN', 'PCAR', 'TSLA',
           'NVDA', 'META', 'ASML',
           'AVGO', 'PEP', 'COST',
           'AZN', 'CSCO']
)
# print(distance_matrix) # verifies, shows distance matrix

# show AAPL distance with repect to other stocks
stock_list = ['AAPL', 'MSFT', 'GOOG',
              'AMZN', 'PCAR', 'TSLA',
              'NVDA', 'META', 'ASML',
              'AVGO', 'PEP', 'COST',
              'AZN', 'CSCO']

AAPL_distantce_matrix = distance_matrix.loc['AAPL'].to_list()
############################### End testing for calculate distance matrix #########################################
