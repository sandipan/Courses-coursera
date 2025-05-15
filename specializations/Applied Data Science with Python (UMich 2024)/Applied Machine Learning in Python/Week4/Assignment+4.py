
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.0** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-machine-learning/resources/bANLa) course resource._
# 
# ---

# ## Assignment 4 - Understanding and Predicting Property Maintenance Fines
# 
# This assignment is based on a data challenge from the Michigan Data Science Team ([MDST](http://midas.umich.edu/mdst/)). 
# 
# The Michigan Data Science Team ([MDST](http://midas.umich.edu/mdst/)) and the Michigan Student Symposium for Interdisciplinary Statistical Sciences ([MSSISS](https://sites.lsa.umich.edu/mssiss/)) have partnered with the City of Detroit to help solve one of the most pressing problems facing Detroit - blight. [Blight violations](http://www.detroitmi.gov/How-Do-I/Report/Blight-Complaint-FAQs) are issued by the city to individuals who allow their properties to remain in a deteriorated condition. Every year, the city of Detroit issues millions of dollars in fines to residents and every year, many of these fines remain unpaid. Enforcing unpaid blight fines is a costly and tedious process, so the city wants to know: how can we increase blight ticket compliance?
# 
# The first step in answering this question is understanding when and why a resident might fail to comply with a blight ticket. This is where predictive modeling comes in. For this assignment, your task is to predict whether a given blight ticket will be paid on time.
# 
# All data for this assignment has been provided to us through the [Detroit Open Data Portal](https://data.detroitmi.gov/). **Only the data already included in your Coursera directory can be used for training the model for this assignment.** Nonetheless, we encourage you to look into data from other Detroit datasets to help inform feature creation and model selection. We recommend taking a look at the following related datasets:
# 
# * [Building Permits](https://data.detroitmi.gov/Property-Parcels/Building-Permits/xw2a-a7tf)
# * [Trades Permits](https://data.detroitmi.gov/Property-Parcels/Trades-Permits/635b-dsgv)
# * [Improve Detroit: Submitted Issues](https://data.detroitmi.gov/Government/Improve-Detroit-Submitted-Issues/fwz3-w3yn)
# * [DPD: Citizen Complaints](https://data.detroitmi.gov/Public-Safety/DPD-Citizen-Complaints-2016/kahe-efs3)
# * [Parcel Map](https://data.detroitmi.gov/Property-Parcels/Parcel-Map/fxkw-udwf)
# 
# ___
# 
# We provide you with two data files for use in training and validating your models: train.csv and test.csv. Each row in these two files corresponds to a single blight ticket, and includes information about when, why, and to whom each ticket was issued. The target variable is compliance, which is True if the ticket was paid early, on time, or within one month of the hearing data, False if the ticket was paid after the hearing date or not at all, and Null if the violator was found not responsible. Compliance, as well as a handful of other variables that will not be available at test-time, are only included in train.csv.
# 
# Note: All tickets where the violators were found not responsible are not considered during evaluation. They are included in the training set as an additional source of data for visualization, and to enable unsupervised and semi-supervised approaches. However, they are not included in the test set.
# 
# <br>
# 
# **File descriptions** (Use only this data for training your model!)
# 
#     train.csv - the training set (all tickets issued 2004-2011)
#     test.csv - the test set (all tickets issued 2012-2016)
#     addresses.csv & latlons.csv - mapping from ticket id to addresses, and from addresses to lat/lon coordinates. 
#      Note: misspelled addresses may be incorrectly geolocated.
# 
# <br>
# 
# **Data fields**
# 
# train.csv & test.csv
# 
#     ticket_id - unique identifier for tickets
#     agency_name - Agency that issued the ticket
#     inspector_name - Name of inspector that issued the ticket
#     violator_name - Name of the person/organization that the ticket was issued to
#     violation_street_number, violation_street_name, violation_zip_code - Address where the violation occurred
#     mailing_address_str_number, mailing_address_str_name, city, state, zip_code, non_us_str_code, country - Mailing address of the violator
#     ticket_issued_date - Date and time the ticket was issued
#     hearing_date - Date and time the violator's hearing was scheduled
#     violation_code, violation_description - Type of violation
#     disposition - Judgment and judgement type
#     fine_amount - Violation fine amount, excluding fees
#     admin_fee - $20 fee assigned to responsible judgments
# state_fee - $10 fee assigned to responsible judgments
#     late_fee - 10% fee assigned to responsible judgments
#     discount_amount - discount applied, if any
#     clean_up_cost - DPW clean-up or graffiti removal cost
#     judgment_amount - Sum of all fines and fees
#     grafitti_status - Flag for graffiti violations
#     
# train.csv only
# 
#     payment_amount - Amount paid, if any
#     payment_date - Date payment was made, if it was received
#     payment_status - Current payment status as of Feb 1 2017
#     balance_due - Fines and fees still owed
#     collection_status - Flag for payments in collections
#     compliance [target variable for prediction] 
#      Null = Not responsible
#      0 = Responsible, non-compliant
#      1 = Responsible, compliant
#     compliance_detail - More information on why each ticket was marked compliant or non-compliant
# 
# 
# ___
# 
# ## Evaluation
# 
# Your predictions will be given as the probability that the corresponding blight ticket will be paid on time.
# 
# The evaluation metric for this assignment is the Area Under the ROC Curve (AUC). 
# 
# Your grade will be based on the AUC score computed for your classifier. A model which with an AUROC of 0.7 passes this assignment, over 0.75 will recieve full points.
# ___
# 
# For this assignment, create a function that trains a model to predict blight ticket compliance in Detroit using `train.csv`. Using this model, return a series of length 61001 with the data being the probability that each corresponding ticket from `test.csv` will be paid, and the index being the ticket_id.
# 
# Example:
# 
#     ticket_id
#        284932    0.531842
#        285362    0.401958
#        285361    0.105928
#        285338    0.018572
#                  ...
#        376499    0.208567
#        376500    0.818759
#        369851    0.018528
#        Name: compliance, dtype: float32

