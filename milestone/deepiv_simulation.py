import data_simulator

import numpy as np

import pdb

from deepiv.models import Treatment, Response
import deepiv.architectures as architectures
import deepiv.densities as densities

import tensorflow as tf

from keras.layers import Input, Dense
from keras.models import Model
from keras.layers.merge import Concatenate

def deepiv(n, rho):
    '''
    Generates simulated data and runs both stages of the deepiv architecture

    Arguments:
    ypcor -- the amount of endogeneity in our model

    Returns:
    performance -- out of sample monte carlo error against true causal function

    '''
    dropout_rate = min(1000./(1000. + n), 0.5)
    epochs = int(1500000./float(n)) # heuristic to get epochs
    batch_size = 100

    x, z, p, y, g_true = data_simulator.demand(n, ypcor=rho)

    # FIRST STAGE: z->p model
    instruments = Input(shape=(z.shape[1],), name = "instruments")
    features = Input(shape=(x.shape[1],), name = "features")
    treatment_input = Concatenate(axis=1)([instruments, features])

    hidden = [128, 64, 32]

    activation = "tanh" 
    l2_reg = 0.0001

    n_components = 10

    est_treat = architectures.feed_forward_net(treatment_input, 
                                               lambda x: densities.mixture_of_gaussian_output(x, n_components),
                                               hidden_layers=hidden,
                                               dropout_rate=dropout_rate,
                                               l2 = l2_reg,
                                               activations=activation)

    treatment_model = Treatment(inputs=[instruments, features], outputs=est_treat)
    print("Fitting treatment...")
    treatment_model.compile('adam',
                            loss='mixture_of_gaussians',
                            n_components = n_components)

    treatment_model.fit([z, x], p, epochs = epochs, batch_size = batch_size, verbose=0)

    # SECOND STAGE: p->y model
    print("Fitting response...")
    activation = "relu"

    policy = Input(shape=(p.shape[1],), name="policy")
    response_input = Concatenate(axis=1)([features, policy])

    est_response = architectures.feed_forward_net(response_input, Dense(1),
                                                  activations=activation,
                                                  hidden_layers=hidden,
                                                  l2 = l2_reg,
                                                  dropout_rate=dropout_rate)

    response_model = Response(treatment=treatment_model,
                              inputs=[features, policy],
                              outputs = est_response)

    response_model.compile('adam', loss='mse')
    response_model.fit([z, x], y, epochs=epochs, verbose=0,
                       batch_size=batch_size, samples_per_batch=2)

    performance = data_simulator.monte_carlo_error(lambda x,z,p: response_model.predict([x,p]), 
                                                   rho=0,
                                                   ntest=n)
    return performance




