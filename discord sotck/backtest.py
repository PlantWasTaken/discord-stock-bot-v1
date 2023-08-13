import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler

def get_graph(ticker,future_steps,interval):
    SEQ_LEN = 60
    ticker = ticker

    df = pd.read_csv(r'data\\'+ ticker+'.csv')['Close']
    scalar = MinMaxScaler()
    scaled_data = scalar.fit_transform(df.values.reshape(-1,1))

    # Load the saved model
    loaded_model = tf.keras.models.load_model(r'models\\'+ticker+".h5")


    # Number of future time steps to predict
    future_steps = future_steps

    #ft = np.array([scaled_data[i:i+SEQ_LEN] for i in range(future_steps-SEQ_LEN)])
    ft = np.array([scaled_data[-SEQ_LEN-i:-i] for i in range(1,future_steps+1)])

    pred = loaded_model.predict(ft,verbose=2)

    Y2 = df[-SEQ_LEN:]
    predicted_prices = scalar.inverse_transform(np.array(pred))

    predicted_prices = np.squeeze(predicted_prices)


    #print(len(Y2),len(predicted_prices))
    prices = list(Y2) + list(predicted_prices)

    x = np.linspace(0,((future_steps*2)-1), num=(2*future_steps))

    #print(len(x))
    plt.plot(x[:future_steps+1], prices[:future_steps+1])
    plt.plot(x[future_steps:], prices[future_steps:])

    plt.title(ticker+' Stock price prediction', fontsize=15)

    plt.xlabel("Time "+interval+" intervals", fontsize = 15)
    plt.ylabel("Price",fontsize = 15)

    plt.savefig(r'graphs\\'+ticker+'.png')
    #print(ticker)
