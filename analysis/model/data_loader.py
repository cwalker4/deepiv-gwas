import random
import numpy as np
import os
import sys

import utils

def load_data(self, types, stage, data_dir):
    ''' 
    loads each type of data (train, val, test) from data_dir

    Args:
        types (list) has one or more of 'train', 'val', 'test', depending on what is needed
        data_dir: (string) directory containing the dataset
        stage: (string) one of either 'treatment' or 'response'

    Returns:
        data: (dict) contains the data with labels for each type in types
     
    '''
    data = {}
    
    for split in ['train', 'val', 'test']:
        if split in types:
            data[split] = {}
            if stage == 'treatment':
                expression_path = os.path.join(data_dir, stage, split, "expression.csv")
                variants_path = os.path.join(data_dir, stage, split, "variants.csv")
                expression = np.loadtxt(expression_path, delimiter=',')
                variants = np.loadtxt(variants_path, delimiter=',')
                data[split]['data'] = expression
                data[split]['labels'] = variants
                data[split]['size'] = variants.shape[0]
            elif stage == 'response':
                expression_path = os.path.join(data_dir, stage, "expression.csv")
                outcomes_path = os.path.join(data_dir, stage, split, "outcomes.csv")
                expression = np.loadtxt(expression_path, delimiter=',')
                outcomes = np.loadtxt(loutcomes_path, delimiter=',')
                data[split]['data'] = expression
                data[split]['labels'] = outcomes
                data[split]['size'] = expression.shape[0]
    
    return data
