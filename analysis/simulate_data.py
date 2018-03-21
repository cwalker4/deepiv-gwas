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

print("Loading data for var-cov matrix...")
expression_training = pd.read_csv('data/treatment/train/expression.csv')

# Generate 100,000 p vectors from normal dist

mu = np.zeros(2344)
cov_1 = np.identity(2344)
cov_2 = expression_training.transpose().as_matrix() @ expression_training.as_matrix()/100000

sample_data_ind = np.random.multivariate_normal(mu, cov_1, 100000)
sample_data_cov = np.random.multivariate_normal(mu, cov_2, 100000)

# Sanity check
print(mu.shape)
print(cov_1.shape)
print(cov_2.shape)
print(sample_data_ind.shape)
print(sample_data_cov.shape)

def evaluate(model, stage, data):
    '''
    Evaluate the model over entire test set
    
    Args:
        model: (keras.Model) the neural network
        data: (dict) test data containing 'data' and 'labels'

    Returns:
        err: (float) one of MSE or Misclassification Error
    '''
    preds = model.predict(data)
    preds = (preds> 0.5).astype(int)
    

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

    predictions_ind = evaluate(model, args.stage, sample_data_ind)
    predictions_cov = evaluate(model, args.stage, sample_data_cov)
    save_dataset(sample_data_ind, 'data/simulate/independent', 'expression.csv')
    save_dataset(predictions_ind, 'data/simulate/independent', 'outcomes.csv')
    save_dataset(sample_data_cov, 'data/simulate/covariance', 'expression.csv')
    save_dataset(predictions_cov, 'data/simulate/covariance', 'outcomes.csv')
