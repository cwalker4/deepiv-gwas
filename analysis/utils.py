''' General utility functions '''

import json
import logging

class Params():
    '''
    Loads hyperparameters from a json file

    Example usage:
    params = Params(json_path)
    print(params.learning_rate)
    params.learning_rate = 0.5 # change the value of learning_rate in params
    '''

    def __init__(self, json_path):
        self.update(json_path)

    def save(self, json_path):
        ''' saves parameters to json file'''
        with open(json_path), 'w') as f:
            json.dump(self.__dict__, f, indent = 4)

    def update(self, json_path):
        ''' loads parameters from json file'''
        with open(json_path) as f:
            params = json.load(f)
            self.__dict__.update(params)

    @property
    def dict(self):
        ''' gives dict-like access to Params instance by `params.dict['learning_rate']` '''
        return self.__dict__


def set_logger(log_path):
    ''' 
    Sets the logger to log terminal output to file `log_path`

    Args:
        log_path: (string) where to log
    '''
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # logging to a file
        file_handler = logging.fileHandler(log_path)
        file_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)%s:%(message)s'))
        logger.addHandler(file_handler)

        # logging to console
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter('%(message)s'))
        logger.addHandler(stream_handler)

def save_dict_to_json(d, json_path):
    '''
    Saves dict of floats in json file

    Args:
        d: (dict) of float-castable values (np.float, int, float, etc.)
        json_path: (string) path to json file
    '''
    with open(json_path, 'w') as f:
        # need to convert values to float for json
        d = {k: float(v) for k, v in d.items()}
        json.dump(d, f, indent=4)
