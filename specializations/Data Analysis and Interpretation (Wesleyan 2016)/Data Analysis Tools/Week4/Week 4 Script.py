# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 10:18:43 2015

@author: jml
"""

# ANOVA

import numpy
import pandas
import statsmodels.formula.api as smf 
import statsmodels.stats.multicomp as multi
import seaborn
import matplotlib.pyplot as plt


data = pandas.read_csv('C:\\courses\\Coursera\\Current\\Data Analysis Tools\\Week4\\diet_exercise.csv', low_memory=False)

#data["Diet"] = data["Diet"].astype('category')
#data['WeightLoss']= data['WeightLoss'].convert_objects(convert_numeric=True)

#dir(smf)

model1 = smf.ols(formula='WeightLoss ~ C(Diet)', data=data).fit()
print (model1.summary())

sub1 = data[['WeightLoss', 'Diet']].dropna()

print ("means for WeightLoss by Diet A vs. B")
m1= sub1.groupby('Diet').mean()
print (m1)

print ("standard deviation for mean WeightLoss by Diet A vs. B")
st1= sub1.groupby('Diet').std()
print (st1)

# bivariate bar graph
seaborn.factorplot(x="Diet", y="WeightLoss", data=data, kind="bar", ci=None)
plt.xlabel('Diet Type')
plt.ylabel('Mean Weight Loss in pounds')


sub2=data[(data['Exercise']=='Cardio')]
sub3=data[(data['Exercise']=='Weights')]

print ('association between diet and weight loss for those using Cardio exercise')
model2 = smf.ols(formula='WeightLoss ~ C(Diet)', data=sub2).fit()
print (model2.summary())

print ('association between diet and weight loss for those using Weights exercise')
model3 = smf.ols(formula='WeightLoss ~ C(Diet)', data=sub3).fit()
print (model3.summary())

print ("means for WeightLoss by Diet A vs. B  for CARDIO")
m3= sub2.groupby('Diet').mean()
print (m3)
print ("Means for WeightLoss by Diet A vs. B for WEIGHTS")
m4 = sub3.groupby('Diet').mean()
print (m4)

# End of Lesson 2
#%%
# Beginning of Lesson 3

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

#sub1['NUMCIGMO_EST']= sub1['NUMCIGMO_EST'].convert_objects(convert_numeric=True)

ct1= sub1.groupby('NUMCIGMO_EST').size()
print (ct1)

model1 = smf.ols(formula='NUMCIGMO_EST ~ MAJORDEPLIFE', data=sub1).fit()
print (model1.summary())

sub2 = sub1[['NUMCIGMO_EST', 'MAJORDEPLIFE']].dropna()

print ('means for numcigmo_est by major depression status')
m1= sub2.groupby('MAJORDEPLIFE').mean()
print (m1)

print ('standard deviations for numcigmo_est by major depression status')
sd1 = sub2.groupby('MAJORDEPLIFE').std()
print (sd1)

sub3 = sub1[['NUMCIGMO_EST', 'ETHRACE2A']].dropna()

model1 = smf.ols(formula='NUMCIGMO_EST ~ C(ETHRACE2A)', data=sub3).fit()
print (model1.summary())

print ('means for numcigmo_est by major depression status')
m2= sub3.groupby('ETHRACE2A').mean()
print (m2)

print ('standard deviations for numcigmo_est by major depression status')
sd2 = sub3.groupby('ETHRACE2A').std()
print (sd2)

mc2 = multi.MultiComparison(sub3['NUMCIGMO_EST'], sub3['ETHRACE2A'])
res2 = mc2.tukeyhsd()
print(res2.summary())

# CHISQ


import pandas
import numpy
import scipy.stats
import seaborn
import matplotlib.pyplot as plt
import statsmodels.stats.proportion as sm

data = pandas.read_csv('C:\\courses\\Coursera\\Current\\Data Analysis Tools\\Week4\\nesarc_pds.csv', low_memory=False)

#setting variables you will be working with to numeric
data['TAB12MDX'] = data['TAB12MDX'].convert_objects(convert_numeric=True)
data['CHECK321'] = data['CHECK321'].convert_objects(convert_numeric=True)
data['S3AQ3B1'] = data['S3AQ3B1'].convert_objects(convert_numeric=True)
data['S3AQ3C1'] = data['S3AQ3C1'].convert_objects(convert_numeric=True)
data['AGE'] = data['AGE'].convert_objects(convert_numeric=True)

#subset data to young adults age 18 to 25 who have smoked in the past 12 months
sub1=data[(data['AGE']>=18) & (data['AGE']<=25) & (data['CHECK321']==1)]

#make a copy of my new subsetted data
sub2 = sub1.copy()

# recode missing values to python missing (NaN)
sub2['S3AQ3B1']=sub2['S3AQ3B1'].replace(9, numpy.nan)
sub2['S3AQ3C1']=sub2['S3AQ3C1'].replace(99, numpy.nan)


#START RUNNING CODE HERE

#recoding values for S3AQ3B1 into a new variable, USFREQMO
recode1 = {1: 30, 2: 22, 3: 14, 4: 6, 5: 2.5, 6: 1}
sub2['USFREQMO']= sub2['S3AQ3B1'].map(recode1)

#recoding values for S3AQ3B1 into a new variable, USFREQMO
recode2 = {1: 30, 2: 22, 3: 14, 4: 5, 5: 2.5, 6: 1}
sub2['USFREQMO']= sub2['S3AQ3B1'].map(recode2)


def USQUAN (row):
   if row['S3AQ3B1'] != 1:
      return 0
   elif row['S3AQ3C1'] <= 5 :
      return 3
   elif row['S3AQ3C1'] <=10:
      return 8
   elif row['S3AQ3C1'] <= 15:
      return 13
   elif row['S3AQ3C1'] <= 20:
      return 18
   elif row['S3AQ3C1'] > 20:
      return 37
sub2['USQUAN'] = sub2.apply (lambda row: USQUAN (row),axis=1)

c5 = sub2['USQUAN'].value_counts(sort=False, dropna=True)
print(c5)

c6 = sub2['S3AQ3C1'].value_counts(sort=False, dropna=True)
print(c6)

# contingency table of observed counts
ct1=pandas.crosstab(sub2['TAB12MDX'], sub2['USQUAN'])
print (ct1)

# column percentages
colsum=ct1.sum(axis=0)
colpct=ct1/colsum
print(colpct)

# chi-square
print ('chi-square value, p value, expected counts')
cs1= scipy.stats.chi2_contingency(ct1)
print (cs1)

# set variable types 
sub2["USQUAN"] = sub2["USQUAN"].astype('category')
sub2['TAB12MDX'] = sub2['TAB12MDX'].convert_objects(convert_numeric=True)

# bivariate bar graph
seaborn.factorplot(x="USQUAN", y="TAB12MDX", data=sub2, kind="bar", ci=None)
plt.xlabel('number of cigarettes smoked per day')
plt.ylabel('Proportion Nicotine Dependent')

sub3=sub2[(sub2['MAJORDEPLIFE']== 0)]
sub4=sub2[(sub2['MAJORDEPLIFE']== 1)]

print ('association between smoking quantity and nicotine dependence for those W/O deperession')
# contingency table of observed counts
ct2=pandas.crosstab(sub3['TAB12MDX'], sub3['USQUAN'])
print (ct2)

# column percentages
colsum=ct1.sum(axis=0)
colpct=ct1/colsum
print(colpct)

# chi-square
print ('chi-square value, p value, expected counts')
cs2= scipy.stats.chi2_contingency(ct2)
print (cs2)

print ('association between smoking quantity and nicotine dependence for those WITH depression')
# contingency table of observed counts
ct3=pandas.crosstab(sub4['TAB12MDX'], sub4['USQUAN'])
print (ct3)

# column percentages
colsum=ct1.sum(axis=0)
colpct=ct1/colsum
print(colpct)

# chi-square
print ('chi-square value, p value, expected counts')
cs3= scipy.stats.chi2_contingency(ct3)
print (cs3)


seaborn.factorplot(x="USQUAN", y="TAB12MDX", data=sub4, kind="point", ci=None)
plt.xlabel('number of cigarettes smoked per day')
plt.ylabel('Proportion Nicotine Dependent')
plt.title('association between smoking quantity and nicotine dependence for those WITH depression')

seaborn.factorplot(x="USQUAN", y="TAB12MDX", data=sub3, kind="point", ci=None)
plt.xlabel('number of cigarettes smoked per day')
plt.ylabel('Proportion Nicotine Dependent')
plt.title('association between smoking quantity and nicotine dependence for those WITHOUT depression')

# End of Lesson 3

#%%

# Beginning of Lesson 4

# CORRELATION
import pandas
import numpy
import scipy.stats
import seaborn
import matplotlib.pyplot as plt

data = pandas.read_csv('gapminder.csv', low_memory=False)

data['urbanrate'] = data['urbanrate'].convert_objects(convert_numeric=True)
data['incomeperperson'] = data['incomeperperson'].convert_objects(convert_numeric=True)
data['internetuserate'] = data['internetuserate'].convert_objects(convert_numeric=True)
data['incomeperperson']=data['incomeperperson'].replace(' ', numpy.nan)

data_clean=data.dropna()

print (scipy.stats.pearsonr(data_clean['urbanrate'], data_clean['internetuserate']))

def incomegrp (row):
   if row['incomeperperson'] <= 744.239:
      return 1
   elif row['incomeperperson'] <= 9425.326 :
      return 2
   elif row['incomeperperson'] > 9425.326:
      return 3
   
data_clean['incomegrp'] = data_clean.apply (lambda row: incomegrp (row),axis=1)

chk1 = data_clean['incomegrp'].value_counts(sort=False, dropna=False)
print(chk1)

sub1=data_clean[(data_clean['incomegrp']== 1)]
sub2=data_clean[(data_clean['incomegrp']== 2)]
sub3=data_clean[(data_clean['incomegrp']== 3)]

print ('association between urbanrate and internetuserate for LOW income countries')
print (scipy.stats.pearsonr(sub1['urbanrate'], sub1['internetuserate']))
print ('       ')
print ('association between urbanrate and internetuserate for MIDDLE income countries')
print (scipy.stats.pearsonr(sub2['urbanrate'], sub2['internetuserate']))
print ('       ')
print ('association between urbanrate and internetuserate for HIGH income countries')
print (scipy.stats.pearsonr(sub3['urbanrate'], sub3['internetuserate']))
#%%
scat1 = seaborn.regplot(x="urbanrate", y="internetuserate", data=sub1)
plt.xlabel('Urban Rate')
plt.ylabel('Internet Use Rate')
plt.title('Scatterplot for the Association Between Urban Rate and Internet Use Rate for LOW income countries')
print (scat1)
#%%
scat2 = seaborn.regplot(x="urbanrate", y="internetuserate", fit_reg=False, data=sub2)
plt.xlabel('Urban Rate')
plt.ylabel('Internet Use Rate')
plt.title('Scatterplot for the Association Between Urban Rate and Internet Use Rate for MIDDLE income countries')
print (scat2)
#%%
scat3 = seaborn.regplot(x="urbanrate", y="internetuserate", data=sub3)
plt.xlabel('Urban Rate')
plt.ylabel('Internet Use Rate')
plt.title('Scatterplot for the Association Between Urban Rate and Internet Use Rate for HIGH income countries')
print (scat3)
