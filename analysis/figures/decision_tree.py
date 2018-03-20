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
#expression_levels = pd.read_csv('data/treatment/test/expression.csv')
print("- done.\nLoading outcomes...")
outcomes = pd.read_csv('data/simulate/outcomes.csv')
#outcomes = pd.read_csv('data/response/test/outcomes.csv')
print("- done.")

decision_tree = tree.DecisionTreeClassifier(max_depth = 5)
print("Fitting tree...")
decision_tree = decision_tree.fit(expression_levels, outcomes)
print("- done.")

print(">>>>> Trained fruit_classifier <<<<<")
print(decision_tree)


with open("decision_tree.dot", "w") as f:
    f = tree.export_graphviz(decision_tree, out_file=f)
    
#dot -Tpdf decision_tree.dot -o decision_tree.pdf

#open -a preview decision_tree.pdf


#dot_data = tree.export_graphviz(decision_tree, out_file='data/simulate/tree_raw.pdf') 
#graph = pydotplus.graph_from_dot_data(dot_data) 
#graph.write_pdf("data/simulate/tree_processed.pdf")
#graph = graphviz.Source(dot_data) 
#graph.render('data/simulate/tree.gv', view = True) 