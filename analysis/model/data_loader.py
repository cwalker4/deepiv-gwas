import random
import numpy as np
import os
import sys

import utils

class DataLoader(object):
    '''
    Takes care of data handling.
    '''

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
                    expression = os.path.join(data_dir, stage, split, "expression.csv")
                    variants = os.path.join(data_dir, stage, split, "variants.csv")
                    data[split]['data'] = expression
                    data[split]['labels'] = variants
                    data[split]['size'] = variants.shape[0]
                elif stage == 'response':
                    expression = os.path.join(data_dir, stage, "expression.csv")
                    outcomes = os.path.join(data_dir, stage, split, "outcomes.csv")
                    data[split]['data'] = expression
                    data[split]['labels'] = outcomes
                    data[split]['size'] = expression.shape[0]
        
        return data
