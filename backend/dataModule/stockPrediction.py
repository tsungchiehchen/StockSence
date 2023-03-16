from keras.layers import LSTM
from keras.layers import Dense
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split

from keras.models import Sequential
from keras.layers import Dense, LSTM
from keras.callbacks import EarlyStopping
from keras import optimizers
from tensorflow import keras

import pandas as pd
import numpy as np
import pickle
import financialanalysis as fa
import matplotlib.pyplot as plt
import time


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


def stock_prediction_inference(symbol, num_days):
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

    previousPrices = np.array(list(StockData['Close'].iloc[-num_days:]))

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
    print(NextPeriodPrice)


# testing
symbol = 'AAPL'

# setting parameter for training LSTM model
train_on_number_of_days = 60
future_number_of_days = 30

# stock_prediction_train_model(
#     symbol, train_on_number_of_days, future_number_of_days)

stock_prediction_inference(symbol, train_on_number_of_days)
