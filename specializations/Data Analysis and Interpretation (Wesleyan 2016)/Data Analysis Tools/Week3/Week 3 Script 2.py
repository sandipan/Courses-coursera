# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 14:59:43 2015

@author: jml
"""
#%matplotlib inline
#ipython nbconvert --to html notebook.ipynb

import pandas
import numpy
import seaborn
import scipy
import matplotlib.pyplot as plt

data = pandas.read_csv('C:\\courses\\Coursera\\Current\\Data Analysis Tools\\Week3\\gapminder.csv', low_memory=False)

data_clean = data.drop('country', 1)
data_clean = data_clean.convert_objects(convert_numeric=True) #.dtypes
data_clean = data_clean.replace(' ', numpy.nan)
data_clean = data_clean.dropna()


import seaborn as sns
g = sns.pairplot(data=data_clean,
                  x_vars=['incomeperperson','alcconsumption','armedforcesrate',
                     'breastcancerper100th','co2emissions','femaleemployrate','hivrate', 
                     'internetuserate','oilperperson','polityscore','relectricperperson',
                     'suicideper100th','employrate','urbanrate', 'lifeexpectancy'],
                  y_vars=['lifeexpectancy'])
                  
fig, axes = plt.subplots(ncols=14)
for i, xvar in enumerate(['incomeperperson','alcconsumption','armedforcesrate',
                     'breastcancerper100th','co2emissions','femaleemployrate','hivrate', 
                     'internetuserate','oilperperson','polityscore','relectricperperson',
                     'suicideper100th','employrate','urbanrate', 'lifeexpectancy']):
    axes[i].scatter(data[xvar],data['lifeexpectancy'])

for x in ['incomeperperson','alcconsumption','armedforcesrate', \
                     'breastcancerper100th','co2emissions','femaleemployrate','hivrate',  \
                     'internetuserate','oilperperson','polityscore','relectricperperson', \
                     'suicideper100th','employrate','urbanrate', 'lifeexpectancy']:
   seaborn.regplot(x=x, y="lifeexpectancy", fit_reg=True, data=data_clean)


scat1 = seaborn.regplot(x="urbanrate", y="internetuserate", fit_reg=True, data=data)
plt.xlabel('Urban Rate')
plt.ylabel('Internet Use Rate')
plt.title('Scatterplot for the Association Between Urban Rate and Internet Use Rate')

scat2 = seaborn.regplot(x="incomeperperson", y="internetuserate", fit_reg=True, data=data)
plt.xlabel('Income per Person')
plt.ylabel('Internet Use Rate')
plt.title('Scatterplot for the Association Between Income per Person and Internet Use Rate')

data_clean=data.dropna()

print ('association between urbanrate and internetuserate')
print (scipy.stats.pearsonr(data_clean['urbanrate'], data_clean['internetuserate']))

print ('association between incomeperperson and internetuserate')
print (scipy.stats.pearsonr(data_clean['incomeperperson'], data_clean['internetuserate']))

seaborn.pairplot(data_clean, vars=['incomeperperson',"lifeexpectancy"])

pandas.DataFrame(data=np.array(scipy.stats.pearsonr(data_clean['incomeperperson'], data_clean['internetuserate']))).T #, columns=['r','p'])