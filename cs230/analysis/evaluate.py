import argparse
import logging
import os

from keras.models import load_model

from sklearn import metrics
import numpy as np
import matplotlib.pyplot as plt

import utils
import model.net as net
from model.data_loader import load_data
from model.utils import set_logger
from model.utils import Params

parser = argparse.ArgumentParser()
parser.add_argument('stage', help = "Which stage of network to evaluate")
parser.add_argument('restore_file', help = "Name of directory containing weights to load")


def plot_roc(labels, preds):
    fpr, tpr, thresholds = metrics.roc_curve(labels, preds)
    auc = metrics.auc(fpr, tpr)
    # plotting
    plt.plot(fpr, tpr, 'b', label = 'AUC = %.5f' % auc)
    plt.legend()
    plt.plot([0,1], [0,1], 'k--')
    plt.xlim([0,1])
    plt.ylim([0,1])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.show()


def evaluate(model, stage, data):
    '''
    Evaluate the model over entire test set
    
    Args:
        model: (keras.Model) the neural network
        data: (dict) test data containing 'data' and 'labels'

    Returns:
        err: (float) one of MSE or Misclassification Error
    '''
    preds = model.predict(data['data'])
    preds_raw = np.copy(preds)
    
    metrics = {}

    if stage == 'treatment':
        error = ((preds - data['labels']) ** 2).mean() # taking the mean over all errors 
        metrics['mse'] = error

    if stage == 'response':
        labels = (data['labels'] > 0.5).astype(int)
        labels = labels[:,np.newaxis]
        #print(labels.shape)
        preds = (preds > 0.5).astype(int)
        #print(preds.shape)
        error = (preds != labels).mean()
        print(error)
        n_misclassified = (preds != labels).sum()
        metrics['misclassification err'] = error
        metrics['n_misclassified'] = n_misclassified

    plot_roc(labels, preds_raw)

    return metrics

if __name__ == '__main__':
    '''
    Evaluate model on the test set
    '''
    args = parser.parse_args()
    set_logger(os.path.join(args.restore_file, 'evaluate.log'))
    
    # reloading model
    logging.info("Loading weights...")
    model = load_model(os.path.join(args.restore_file, 'weights_best.hdf5'))
    logging.info("- done.")

    # load data
    logging.info("Loading the datasets...")
    data = load_data(['test'], args.stage, 'data')
    logging.info("- done.")

    test_metrics = evaluate(model, args.stage, data['test'])
    save_path = os.path.join(args.restore_file, "metrics_test.json")
    utils.save_dict_to_json(test_metrics, save_path)



