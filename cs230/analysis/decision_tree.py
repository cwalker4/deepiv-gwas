"Read, split and save the datasets for our model"""
import csv
import os
import sys
import pandas as pd
import numpy as np
from sklearn import tree
import graphviz


print("Loading expression...")
expression_levels = pd.read_csv('data/simulate/covariance/expression.csv')
#expression_levels = pd.read_csv('data/treatment/test/expression.csv')
print("- done.\nLoading outcomes...")
outcomes = pd.read_csv('data/simulate/covariance/outcomes.csv')
#outcomes = pd.read_csv('data/response/test/outcomes.csv')
print("- done.")

decision_tree = tree.DecisionTreeClassifier(criterion='entropy', max_depth=4)
print("Fitting tree...")
decision_tree = decision_tree.fit(expression_levels, outcomes)
print("- done.")

dot_data = tree.export_graphviz(decision_tree, out_file=None,
        filled=True, rotate=True)
graph = graphviz.Source(dot_data)

graph.render("decision_tree")