# In[17]:

import pandas as pd
import numpy as np
import matplotlib.pylab as plt

def preprocess(X):
    one_hot = pd.get_dummies(X['city'])
    for column in ['state', 'violation_code', 'dosposition']:
        one_hot = one_hot.merge(pd.get_dummies(X['state']), left_index=True, right_index=True) #merge
    one_hot = one_hot.join(X[['fine_amount', 'admin_fee', 'state_fee',                               'late_fee', 'discount_amount','clean_up_cost', 'judgment_amount']])    
    return one_hot

def preprocess2(X):
    from sklearn.preprocessing import LabelEncoder
    le=LabelEncoder()
    for col in ['state', 'violation_code', 'disposition']:
        le.fit(X[col].tolist())
        X[col]=le.transform(X[col].tolist())
    #print(set(X['grafitti_status'].tolist()))
    #X['hearing_date'] = pd.to_datetime(X['hearing_date'])
    #X['ticket_issued_date'] = pd.to_datetime(X['ticket_issued_date'])
    #X['days'] = X['hearing_date'] - X['ticket_issued_date']
    #print(X['days'])
    X = X[['state', 'violation_code', 'disposition', 'fine_amount', 'admin_fee', 'state_fee',            'late_fee', 'discount_amount','clean_up_cost', 'judgment_amount']]   ##'grafitti_status', \
    return X

def blight_model():
    
    from sklearn.metrics import roc_auc_score
    from sklearn.model_selection import train_test_split
    #from sklearn.ensemble import RandomForestClassifier
    #from sklearn.svm import SVC
    from sklearn.ensemble import GradientBoostingClassifier

    pd.set_option('display.max_columns', None)

    # Your code here
    train = pd.read_csv('train.csv', encoding = 'ISO-8859-1')
    #print(train.shape, train.columns)
    #print(train.head())
    #train.to_csv('C:\\courses\\Coursera\\Current\\ML Python\\Week4\\train.csv')
    #train.plot.hist()
    #plt.show()
    train = train[pd.notnull(train.compliance)]
    X_train, y_train = train.drop('compliance', axis=1), train.compliance
    #X_train_ohe = preprocess(X_train)
    #print(X_train_ohe.shape)
    #print(X_train_ohe)
    X_train = preprocess2(X_train) 
    
    #X_train, X_test, y_train, y_test = train_test_split(X_train_ohe, y_train, test_size=0.33, random_state=42)
    #X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=0.33, random_state=42)
    #clf = RandomForestClassifier(random_state=0)
    #clf = SVC()
    #clf = GradientBoostingClassifier()
    #clf.fit(X_train, y_train)
    #y_pred = clf.predict_proba(X_test)[:,1]
    #print(roc_auc_score(y_test, y_pred))
    
    clf = GradientBoostingClassifier()
    clf.fit(X_train, y_train)
    test = pd.read_csv('test.csv', encoding = 'ISO-8859-1')
    ids = test.ticket_id
    X_test = preprocess2(test) 
    y_pred = pd.Series(clf.predict_proba(X_test)[:,1], index=ids, name='compliance')
    
    return y_pred # Your answer here

blight_model()


# In[ ]:



