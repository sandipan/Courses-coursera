# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 21:12:54 2015

@author: ldierker
"""

# -*- coding: utf-8 -*-

from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import os
import matplotlib.pylab as plt
from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
import sklearn.metrics

#os.chdir("C:\TREES")

"""
Data Engineering and Analysis
"""
#Load the dataset

#AH_data = pd.read_csv("tree_addhealth.csv")
#AH_data = pd.read_csv("C:\\courses\\Coursera\\Current\\ML\\Week1\\tree_addhealth.csv")
AH_data = pd.read_csv("C:\\courses\\Coursera\\Current\\ML\\Week1\\gapminder.csv")

data_clean = AH_data.dropna()

data_clean.dtypes
data_clean.describe()

data_clean.drop('country', 1)
data_clean.convert_objects(convert_numeric=True) #.dtypes

pd.cut(data_clean.lifeexpectancy, bins=[0,60,100])
plt.show()

"""
Modeling and Prediction
"""
#Split into training and testing sets

#predictors = data_clean[['BIO_SEX','HISPANIC','WHITE','BLACK','NAMERICAN','ASIAN',
#'age','ALCEVR1','ALCPROBS1','marever1','cocever1','inhever1','cigavail','DEP1',
#'ESTEEM1','VIOL1','PASSIST','DEVIANT1','SCHCONN1','GPA1','EXPEL1','FAMCONCT','PARACTV',
#'PARPRES']]

predictors = data_clean[['incomeperperson','alcconsumption','armedforcesrate','breastcancerper100th','co2emissions','femaleemployrate','hivrate', \
					     'internetuserate','oilperperson','polityscore','relectricperperson','suicideper100th','employrate','urbanrate']]


#targets = data_clean.TREG1
targets = data_clean.lifeexpectancy

pred_train, pred_test, tar_train, tar_test  =   train_test_split(predictors, targets, test_size=.4)

pred_train.shape
pred_test.shape
tar_train.shape
tar_test.shape

#Build model on training data
classifier=DecisionTreeClassifier()
classifier=classifier.fit(pred_train,tar_train)

predictions=classifier.predict(pred_test)

sklearn.metrics.confusion_matrix(tar_test,predictions)
sklearn.metrics.accuracy_score(tar_test, predictions)

#Displaying the decision tree
from sklearn import tree
#from StringIO import StringIO
from StringIO import StringIO
#from StringIO import StringIO 
from IPython.display import Image
out = StringIO()
tree.export_graphviz(classifier, out_file=out)
import pydotplus
#import pydot
#pydot.graph_from_dot_data(out.getvalue()).write_png("C:\\courses\\Coursera\\Current\\ML\\Week1\\dtree2.png")
graph=pydotplus.graph_from_dot_data(out.getvalue())
Image(graph.create_png())
graph.write_png("dt.png")




