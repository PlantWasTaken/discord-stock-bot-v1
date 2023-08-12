#DO NYOT CHANGE UWU DIS WORKEY 
import pandas as pd
from rich.progress import track
import yfinance as yf
from datetime import date, timedelta

import numpy as np
import tensorflow as tf
from tensorflow import keras
import random
from keras import layers

from sklearn.preprocessing import MinMaxScaler

from backtest import get_graph

def get_model(ticker, future_steps, interval):
    ticker = ticker #'5253.T' #AMZN'  #'TSLA'
    interval = interval
    future_steps = future_steps
    SEQ_LEN = 60

    start = date.today() - timedelta(days=7)
    end = date.today()

    data = yf.download(ticker, start=start, end=end,interval=interval)
    df = pd.DataFrame(data)['Close']
    df.to_csv(r'data\\'+ ticker+'.csv')

    # Normalize the data
    scaler = MinMaxScaler()
    normalized_prices = scaler.fit_transform(df.values.reshape(-1,1))

    # Prepare sequences and labels
    
    sequences = []
    labels = []

    for i in range(len(normalized_prices) - SEQ_LEN):
        seq = normalized_prices[i:i+SEQ_LEN]
        label = normalized_prices[i+SEQ_LEN]
        sequences.append(seq)
        labels.append(label)

    X = np.array(sequences)
    y = np.array(labels)

    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.LSTM(64, activation='relu', input_shape=(SEQ_LEN, 1), return_sequences=True))
    model.add(tf.keras.layers.Dropout(0.2))
    model.add(tf.keras.layers.LSTM(32, activation='relu', return_sequences=False))
    model.add(tf.keras.layers.Dropout(0.2))
    model.add(tf.keras.layers.Dense(1))

    model.compile(optimizer=tf.keras.optimizers.Adam(), loss='mse')

    model.fit(X, y, epochs=5, batch_size=32,use_multiprocessing=True,verbose=2)

    # Save the model
    model.save('models/'+ticker+'.h5')

    get_graph(ticker,future_steps,interval)

#get_model('TSLA', 60, '1m')
