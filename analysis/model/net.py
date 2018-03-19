from __future__ import absolute_import, division, print_function, unicode_literals

import keras
import keras.backend as K
from keras.layers import (Dense, Dropout)
from keras.models import Sequential
from keras.regularizers import l2
from keras.constraints import maxnorm
from keras.utils import np_utils

import numpy as np

def feed_forward_net(input_layer, output_layer, params): 
    '''
    Helper function for building a Keras feed forward network.

    Args:
        input_layer: (keras.Input) input object appropriate for data
        output_layer: (keras.layer) function for output layer

    params: (dict) includes
        hidden_layers: (int) list of layer sizes
        activations: (string) list of activations to use for each layer; coerced to list if 
                    only one is provided
        dropout_rate: (float) 
        l2: (float) l2 regularization parameter
        constrain_norm: (boolean) whether to use kernel_constraint in dense layers

    Returns:
        output of final layer of network (i.e. predictions)
    '''

    state = input_layer
    if isinstance(params.activations, str):
        activations = [params.activations] * len(params.hidden_layers)

    for h, a in zip(params.hidden_layers, activations):
        if params.l2 > 0.:
            w_reg = keras.regularizers.l2(params.l2)
        else:
            w_reg = None
        const = maxnorm(2) if params.constrain_norm else  None
        state = Dense(h, activation=a, kernel_regularizer=w_reg, kernel_constraint=const)(state)
        if params.dropout_rate > 0.:
            state = Dropout(params.dropout_rate)(state)
    
    return output_layer(state)

def accuracy(outputs, labels, stage):
    '''
    Compute accuracy, given outputs and labels for all tokens
    
    Args:
        outputs: (np.ndarray) output of model
        labels: (np.ndarray) true labels
        stage: (string) one of either 'treatment' or 'response'

    '''
    # calculate MSE for treatment model
    if stage == 'treatment':
        error = ((labels - output) ** 2).mean(axis=1)

    # calculate misclassification error for response model
    if stage == 'response':
        labels = labels > 0.5
        error = (labels - output).mean()

    return error

metrics = {
        'accuracy': accuracy,
}

