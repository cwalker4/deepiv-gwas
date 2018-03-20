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
expression_levels = pd.read_csv('data/simulate/expression.csv')
print("- done.\nLoading outcomes...")
outcomes = pd.read_csv('data/simulate/outcomes.csv')
print("- done.")

decision_tree = tree.DecisionTreeClassifier(max_depth = 5, min_samples_leaf = 10)
print("Fitting tree...")
decision_tree = decision_tree.fit(expression_levels, outcomes)
print("- done.")

dot_data = tree.export_graphviz(decision_tree, out_file='data/simulate/tree_raw.pdf') 
graph = pydotplus.graph_from_dot_data(dot_data) 
graph.write_pdf("data/simulate/tree_processed.pdf")
#graph = graphviz.Source(dot_data) 
#graph.render('data/simulate/tree.gv', view = True) 