"""Read, split and save the datasets for our model"""

import csv
import os
import sys
import pandas as pd
import numpy as np
from sklearn import tree
import graphviz
import pydotplus


print("Loading expression...")
expression_levels = pd.read_csv('data/simulate/covariance/expression.csv')
#expression_levels = pd.read_csv('data/treatment/test/expression.csv')
print("- done.\nLoading outcomes...")
outcomes = pd.read_csv('data/simulate/covariance/outcomes.csv')
#outcomes = pd.read_csv('data/response/test/outcomes.csv')
print("- done.")

decision_tree = tree.DecisionTreeClassifier(min_samples_leaf = 50) #max_depth = 20
print("Fitting tree...")
decision_tree = decision_tree.fit(expression_levels, outcomes)
print("- done.")

print(">>>>> Trained fruit_classifier <<<<<")
print(decision_tree)


with open("figures/decision_tree.dot", "w") as f:
    f = tree.export_graphviz(decision_tree, out_file=f)


#### Put this into the command line in the folder "figures" to get pdf of results
#dot -Tpdf decision_tree.dot -o decision_tree.pdf
#open -a preview decision_tree.pdf
