# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 16:26:46 2015

@author: sandipan
"""

#%matplotlib inline
#ipython nbconvert --to html notebook.ipynb

#from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from sklearn.cross_validation import train_test_split, cross_val_score
from sklearn.linear_model import LassoLarsCV, LinearRegression, Lasso
 
#Load the dataset
GM_data = pd.read_csv("C:\\courses\\Coursera\\Current\\ML for Data Analysis\\Week3\\gapminder.csv")
data_clean = GM_data.dropna()

data_clean.dtypes
data_clean.describe()

data_clean = data_clean.drop('country', 1)
data_clean = data_clean.convert_objects(convert_numeric=True) #.dtypes
#data_clean = data_clean.dropna()
data_clean = data_clean.dropna(subset = ['lifeexpectancy'])
data_clean.head()

#upper-case all DataFrame column names
#data_clean.columns = map(str.upper, data_clean.columns)

#select predictor variables and target variable as separate data sets  
predvar= data_clean[['incomeperperson','alcconsumption','armedforcesrate',
                     'breastcancerper100th','co2emissions','femaleemployrate','hivrate', 
                     'internetuserate','oilperperson','polityscore','relectricperperson',
                     'suicideper100th','employrate','urbanrate']]

#data_clean['lifeexpectancy'] = pd.cut(data_clean.lifeexpectancy, bins=[0,70,100])
#data_clean = data_clean.dropna(subset = ['lifeexpectancy'])

target = data_clean.lifeexpectancy
 
# standardize predictors to have mean=0 and sd=1
predictors=predvar.copy()
predictors = predictors.fillna(predictors.median())
from sklearn import preprocessing
predictors['incomeperperson']=preprocessing.scale(predictors['incomeperperson'].astype('float64'))
predictors['alcconsumption']=preprocessing.scale(predictors['alcconsumption'].astype('float64'))
predictors['armedforcesrate']=preprocessing.scale(predictors['armedforcesrate'].astype('float64'))
predictors['breastcancerper100th']=preprocessing.scale(predictors['breastcancerper100th'].astype('float64'))
predictors['co2emissions']=preprocessing.scale(predictors['co2emissions'].astype('float64'))
predictors['femaleemployrate']=preprocessing.scale(predictors['femaleemployrate'].astype('float64'))
predictors['hivrate']=preprocessing.scale(predictors['hivrate'].astype('float64'))
predictors['internetuserate']=preprocessing.scale(predictors['internetuserate'].astype('float64'))
predictors['oilperperson']=preprocessing.scale(predictors['oilperperson'].astype('float64'))
predictors['polityscore']=preprocessing.scale(predictors['polityscore'].astype('float64'))
predictors['relectricperperson']=preprocessing.scale(predictors['relectricperperson'].astype('float64'))
predictors['suicideper100th']=preprocessing.scale(predictors['suicideper100th'].astype('float64'))
predictors['employrate']=preprocessing.scale(predictors['employrate'].astype('float64'))
predictors['urbanrate']=preprocessing.scale(predictors['urbanrate'].astype('float64'))

# split data into train and test sets
pred_train, pred_test, tar_train, tar_test = train_test_split(predictors, target, 
                                                              test_size=.3, random_state=123)

# specify the lasso regression model
model=LassoLarsCV(cv=10, precompute=False).fit(pred_train,tar_train)

# print variable names and regression coefficients
dict(zip(predictors.columns, model.coef_))

# plot coefficient progression
m_log_alphas = -np.log10(model.alphas_)
ax = plt.gca()
plt.plot(m_log_alphas, model.coef_path_.T)
plt.axvline(-np.log10(model.alpha_), linestyle='--', color='k', label='alpha CV')
plt.ylabel('Regression Coefficients')
plt.xlabel('-log(alpha)')
plt.legend()
plt.title('Regression Coefficients Progression for Lasso Paths')

# plot mean square error for each fold
m_log_alphascv = -np.log10(model.cv_alphas_)
plt.figure()
plt.plot(m_log_alphascv, model.cv_mse_path_, ':')
plt.plot(m_log_alphascv, model.cv_mse_path_.mean(axis=-1), 'k',
         label='Average across the folds', linewidth=2)
plt.axvline(-np.log10(model.alpha_), linestyle='--', color='k',
            label='alpha CV')
plt.legend()
plt.xlabel('-log(alpha)')
plt.ylabel('Mean squared error')
plt.title('Mean squared error on each fold')
 
  
lasso = Lasso()
alphas = np.logspace(-4, -.5, 30)

scores = list()
scores_std = list()

for alpha in alphas:
    lasso.alpha = alpha
    this_scores = cross_val_score(lasso, pred_train, tar_train, n_jobs=1)
    scores.append(np.mean(this_scores))
    scores_std.append(np.std(this_scores))

plt.figure(figsize=(4, 3))
plt.semilogx(alphas, scores)
# plot error lines showing +/- std. errors of the scores
plt.semilogx(alphas, np.array(scores) + np.array(scores_std) / np.sqrt(len(pred_train)),
             'b--')
plt.semilogx(alphas, np.array(scores) - np.array(scores_std) / np.sqrt(len(pred_train)),
             'b--')
plt.ylabel('CV score')
plt.xlabel('alpha')
plt.axhline(np.max(scores), linestyle='--', color='.5')
plt.title('Choosing the right alpha with grid-search and cross validation')

      

# MSE from training and test data
from sklearn.metrics import mean_squared_error
train_error = mean_squared_error(tar_train, model.predict(pred_train))
test_error = mean_squared_error(tar_test, model.predict(pred_test))
print ('training data MSE')
print(train_error)
print ('test data MSE')
print(test_error)

# R-square from training and test data
rsquared_train=model.score(pred_train,tar_train)
rsquared_test=model.score(pred_test,tar_test)
print ('training data R-square')
print(rsquared_train)
print ('test data R-square')
print(rsquared_test)

# Create linear regression object
regr = LinearRegression()
# Train the model using the training sets
regr.fit(pred_train, tar_train)
# The coefficients
#print('Coefficients: \n', regr.coef_)
print(dict(zip(predictors.columns, regr.coef_)))
# The mean square error
train_error = mean_squared_error(tar_train, regr.predict(pred_train))
test_error = mean_squared_error(tar_test, regr.predict(pred_test))
print ('training data MSE')
print(train_error)
print ('test data MSE')
print(test_error)

# R-square from training and test data
rsquared_train=regr.score(pred_train,tar_train)
rsquared_test=regr.score(pred_test,tar_test)
print ('training data R-square')
print(rsquared_train)
print ('test data R-square')
print(rsquared_test)

