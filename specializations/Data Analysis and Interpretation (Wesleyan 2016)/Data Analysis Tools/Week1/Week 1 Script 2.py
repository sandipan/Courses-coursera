# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 22:53:18 2016

@author: Sandipan.Dey
"""

#import numpy
import pandas
import statsmodels.formula.api as smf
import statsmodels.stats.multicomp as multi 
import pandas as pd
import matplotlib.pylab as plt
#from pandas.tools.plotting import scatter_matrix, andrews_curves, radviz
#import seaborn as sns

data = pandas.read_csv('C:\\courses\\Coursera\\Current\\Data Analysis Tools\\Week1\\gapminder.csv', low_memory=False)
data.drop('country', 1)
data = data.convert_objects(convert_numeric=True) #.dtypes

#df1 = pd.DataFrame(data, columns=['lifeexpectancy','breastcancerper100th','incomeperperson', 'internetuserate', 'co2emissions'])
df1 = pd.DataFrame(data, columns=['lifeexpectancy','incomeperperson'])
df1 = df1.dropna()
df1.describe()

plt.figure()
df1.hist(alpha=0.5, bins=10, xrot=90)

df1['incomeperperson'] = pd.cut(df1.incomeperperson, bins=[0,2385,52302])
df1.head()

ct1 = df1.groupby('incomeperperson').size()
print (ct1)

# using ols function for calculating the F-statistic and associated p value
model1 = smf.ols(formula='lifeexpectancy ~ C(incomeperperson)', data=df1)
results1 = model1.fit()
print (results1.summary())

print ('means for lifeexpectancy by incomeperperson categories')
m1= df1.groupby('incomeperperson').mean()
print (m1)
df1.boxplot(['lifeexpectancy'], by='incomeperperson')

print ('standard deviations for lifeexpectancy by incomeperperson categories')
sd1 = df1.groupby('incomeperperson').std()
print (sd1)

df2 = pd.DataFrame(data, columns=['lifeexpectancy','alcconsumption'])
df2 = df2.dropna()
df2.describe()
plt.figure()
df2.hist(alpha=0.5, bins=10, xrot=90)

df2['alcconsumption'] = pd.cut(df2.alcconsumption, bins=[0,3,6,10,25])
df2.head()

model2 = smf.ols(formula='lifeexpectancy ~ C(alcconsumption)', data=df2).fit()
print (model2.summary())

print ('means for lifeexpectancy by alcconsumption')
g2 = df2.groupby('alcconsumption')
print (g2.mean())
df2.boxplot(['lifeexpectancy'], by='alcconsumption')

print ('standard deviations for for lifeexpectancy by alcconsumption')
print (g2.sd())

mc1 = multi.MultiComparison(df2['lifeexpectancy'], df2['alcconsumption'])
res1 = mc1.tukeyhsd()
print(res1.summary())


























