from __future__ import absolute_import, division, print_function, unicode_literals

import keras
import keras.backend as K
from keras.layers import (Dense, Dropout)
from keras.models import Sequential
from keras.regularizers import l2
from keras.constraints import maxnorm
from keras.utils import np_utils

import numpy as np

def feed_forward_net(input, output, hidden_layers=[64, 64], activations='relu',
                     dropout_rate=0., l2=0., constrain_norm=False):
    '''
    Helper function for building a Keras feed forward network.

    Args:
        input: (keras.Input) input object appropriate for data
        output: (keras.layers) function representing final layer of network 
        hidden_layers: (int) list of layer sizes
        activations: (string) list of activations to use for each layer; coerced to list if 
                    only one is provided
        dropout_rate: (float) 
        l2: (float) l2 regularization parameter
        constrain_norm: (boolean) whether to use kernel_constraint in dense layers

    Returns:
        output of final layer of network (i.e. predictions)
    '''

    state = input
    if isinstance(activations, str):
        activations = [activations] * len(hidden_layers)

    for h, a in zip(hidden_layers, activations):
        if l2 > 0.:
            w_reg = keras.regularizers.l2(l2)
        else:
            w_reg = None
        const = maxnorm(2) if constrain_norm else  None
        state = Dense(h, activation=a, kernel_regularizer=w_reg, kernel_constraint=const)(state)
        if dropout_rate > 0.:
            state = Dropout(dropout_rate)(state)
    
    return output(state)
