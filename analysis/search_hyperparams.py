"""Peform hyperparemeters search"""

import argparse
import os
from subprocess import check_call
import sys

from model.utils import Params


PYTHON = sys.executable
parser = argparse.ArgumentParser()
parser.add_argument('stage', help="Which stage of network to train")
parser.add_argument('--model', default='learning_rate',
                    help="Directory containing params.json")


def launch_training_job(stage, model, job_name, params):
    """Launch training of the model with a set of hyperparameters in parent_dir/job_name

    Args:
        stage: (string) one of either 'treatment' or 'response'
        model: (string) name of model directory; e.g. learning_rate
        job_name: (string) unique name of job
        params: (dict) containing hyperparameters
    """
    # Create a new folder in parent_dir with unique_name "job_name"
    model_dir = os.path.join('experiments', stage, model, job_name)
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    # Write parameters in json file
    json_path = os.path.join(model_dir, 'params.json')
    params.save(json_path)

    # Launch training with this config
    cmd = "{python} train.py {stage} --model {model}".format(python=PYTHON, stage=stage, 
            model=os.path.join(model, job_name))

    print(cmd)
    check_call(cmd, shell=True)


if __name__ == "__main__":
    # Load the "reference" parameters from parent_dir json file
    args = parser.parse_args()
    json_path = os.path.join('experiments', args.stage, args.model, 'params.json')
    assert os.path.isfile(json_path), "No json configuration file found at {}".format(json_path)
    params = Params(json_path)

    # Perform hypersearch over one parameter
    #learning_rates = [1e-5, 1e-4, 1e-3, 1e-2]
    #fine_learning_rates = [1e-5, 2e-5, 3e-5, 4e-5, 5e-5, 7e-5, 1e-4, 8e-5, 9e-5, 2e-4, 3e-4]
    #l2 = [.00005, .0001, .0002, .0003, .0004, .0005, .0006]
    dropout = [.05, .075, .1, .2, .3, .4, .5]

    for val in dropout:
        # Modify the relevant parameter in params
        params.dropout_rate = val

        # Launch job (name has to be unique)
        job_name = "dropout_{}".format(val)
        launch_training_job(args.stage, args.model, job_name, params)
