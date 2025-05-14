# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 00:45:31 2016
@author: sandipan"""
import pandas as pd

data = pd.read_csv('gapminder.csv', low_memory=False)  # make sure that the csv file is on the path
print (len(data)) #number of observations (rows)
print (len(data.columns)) # number of variables (columns)

# 3 numeric variables selected: lifeexpectancy, employrate, internetuserate
# since all the variables are continuous variables, each of them needs to be binned first and then frequency table will be computed on the binned variables
data['lifeexpectancy'] = data['lifeexpectancy'].convert_objects(convert_numeric=True)
data['employrate'] = data['employrate'].convert_objects(convert_numeric=True)
data['internetuserate'] = data['internetuserate'].convert_objects(convert_numeric=True)

# plot the histogram of lifeexpectancy 
pd.DataFrame.hist(data, 'lifeexpectancy')
# create 3 equal width intervals (categories) of lifeexpectancy values: with ages in between (47.758, 59.661], (59.661, 71.527] and (71.527, 83.394].
data['lifeexpectancy_binned'], bins = pd.cut(data['lifeexpectancy'], 3, retbins=True)
#counts and percentages (i.e. frequency distributions) for each variable
print data['lifeexpectancy_binned'].value_counts(sort=False)
print data['lifeexpectancy_binned'].value_counts(sort=False, normalize=True)

# plot the histogram of employrate 
pd.DataFrame.hist(data, 'employrate')
# create 3 equal width intervals (categories) of employrate values: (31.949, 49.0667], (49.0667, 66.133] and (66.133, 83.2].
data['employrate_binned'], bins = pd.cut(data['employrate'], 3, retbins=True)
#counts and percentages (i.e. frequency distributions) for each variable
print data['employrate_binned'].value_counts(sort=False)
print data['employrate_binned'].value_counts(sort=False, normalize=True)

# plot the histogram of internetuserate 
pd.DataFrame.hist(data, 'internetuserate')
# create 2 equal width intervals (categories) of internetuserate values: (0.115, 47.924] and (0.115, 47.924].
data['internetuserate_binned'], bins = pd.cut(data['internetuserate'], 2, retbins=True)
#counts and percentages (i.e. frequency distributions) for each variable
print data['internetuserate_binned'].value_counts(sort=False)
print data['internetuserate_binned'].value_counts(sort=False, normalize=True)	

