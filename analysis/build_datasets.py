"""Read, split and save the kaggle dataset for our model"""

import csv
import os
import sys
import pandas as pd
import numpy as np


def load_dataset(path_csv):
    """Loads dataset into memory from csv file"""

    expression_levels = pd.read_csv(path_csv['expression_levels'])
    gene_variants = pd.read_csv(path_csv['gene_variants'])
    outcomes = pd.read_csv(path_csv['outcomes'])

    expression_levels = expression_levels.drop('mrna', axis=1).transpose().as_matrix()
    gene_variants = gene_variants.drop('hugo', axis=1).transpose().as_matrix()
    outcomes = outcomes['outcome'].as_matrix()

    return expression_levels, gene_variants, outcomes


def save_dataset(dataset, save_dir, fname):
    """Writes sentences.txt and labels.txt files in save_dir from dataset

    Args:
        dataset: (np.array) 
        save_dir: (string)
        fname: (string)
    """
    # Create directory if it doesn't exist
    print("Saving in {}...".format(save_dir))
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Export the dataset
    np.savetxt(os.path.join(save_dir, fname), dataset, ',')
    print("- done.")


if __name__ == "__main__":
    # Check that the dataset exists 
    expression_path = 'data/raw/expression_levels_subset.csv'
    variants_path = 'data/raw/gene_variants.csv'
    outcomes_path = 'data/raw/outcomes.csv'

    msg = "{} file not found".format(path_dataset)
    for path in [expression_path, variants_path, outcomes_path]:
        assert os.path.isfile(path), msg

    # Load the dataset into memory
    dataset_paths = {'expression' : expression_path,
            'gene_variants' : variants_path,
            'outcomes' : outcomes_path}

    print("Loading dataset into memory...")
    expression, variants, outcomes = load_dataset(dataset_paths)
    print("- done")

    # Split the dataset into train, dev and split (dummy split with no shuffle)
    train_expression = expression[:int(0.7*expression.shape[0])]
    dev_expression = expression[int(0.7*expression.shape[0]) : int(0.85*expression.shape[0])]
    test_expression = expression[int(0.86*expression.shape[0])]

    train_variants = variants[:int(0.7*variants.shape[0])]
    dev_variants = variants[int(0.7*variants.shape[0]) : int(0.85*variants.shape[0])]
    test_variants = variants[int(0.86*variants.shape[0])]
    
    train_outcomes = outcomes[:int(0.7*outcomes.shape[0])]
    dev_outcomes = outcomes[int(0.7*outcomes.shape[0]) : int(0.85*outcomes.shape[0])]
    test_outcomes = outcomes[int(0.86*outcomes.shape[0])]
 
    # Save the datasets to files
    save_dataset(train_expression, 'data/treatment/train', 'expression.csv')
    save_dataset(dev_expression, 'data/treatment/dev', 'expression.csv')
    save_dataset(test_expression, 'data/treatment/test', 'expression.csv')

    save_dataset(train_variants, 'data/treatment/train', 'variants.csv')
    save_dataset(dev_variants, 'data/treatment/dev', 'variants.csv')
    save_dataset(test_variants, 'data/treatment/test', 'variants.csv')

    save_dataset(train_outcomes, 'data/response/train', 'outcomes.csv')
    save_dataset(dev_outcomes, 'data/response/dev', 'outcomes.csv')
    save_dataset(test_outcomes, 'data/respone/test', 'outcomes.csv')
