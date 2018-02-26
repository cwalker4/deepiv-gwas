import numpy as np
from keras import layers, regularizers

import tensorflow as tf

from keras.layers import Input, Dense, Activation
from keras.layers import Dropout
from keras.models import Model

import keras.backend as K
K.set_image_data_format('channels_last')
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow

import data_simulator

from deepiv.models import Treatment, Response
import deepiv.architectures as architectures
import deepiv.densities as densities
from keras.layers.merge import Concatenate

n = 5000
dropout_rate = min(1000./(1000. + n), 0.5)
epochs = int(1500000./float(n)) # heuristic to get epochs
epochs = 30
batch_size = 100

x, z, p, y, g_true = data_simulator.demand(n, ypcor=0.5)

print("Data shapes:\n\
        Features:{x} \n\
        Instruments: {z} \n\
        Policy: {p} \n\
        Response: {y}".format(**{'x':x.shape, 'z':z.shape,
            'p':p.shape, 'y':y.shape}))

        # FIRST STAGE: z->p model
instruments = Input(shape=(z.shape[1],), name = "instruments")
features = Input(shape=(x.shape[1],), name = "features")
treatment_input = Concatenate(axis=1)([instruments, features])

hidden = [128, 64, 32]

activation = "tanh" # TODO: try relu
l2_reg = 0.0001

n_components = 10

np.random.seed(123)

def OneStageModel(input_shape):
    # Define input placeholder 
    X_input = Input(input_shape)

    X = X_input

        # Define 3 hidden layers with nodes 128, 64, 32 respectively 
    X = Dense(128, activation='relu', name='fc1')(X)
    Dropout(dropout_rate)
    X = Dense(64, activation='relu', name='fc2')(X)
    Dropout(dropout_rate)
    X = Dense(32, activation='relu', name='fc3')(X)
    Dropout(dropout_rate)

    # Define output layer
    X = Dense(1, activation = 'relu', name = 'output')(X)

    # Define Regularization technique on activity
    activity_regularizer = keras.regularizers.l2(l2_reg)

    # Create Model
    model = Model(inputs = X_input, outputs = X, name='OneStageModel')

    return model


policy = Input(shape=(p.shape[1],), name="policy")
response_input = Concatenate(axis=1)([features, policy])

# Create the model
oneStageNN = OneStageModel(response_input.shape[1:])

# Compile the model to optimize with RMSprop and MSE loss 
oneStageNN.compile(optimizer='adam', loss='mse')

# Train the model
oneStageNN.fit(response_input, response, epochs=epochs, batch_size=batch_size)


# Make predictions
preds = oneStageNN.evaluate(response_input, response, batch_size=batch_size, verbose=1, sample_weight=None)

print()
print ("Loss = " + str(preds[0]))
print ("Test Accuracy = " + str(preds[1]))


