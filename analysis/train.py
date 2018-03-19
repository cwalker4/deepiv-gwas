"""Train first-stage model"""

import argparse
import logging
import os

import tensorflow as tf

from keras.models import Model
from keras.layers import Input, Dense
from keras import optimizers
from keras.callbacks import ModelCheckpoint, EarlyStopping

import model.net as net
from model.utils import Params
from model.utils import set_logger
from model.data_loader import load_data

import numpy as np


parser = argparse.ArgumentParser()
parser.add_argument('stage', help="Which stage network to train")
parser.add_argument('--model', default="base_model", help="Name of directory containing params.json")
parser.add_argument('--restore_dir', default=None,
                    help="Optional, directory containing weights to reload before training")


def train_and_evaluate(model, train_data, val_data, optimizer, metrics, params, model_dir, restore_file=None):
    '''
    Trains the Keras model

    Args:
        model: (keras.Model) the neural network
        train_data: (dict) train data with keys 'data' and 'labels'
        val_data: (dict) validation data with keys 'data' and 'labels'
        optimizer: (keras.optimizers) optimizer for parameters of model
        loss_fn: a function that takes batch_labels and batch_output and computes batch loss
        metrics: (dict) a dictionary of functions that compute a metric using output and labels of a batch
        params: (Params) hyperparameters
        model_dir: (string) directory containing config, weights and log 
    '''
    model.compile(optimizer=optimizer, loss=params.loss_fn)
    check_path = os.path.join(model_dir, "weights.improvement-{epoch:02d}-{val_loss:.5f}.hdf5")
    early_stopping = EarlyStopping(monitor='val_loss', patience=5, mode='min')
    checkpointer = ModelCheckpoint(check_path, monitor='val_loss', mode='min', save_best_only=True)

    model.fit(train_data['data'], train_data['labels'], epochs=params.num_epochs,
              batch_size = params.batch_size, validation_data=(val_data['data'], val_data['labels']),
              callbacks=[checkpointer, early_stopping])


if __name__ == '__main__':
    # Set the random seed for the whole graph for reproductible experiments
    np.random.seed(123)
    tf.set_random_seed(123)

    # Load the parameters from the experiment params.json file in model_dir
    args = parser.parse_args()
    json_path = os.path.join('experiments', args.stage, args.model, 'params.json')
    assert os.path.isfile(json_path), "No json configuration file found at {}".format(json_path)
    params = Params(json_path)

    # Check that we are not overwriting some previous experiment
    # Comment these lines if you are developing your model and don't care about overwritting
    #model_dir_has_best_weights = os.path.isdir(os.path.join(args.model_dir, "best_weights"))
    #overwritting = model_dir_has_best_weights and args.restore_dir is None
    #assert not overwritting, "Weights found in model_dir, aborting to avoid overwrite"

    # Set the logger
    set_logger(os.path.join('experiments', args.stage, args.model, 'train.log'))

    logging.info("Loading the datasets...")

    # load data
    data_dir = os.path.join('data', args.stage)
    data = load_data(['train', 'val'], args.stage, 'data')
    train_data = data['train']
    val_data = data['val']

    logging.info("- done.")

    # specifying train and val dataset sizes
    params.train_size = train_data['size']
    params.val_size = val_data['size']

    logging.info("- done.")

    # define the model 
    input_layer = Input(shape=(train_data['data'].shape[1],))
    output_layer = Dense(train_data['labels'].shape[1], activation=params.output_activation)

    ffn = net.feed_forward_net(input_layer, output_layer, params)
    optimizer = optimizers.adam(lr=params.learning_rate) # add others params to .json if we want
    model = Model(inputs=input_layer, outputs=ffn)

    # fetch loss function and metrics
    metrics = net.metrics

    # train the model
    logging.info("Starting training for {} epoch(s)".format(params.num_epochs))
    train_and_evaluate(model, train_data, val_data, optimizer, metrics,
                       params, os.path.join('experiments', args.stage, args.model)) 
