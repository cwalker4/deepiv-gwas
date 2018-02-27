import numpy as np
from keras import layers, regularizers

import tensorflow as tf

from keras.layers import Input, Dense, Activation
from keras.layers import Dropout
from keras.models import Sequential
from keras.layers.merge import Concatenate

import keras.backend as K
K.set_image_data_format('channels_last')
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow

import data_simulator

import pdb

import data_generator

'''
x, z, p, y, g_true = data_simulator.demand(n, ypcor=0.5)

print("Data shapes:\n\
        Features:{x} \n\
        Instruments: {z} \n\
        Policy: {p} \n\
        Response: {y}".format(**{'x':x.shape, 'z':z.shape,
                              'p':p.shape, 'y':y.shape}))

'''
def onestage_model(n):
    hidden = [128, 64, 32]
    l2_reg = 0.0001
    dropout_rate = min(1000./(1000. + n), 0.5)

    np.random.seed(123)

    w_reg = regularizers.l2(l2_reg)

    oneStageNN = Sequential([
            # Define 3 hidden layers with nodes 128, 64, 32 respectively 
        Dense(hidden[0], activation='relu', input_dim = 9, name='fc1', kernel_regularizer=w_reg),
        Dropout(dropout_rate),
        Dense(hidden[1], activation='relu', name='fc2', kernel_regularizer=w_reg),
        Dropout(dropout_rate),
        Dense(hidden[2], activation='relu', name='fc3', kernel_regularizer=w_reg),
        Dropout(dropout_rate),
        Dense(1, activation = 'linear', name = 'output') 
            ])
    
    return oneStageNN

def g_hat_helper(pred_fn, x, p):
    policy = np.concatenate((x, p), axis=1)
    return pred_fn(policy)

def one_stage(n, rho):
    epochs = int(1500000./float(n)) # heuristic to get epochs
    batch_size = 100

    x, z, p, y, g_true = data_simulator.demand(n, ypcor=rho)
    policy = np.concatenate((x, p), axis=1)

    oneStageNN = onestage_model(n)

    # Compile the model to optimize with RMSprop and MSE loss 
    oneStageNN.compile(optimizer='adam', loss='mse')

    # Train the model
    oneStageNN.fit(policy, y, epochs=epochs, batch_size=batch_size,
                   verbose=0)

    performance = data_simulator.monte_carlo_error(lambda x,z,p: g_hat_helper(oneStageNN.predict, x, p),
                                                   rho=0,
                                                   ntest=n)

#    performance = data_generator.monte_carlo_error(lambda x,z,p: g_hat_helper(oneStageNN.predict, x, p),
#                                                   data_generator.demand)
    return performance

