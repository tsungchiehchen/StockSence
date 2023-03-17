from keras.layers import LSTM
from keras.layers import Dense
from sklearn.preprocessing import MinMaxScaler

from keras.models import Sequential
from keras.layers import Dense, LSTM
from keras.callbacks import EarlyStopping
from keras import optimizers
from tensorflow import keras

import pandas as pd
import numpy as np
import pickle
import time
import json
import datetime


def stock_prediction_train_model(symbol, train_on_number_of_days, future_number_of_days, TestingRecords=0):
    StockData = pd.read_csv('./dataset/Historical Price/' + symbol + '.csv')
    # train on the closing prices of each day
    FullData = StockData[['Close']].values

    # Feature Scaling for fast training of neural networks
    sc = MinMaxScaler()

    DataScaler = sc.fit(FullData)
    X = DataScaler.transform(FullData)
    X = X.reshape(X.shape[0],)

    # split into samples
    X_samples = list()
    y_samples = list()

    NumerOfRows = len(X)

    # Iterate thru the values to create combinations
    for i in range(train_on_number_of_days, NumerOfRows-future_number_of_days, 1):
        x_sample = X[i-train_on_number_of_days:i]
        y_sample = X[i:i+future_number_of_days]
        X_samples.append(x_sample)
        y_samples.append(y_sample)

    # Reshape the Input as a 3D (samples, Time Steps, Features)
    X_data = np.array(X_samples)
    X_data = X_data.reshape(X_data.shape[0], X_data.shape[1], 1)
    # don't need to reshape y as a 3D data  as it is supposed to be a single column only
    y_data = np.array(y_samples)

    # Splitting the data into train and test
    if TestingRecords == 0:
        X_train, X_test = X_data, []
        y_train, y_test = y_data, []
    else:
        X_train = X_data[:-TestingRecords]
        X_test = X_data[-TestingRecords:]
        y_train = y_data[:-TestingRecords]
        y_test = y_data[-TestingRecords:]

    # Defining Input shapes for LSTM
    train_on_number_of_days = X_train.shape[1]
    TotalFeatures = X_train.shape[2]

    # Initialising the RNN
    regressor = Sequential()

    # Adding the First input hidden layer and the LSTM layer
    # return_sequences = True, means the output of every time step to be shared with hidden next layer
    regressor.add(LSTM(units=10, activation='relu', input_shape=(
        train_on_number_of_days, TotalFeatures), return_sequences=True))

    # Adding the Second hidden layer and the LSTM layer
    regressor.add(LSTM(units=5, activation='relu', input_shape=(
        train_on_number_of_days, TotalFeatures), return_sequences=True))

    # Adding the Third hidden layer and the LSTM layer
    regressor.add(LSTM(units=5, activation='relu', return_sequences=False))

    # Adding the output layer
    # Notice the number of neurons in the dense layer is now the number of future time steps
    # Based on the number of future days we want to predict
    regressor.add(Dense(units=future_number_of_days))

    # Compiling the RNN
    regressor.compile(optimizer='adam', loss='mean_squared_error')

    # Measuring the time taken by the model to train
    StartTime = time.time()

    # Fitting the RNN to the Training set
    regressor.fit(X_train, y_train, batch_size=5, epochs=100)

    # load pre-train model to pickle
    fileName = './dataset/preTrained model/' + symbol + '.sav'
    pickle.dump(regressor, open(fileName, 'wb'))

    EndTime = time.time()
    print("############### Total Time Taken: ", round(
        (EndTime-StartTime)/60), 'Minutes #############')


def get_number_of_days(end_date):
    start_date = datetime.date(2023, 2, 28)
    num_days = np.busday_count(start_date, end_date)
    return num_days


def stock_prediction_inference(symbol, start_date, end_date):
    num_days = get_number_of_days(end_date)

    # read historical price again
    StockData = pd.read_csv('./dataset/Historical Price/' + symbol + '.csv')
    FullData = StockData[['Close']].values
    # load pretrained model
    model_path = './dataset/preTrained model/' + symbol + '.sav'
    filename = model_path
    regressor = pickle.load(open(filename, 'rb'))
    # Feature Scaling for fast training of neural networks
    sc = MinMaxScaler()

    DataScaler = sc.fit(FullData)

    previousPrices = np.array(list(StockData['Close'].iloc[-60:]))

    # Reshaping the data to (-1, 1)because its a single entry
    previousPrices = previousPrices.reshape(-1, 1)

    # Scaling the data on the same level on which model was trained
    X_test = DataScaler.transform(previousPrices)

    NumberofSamples = 1
    train_on_number_of_days = X_test.shape[0]
    NumberofFeatures = X_test.shape[1]
    # Reshaping the data as 3D input
    X_test = X_test.reshape(
        NumberofSamples, train_on_number_of_days, NumberofFeatures)

    # Generating the predictions for the next period
    NextPeriodPrice = regressor.predict(X_test)

    # Generating the prices in original scale
    NextPeriodPrice = DataScaler.inverse_transform(NextPeriodPrice)
    # get the slice that the user interested
    NextPeriodPrice = NextPeriodPrice[0].tolist()[:num_days]

    # write NextPeriodPrice to json
    writePricetoJSON(StockData, start_date, end_date,
                     NextPeriodPrice, num_days)
    writeDatetoJSON(StockData, start_date, end_date, num_days)


def writePricetoJSON(StockData, start_date, end_date, future_price, num_days):
    # filter rows based on start_date and end_date to get historical date
    historical_price = StockData[(StockData['Date'] >= start_date)
                                 & (StockData['Date'] <= end_date)]
    historical_price = historical_price['Close'].to_list()
    combined = historical_price + future_price

    json_string = json.dumps(json.loads(json.dumps(
        [{"data": combined}]), parse_float=lambda x: round(float(x), 2)))

    with open('./dataset/price prediction/price.json', 'w') as f:
        f.write(json_string)


def writeDatetoJSON(StockData, start_date, end_date, num_days):
    # filter rows based on start_date and end_date to get historical date
    historical_date = StockData[(StockData['Date'] >= start_date)
                                & (StockData['Date'] <= end_date)]
    historical_date = historical_date['Date'].to_list()

    future_date = ["2023-03-01", "2023-03-02", "2023-03-03", "2023-03-06",
                   "2023-03-07", "2023-03-08", "2023-03-09", "2023-03-10",
                   "2023-03-13", "2023-03-14", "2023-03-15", "2023-03-16",
                   "2023-03-17", "2023-03-20", "2023-03-21", "2023-03-22",
                   "2023-03-23", "2023-03-24", "2023-03-27", "2023-03-28",
                   "2023-03-29", "2023-03-30", "2023-03-31", "2023-04-03",
                   "2023-04-04", "2023-04-05", "2023-04-06", "2023-04-07",
                   "2023-04-10", "2023-04-11"]
    future_date = future_date[:num_days]
    date = historical_date + future_date

    with open('./dataset/price prediction/date.json', 'w') as outfile:
        json.dump(date, outfile)


# testing
symbol = 'AAPL'

# setting parameter for training LSTM model
train_on_number_of_days = 60
future_number_of_days = 30

# stock_prediction_train_model(
#     symbol, train_on_number_of_days, future_number_of_days)

start_date = "2022-12-01"
end_date = "2023-03-09"
# end_date = "2023-04-11"
stock_prediction_inference(symbol, start_date, end_date)
