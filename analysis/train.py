"""Train first-stage model"""

import argparse
import logging
import os

import tensorflow as tf

from keras.layers import Input
from keras import optimizers
from keras.callbacks import ModelCheckpoint

from model.utils import Params
from model.utils import set_logger
from model.training import train_and_evaluate


parser = argparse.ArgumentParser()
parser.add_argument('--model_dir', default='experiments/base_model',
                    help="Directory containing params.json")
parser.add_argument('--data_dir', default='data/small', help="Directory containing the dataset")
parser.add_argument('--restore_dir', default=None,
                    help="Optional, directory containing weights to reload before training")



def train_and_evaluate(model, train_data, val_data, optimizer, loss_fn, metrics,  params, model_dir, restore_file=None):
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
    model.compile(optimizer=optimizer, loss=loss_fn)
    check_path = "weights-improvement-{epoch:02d}-{val_acc:.2f}.hdf5"
    checkpointer = MoelCheckpoint(model_dir, monitor='val_loss', mode='max', save_best_only=True)

    model.fit(train_data['data'], train_data['labels'], epochs=params.epochs,
              batch_size = params.batch_size, validation_data=(val_data['data'], val_data['labels'],
              callbacks=[checkpointer])


if __name__ == '__main__':
    # Set the random seed for the whole graph for reproductible experiments
    np.seed(123)
    tf.set_random_seed(123)

    # Load the parameters from the experiment params.json file in model_dir
    args = parser.parse_args()
    json_path = os.path.join(args.model_dir, 'params.json')
    assert os.path.isfile(json_path), "No json configuration file found at {}".format(json_path)
    params = Params(json_path)

    # Load the parameters from the dataset, that gives the size etc. into params
    json_path = os.path.join(args.data_dir, 'dataset_params.json')
    assert os.path.isfile(json_path), "No json file found at {}, run build_vocab.py".format(json_path)
    params.update(json_path)

    # Check that we are not overwriting some previous experiment
    # Comment these lines if you are developing your model and don't care about overwritting
    #model_dir_has_best_weights = os.path.isdir(os.path.join(args.model_dir, "best_weights"))
    #overwritting = model_dir_has_best_weights and args.restore_dir is None
    #assert not overwritting, "Weights found in model_dir, aborting to avoid overwrite"

    # Set the logger
    set_logger(os.path.join(args.model_dir, 'train.log'))

    logging.info("Loading the datasets...")

    # load data
    data_loader = DataLoader(args.data_dir, params)
    data = data_loader.load_data(['train', 'val'], args.data_dir)
    train_data = data['train']
    val_data = data['val']

    logging.info("- done.")

    # specifying train and val dataset sizes
    params.train_size = train_data['size']
    params.val_size = val_data['size']

    logging.info("- done.")

    # define the model 
    input_layer = Input(shape=(train_data.shape[1],))
    model = net.feed_forward_net(input_layer, params)
    optimizer = optimizers.adam(lr=params.learning_rate) # add others params to .json if we want

    # fetch loss function and metrics
    metrics = net.metrics

    # train the model
    logging.info("Starting training for {} epoch(s)".format(params.num_epochs))
    train_and_evaluate(model, train_data, val_data, optimizer, metrics,
                       params, args.model_dir) 