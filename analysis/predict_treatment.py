import argparse
import logging
import os

from keras.models import load_model

import numpy as np
import utils
import model.net as net
from model.data_loader import load_data
from model.utils import set_logger
from model.utils import Params

parser = argparse.ArgumentParser()
parser.add_argument('--model_name', default='base_model',
        help = "Name of directory containing model to load")

if __name__ == '__main__':
    '''
    Load model and generate predicted treatment
    '''
    args = parser.parse_args()

    # loading model
    model_path = os.path.join('experiments/treatment', args.model_name, 'weights_best.hdf5')
    model = load_model(model_path)

    # loading data
    data = load_data(['train', 'val', 'test'], 'treatment', 'data')

    for split in ['train', 'val', 'test']:
        print("Predicting on {}".format(split))
        preds = model.predict(data[split]['data'])
        save_path = os.path.join('data/response', split, 'expression.csv')
        np.savetxt(save_path, preds, delimiter=',')
        print("- done.")
