import argparse
import logging
import os
import csv
import sys
import pandas as pd

from keras.models import load_model

import numpy as np
import utils
import model.net as net
from model.data_loader import load_data
from model.utils import set_logger
from model.utils import Params

parser = argparse.ArgumentParser()
parser.add_argument('stage', help = "Which stage of network to evaluate")
parser.add_argument('restore_file', help = "Name of directory containing weights to load")

# Generate 100,000 p vectors from normal dist

mu = np.zeros(2344)
cov = np.identity(2344)
sample_data = np.random.multivariate_normal(mu, cov, 100000)

# Sanity check
print(mu.shape)
print(cov.shape)
print(sample_data.shape)

def evaluate(model, stage, data):
    '''
    Evaluate the model over entire test set
    
    Args:
        model: (keras.Model) the neural network
        data: (dict) test data containing 'data' and 'labels'

    Returns:
        err: (float) one of MSE or Misclassification Error
    '''
    preds = model.predict(sample_data)
    preds = (preds > 0.5).astype(int)
    

    return preds

def save_dataset(dataset, save_dir, fname):
    """Writes sentences.txt and labels.txt files in save_dir from dataset

    Args:
        dataset: (np.array) 
        save_dir: (string)
        fname: (string)
    """
    dataset = np.array(dataset)

    # Create directory if it doesn't exist
    print("Saving %s in %s..." % (fname, save_dir))
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Export the dataset
    np.savetxt(os.path.join(save_dir, fname), dataset, delimiter=',')
    print("- done.")

if __name__ == '__main__':
    '''
    Evaluate model on the test set
    '''
    args = parser.parse_args()
    set_logger(os.path.join(args.restore_file, 'simulate_data.log'))
    
    # reloading model
    logging.info("Loading weights...")
    model = load_model(os.path.join(args.restore_file, 'weights_best.hdf5'))
    logging.info("- done.")

    # load data
    logging.info("Loading the datasets...")
    data = sample_data
    logging.info("- done.")

    predictions = evaluate(model, args.stage, data)
    save_dataset(sample_data, 'data/simulate', 'expression.csv')
    save_dataset(predictions, 'data/simulate', 'outcomes.csv')
