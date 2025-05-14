# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 10:13:11 2015

@author: jml
"""

import numpy
import pandas
import statsmodels.formula.api as smf
import statsmodels.stats.multicomp as multi 

data = pandas.read_csv('C:\\courses\\Coursera\\Current\\Data Analysis Tools\\Week1\\nesarc_pds.csv', low_memory=False)

#setting variables you will be working with to numeric
data['S3AQ3B1'] = data['S3AQ3B1'].convert_objects(convert_numeric=True)
data['S3AQ3C1'] = data['S3AQ3C1'].convert_objects(convert_numeric=True)
data['CHECK321'] = data['CHECK321'].convert_objects(convert_numeric=True)

#subset data to young adults age 18 to 25 who have smoked in the past 12 months
sub1=data[(data['AGE']>=18) & (data['AGE']<=25) & (data['CHECK321']==1)]

#SETTING MISSING DATA
sub1['S3AQ3B1']=sub1['S3AQ3B1'].replace(9, numpy.nan)
sub1['S3AQ3C1']=sub1['S3AQ3C1'].replace(99, numpy.nan)

#recoding number of days smoked in the past month
recode1 = {1: 30, 2: 22, 3: 14, 4: 5, 5: 2.5, 6: 1}
sub1['USFREQMO']= sub1['S3AQ3B1'].map(recode1)

#converting new variable USFREQMMO to numeric
sub1['USFREQMO']= sub1['USFREQMO'].convert_objects(convert_numeric=True)

# Creating a secondary variable multiplying the days smoked/month and the number of cig/per day
sub1['NUMCIGMO_EST']=sub1['USFREQMO'] * sub1['S3AQ3C1']

sub1['NUMCIGMO_EST']= sub1['NUMCIGMO_EST'].convert_objects(convert_numeric=True)

ct1 = sub1.groupby('NUMCIGMO_EST').size()
print (ct1)

# using ols function for calculating the F-statistic and associated p value
model1 = smf.ols(formula='NUMCIGMO_EST ~ C(MAJORDEPLIFE)', data=sub1)
results1 = model1.fit()
print (results1.summary())

sub2 = sub1[['NUMCIGMO_EST', 'MAJORDEPLIFE']].dropna()

print ('means for numcigmo_est by major depression status')
m1= sub2.groupby('MAJORDEPLIFE').mean()
print (m1)

print ('standard deviations for numcigmo_est by major depression status')
sd1 = sub2.groupby('MAJORDEPLIFE').std()
print (sd1)
#i will call it sub3
sub3 = sub1[['NUMCIGMO_EST', 'ETHRACE2A']].dropna()

model2 = smf.ols(formula='NUMCIGMO_EST ~ C(ETHRACE2A)', data=sub3).fit()
print (model2.summary())

print ('means for numcigmo_est by major depression status')
m2= sub3.groupby('ETHRACE2A').mean()
print (m2)

print ('standard deviations for numcigmo_est by major depression status')
sd2 = sub3.groupby('ETHRACE2A').std()
print (sd2)

mc1 = multi.MultiComparison(sub3['NUMCIGMO_EST'], sub3['ETHRACE2A'])
res1 = mc1.tukeyhsd()
print(res1.summary())


























