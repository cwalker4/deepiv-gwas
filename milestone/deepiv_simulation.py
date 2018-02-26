import data_simulator

import numpy as np

from deepiv.models import Treatment, Response
import deepiv.architectures as architectures
import deepiv.densities as densities

import tensorflow as tf

from keras.layers import Input, Dense
from keras.models import Model
from keras.layers.merge import Concatenate

n = 5000

x, z, p, y, g_true = data_simulator.demand(n, ypcor=0.5)

print("Data shapes:\n\
        Features:{x} \n\
        Instruments: {z} \n\
        Policy: {p} \n\
        Response: {y}".format(**{'x':x.shape, 'z':z.shape,
                                 't':p.shape, 'y':y.shape}))

# FIRST STAGE: z->p model
instruments = Input(shape=z.shape[1],), name = "instruments")
features = Input(shape=(x.shape[1],), name = "features")
treatment_input = Concatenate(axis=1)([instruments, features])

hidden = [128, 64, 32]

activation = "tanh" # TODO: try relu
l2_reg = 0.0001

n_components = 10

est_treat = architectures.feed_forward_net(treatment_input, 
                                           lambda x: densities.mixture_of_gaussian_output(x, n_components),
                                           hidden_layers=hidden,
                                           dropout_rate=dropout_rate,
                                           l2 = l2_reg,
                                           activations=activation)

treatment_model = Treatment(inputs=[instruments, features], outputs=est_treat)
treatmnet_model.compile('adam',
                        loss='mixture_of_gaussians',
                        n_components = n_components)

treatment_model.fit([z, x], p, epochs = epochs, batch_size = batch_size)

# SECOND STAGE: p->y model

treatment = Input(shape=(p.shape[1],), name="treatment")
response_input = Concatenate(axis=1)([features, policy])

est_response = architectures.feed_forward_net(response_input, Dense(1),
                                              activations=act,
                                              hidden_layers=hidden,
                                              l2 = l2_reg,
                                              dropout_rate=dropout_rate)

response_model = Response(treatment=treatment_model,
                          inputs=[features, policy],
                          outputs = est_response)

response_model.compile('adam', loss='mse')
response_model.fit([z, x], y, epochs=epochs, verbose=1,
                   batch_size=batch_siez, samples_per_batch=2)

performance = data_simulator.monte_carlo_error(lambda x,z,t: response_model.predict([x,p]), datafunction)
print("Out of sample performance evaluated against the true function: %f" % performance)




