import numpy as np
from keras import layers, regularizers
import tensorflow as tf
from keras.layers import Input, Dense, Activation
from keras.layers import Dropout
from keras.models import Model
from keras.preprocessing import image
from keras.utils import layer_utils
from keras.utils.data_utils import get_file
from keras.applications.imagenet_utils import preprocess_input
import pydot
from IPython.display import SVG
from keras.utils.vis_utils import model_to_dot
from keras.utils import plot_model
from kt_utils import *

import keras.backend as K
K.set_image_data_format('channels_last')
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow

import data_simulator

%matplotlib inline

numpy.random.seed(123)

def OneStageModel(input_shape):
	# Define input placeholder 
	X_input = Input(input_shape)


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



# Create the model
oneStageNN = OneStageModel(X_train.shape[1:])

# Compile the model to optimize with RMSprop and MSE loss 
oneStageNN.compile(optimizer='adam', loss='mse')

# Train the model
oneStageNN.fit(X_train, Y_train, epochs=40, batch_size=50)


# Make predictions
preds = oneStageNN.evaluate(X_test, Y_test, batch_size=32, verbose=1, sample_weight=None)

print()
print ("Loss = " + str(preds[0]))
print ("Test Accuracy = " + str(preds[1]))


