import numpy as np
from keras import layers, regularizers

import tensorflow as tf

from keras.layers import Input, Dense, Activation
from keras.layers import Dropout
from keras.models import Sequential

import keras.backend as K
K.set_image_data_format('channels_last')
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow

import data_simulator

from deepiv.models import Treatment, Response
import deepiv.architectures as architectures
import deepiv.densities as densities
from keras.layers.merge import Concatenate

import pdb

n = 5000
dropout_rate = min(1000./(1000. + n), 0.5)
epochs = int(1500000./float(n)) # heuristic to get epochs
batch_size = 100

x, z, p, y, g_true = data_simulator.demand(n, ypcor=0.5)

print("Data shapes:\n\
        Features:{x} \n\
        Instruments: {z} \n\
        Policy: {p} \n\
        Response: {y}".format(**{'x':x.shape, 'z':z.shape,
                              'p':p.shape, 'y':y.shape}))

hidden = [128, 64, 32]
l2_reg = 0.0001

n_components = 10

np.random.seed(123)

policy = np.concatenate((x, p), axis=1)

w_reg = regularizers.l2(l2_reg)

oneStageNN = Sequential([
	# Define 3 hidden layers with nodes 128, 64, 32 respectively 
    Dense(hidden[0], activation='relu', input_dim = 9, name='fc1', kernel_regularizer=w_reg),
    Dropout(dropout_rate),
    Dense(hidden[1], activation='relu', name='fc2', kernel_regularizer=w_reg),
    Dropout(dropout_rate),
    Dense(hidden[2], activation='relu', name='fc3', kernel_regularizer=w_reg),
    Dropout(dropout_rate),
    Dense(1, activation = 'linear', name = 'output', kernel_regularizer = w_reg) 
	])

# Compile the model to optimize with RMSprop and MSE loss 
oneStageNN.compile(optimizer='adam', loss='mse')

# Train the model
oneStageNN.fit(policy, y, epochs=epochs, batch_size=batch_size)

