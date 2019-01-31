"""Read, split and save the datasets for our model"""

import csv
import os
import sys
import pandas as pd
import numpy as np


def load_dataset(path_csv):
    """Loads dataset into memory from csv file"""

    print("Loading expression...")
    expression_levels = pd.read_csv(path_csv['expression'])
    print("- done.\nLoading variants...")
    gene_variants = pd.read_csv(path_csv['variants'])
    print("- done.\nLoading outcomes...")
    outcomes = pd.read_csv(path_csv['outcomes'])

    print("- done.\nTransforming expression...")
    expression_levels = expression_levels.drop('mrna', axis=1).transpose().as_matrix()
    print("- done.\nTransforming variants...")
    gene_variants = gene_variants.drop('hugo', axis=1).transpose().as_matrix()
    print("- done.\nTransforming outcomes...")
    outcomes = outcomes['outcome'].as_matrix()
    print("- done.")

    # shuffling data
    permute = np.random.permutation(outcomes.shape[0])
    expression_levels = expression_levels[permute,:]
    gene_variants = gene_variants[permute,:]
    outcomes = outcomes[permute]

    # normalize p
    expression_levels = (expression_levels-np.mean(expression_levels,axis=0))/np.std(expression_levels,axis=0)

    return expression_levels, gene_variants, outcomes


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


if __name__ == "__main__":
    # Check that the dataset exists 
    expression_path = 'data/raw/expression_levels_subset.csv'
    variants_path = 'data/raw/gene_variants.csv'
    outcomes_path = 'data/raw/outcomes.csv'

    for path in [expression_path, variants_path, outcomes_path]:
        msg = "{} file not found".format(path)
        assert os.path.isfile(path), msg

    # Load the dataset into memory
    dataset_paths = {'expression' : expression_path,
            'variants' : variants_path,
            'outcomes' : outcomes_path}

    print("Loading dataset into memory...")
    expression, variants, outcomes = load_dataset(dataset_paths)
    print("- done")

    # Split the dataset into train, dev and split (dummy split with no shuffle)
    train_expression = expression[:int(0.7*expression.shape[0]),:]
    dev_expression = expression[int(0.7*expression.shape[0]) : int(0.85*expression.shape[0]),:]
    test_expression = expression[int(0.85*expression.shape[0]):,:]

    train_variants = variants[:int(0.7*variants.shape[0]),:]
    dev_variants = variants[int(0.7*variants.shape[0]) : int(0.85*variants.shape[0]),:]
    test_variants = variants[int(0.85*variants.shape[0]):,:]
    
    train_outcomes = outcomes[:int(0.7*outcomes.shape[0])]
    dev_outcomes = outcomes[int(0.7*outcomes.shape[0]) : int(0.85*outcomes.shape[0])]
    test_outcomes = outcomes[int(0.85*outcomes.shape[0]):]
 
    # Save the datasets to files
    save_dataset(train_expression, 'data/treatment/train', 'expression.csv')
    save_dataset(dev_expression, 'data/treatment/val', 'expression.csv')
    save_dataset(test_expression, 'data/treatment/test', 'expression.csv')

    save_dataset(train_variants, 'data/treatment/train', 'variants.csv')
    save_dataset(dev_variants, 'data/treatment/val', 'variants.csv')
    save_dataset(test_variants, 'data/treatment/test', 'variants.csv')

    save_dataset(train_outcomes, 'data/response/train', 'outcomes.csv')
    save_dataset(dev_outcomes, 'data/response/val', 'outcomes.csv')
    save_dataset(test_outcomes, 'data/response/test', 'outcomes.csv')
