# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 14:59:43 2015

@author: jml
"""

import pandas
import numpy
import seaborn
import scipy
import matplotlib.pyplot as plt

data = pandas.read_csv('C:\\courses\\Coursera\\Current\\Data Analysis Tools\\Week3\\gapminder.csv', low_memory=False)

#setting variables you will be working with to numeric
data['internetuserate'] = data['internetuserate'].convert_objects(convert_numeric=True)
data['urbanrate'] = data['urbanrate'].convert_objects(convert_numeric=True)
data['incomeperperson'] = data['incomeperperson'].convert_objects(convert_numeric=True)

data['incomeperperson']=data['incomeperperson'].replace(' ', numpy.nan)

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
