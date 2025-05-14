# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 12:40:13 2015

@author: ldierker
"""

import pandas
import numpy
# any additional libraries would be imported here

data = pandas.read_csv('C:\\courses\\Coursera\\Current\\Data Visualization\\Week2\\nesarc_pds.csv', low_memory=False)

# bug fix for display formats to avoid run time errors
pandas.set_option('display.float_format', lambda x:'%f'%x)

#setting variables you will be working with to numeric
data['TAB12MDX'] = data['TAB12MDX'].convert_objects(convert_numeric=True)
data['CHECK321'] = data['CHECK321'].convert_objects(convert_numeric=True)
data['S3AQ3B1'] = data['S3AQ3B1'].convert_objects(convert_numeric=True)
data['S3AQ3C1'] = data['S3AQ3C1'].convert_objects(convert_numeric=True)
data['S2AQ8A'] = data['S2AQ8A'].convert_objects(convert_numeric=True)
data['AGE'] = data['AGE'].convert_objects(convert_numeric=True)

#subset data to young adults age 18 to 25 who have smoked in the past 12 months
sub1=data[(data['AGE']>=18) & (data['AGE']<=25) & (data['CHECK321']==1)]

#make a copy of my new subsetted data
sub2 = sub1.copy()

print 'counts for original S3AQ3B1'
c1 = sub2['S3AQ3B1'].value_counts(sort=False, dropna=False)
print(c1)

# recode missing values to python missing (NaN)
sub2['S3AQ3B1']=sub2['S3AQ3B1'].replace(9, numpy.nan)
sub2['S3AQ3C1']=sub2['S3AQ3C1'].replace(99, numpy.nan)

#if you want to include a count of missing add ,dropna=False after sort=False 
print 'counts for S3AQ3B1 with 9 set to NAN and number of missing requested'
c2 = sub2['S3AQ3B1'].value_counts(sort=False, dropna=False)
print(c2)

#coding in valid data
#recode missing values to numeric value, in this example replace NaN with 11
sub2['S2AQ8A'].fillna(11, inplace=True)
#recode 99 values as missing
sub2['S2AQ8A']=sub2['S2AQ8A'].replace(99, numpy.nan)

print 'S2AQ8A with Blanks recoded as 11 and 99 set to NAN'
# check coding
chk2 = sub2['S2AQ8A'].value_counts(sort=False, dropna=False)
print(chk2)
ds2= sub2["S2AQ8A"].describe()
print(ds2)

#recoding values for S3AQ3B1 into a new variable, USFREQ
recode1 = {1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1}
sub2['USFREQ']= sub2['S3AQ3B1'].map(recode1)

#recoding values for S3AQ3B1 into a new variable, USFREQMO
recode2 = {1: 30, 2: 22, 3: 14, 4: 5, 5: 2.5, 6: 1}
sub2['USFREQMO']= sub2['S3AQ3B1'].map(recode2)

#secondary variable multiplying the number of days smoked/month and the approx number of cig smoked/day
sub2['NUMCIGMO_EST']=sub2['USFREQMO'] * sub2['S3AQ3C1']

#examining frequency distributions for age
print 'counts for AGE'
c3 = sub2['AGE'].value_counts(sort=False)
print(c3)

print 'percentages for AGE'
p3 = sub2['AGE'].value_counts(sort=False, normalize=True)
print (p3)

# quartile split (use qcut function & ask for 4 groups - gives you quartile split)
print 'AGE - 4 categories - quartiles'
sub2['AGEGROUP4']=pandas.qcut(sub2.AGE, 4, labels=["1=0%tile","2=25%tile","3=50%tile","4=75%tile"])
c4 = sub2['AGEGROUP4'].value_counts(sort=False, dropna=True)
print(c4)

# categorize quantitative variable based on customized splits using cut function
# splits into 3 groups (18-20, 21-22, 23-25) - remember that Python starts counting from 0, not 1
sub2['AGEGROUP3'] = pandas.cut(sub2.AGE, [17, 20, 22, 25])
c5 = sub2['AGEGROUP3'].value_counts(sort=False, dropna=True)
print(c5)

#crosstabs evaluating which ages were put into which AGEGROUP3
print (pandas.crosstab(sub2['AGEGROUP3'], sub2['AGE']))

#frequency distribution for AGEGROUP3
print 'counts for AGEGROUP3'
c10 = sub2['AGEGROUP3'].value_counts(sort=False)
print(c10)

print 'percentages for AGEGROUP3'
p10 = sub2['AGEGROUP3'].value_counts(sort=False, normalize=True)
print (p10)

#ADDHEALTH EXAMPLE

import pandas
import numpy

data = pandas.read_csv('addhealth_pds.csv', low_memory=False)

#making individual ethnicity variables numeric
data['H1GI4'] = data['H1GI4'].convert_objects(convert_numeric=True)
data['H1GI6A'] = data['H1GI6A'].convert_objects(convert_numeric=True)
data['H1GI6B'] = data['H1GI6B'].convert_objects(convert_numeric=True)
data['H1GI6C'] = data['H1GI6C'].convert_objects(convert_numeric=True)
data['H1GI6D'] = data['H1GI6D'].convert_objects(convert_numeric=True)

#Set missing data to NAN
data['H1GI4']=data['H1GI4'].replace(6, numpy.nan)
data['H1GI4']=data['H1GI4'].replace(8, numpy.nan)
data['H1GI6A']=data['H1GI6A'].replace(6, numpy.nan)
data['H1GI6A']=data['H1GI6A'].replace(8, numpy.nan)
data['H1GI6B']=data['H1GI6B'].replace(6, numpy.nan)
data['H1GI6B']=data['H1GI6B'].replace(8, numpy.nan)
data['H1GI6C']=data['H1GI6C'].replace(6, numpy.nan)
data['H1GI6C']=data['H1GI6C'].replace(8, numpy.nan)
data['H1GI6D']=data['H1GI6D'].replace(6, numpy.nan)
data['H1GI6D']=data['H1GI6D'].replace(8, numpy.nan)

#count of number of ethnicity categories endorsed, NUMETHNIC
data['NUMETHNIC']=data['H1GI4'] + data['H1GI6A'] + data['H1GI6B'] + data['H1GI6C'] + data['H1GI6D'] 
print('NUMETHNIC')

# subset variables in new data frame, sub1
sub1=data[['AID','H1GI4', 'H1GI6A', 'H1GI6B', 'H1GI6C', 'H1GI6D', 'NUMETHNIC']]

a = sub1.head (n=10)
print(a)

#new ETHNICITY variable, categorical 1 through 6
def ETHNICITY (row):
   if row['NUMETHNIC'] > 1 :
      return 1
   if row['H1GI4'] == 1 :
      return 2
   if row['H1GI6A'] == 1:
      return 3
   if row['H1GI6B'] == 1:
      return 4
   if row['H1GI6C'] == 1:
      return 5
   if row['H1GI6D'] == 1:
      return 6
sub1['ETHNICITY'] = sub1.apply (lambda row: ETHNICITY (row),axis=1)

a = sub1.head (n=10)
print(a)

#frequency distributions for primary and secondary ethinciity variables
print 'counts for Hispanic/Latino'
c10 = sub1['H1GI4'].value_counts(sort=False)
print(c10)

print 'percentages for Hispanic/Latino'
p10 = sub1['H1GI4'].value_counts(sort=False, normalize=True)
print (p10)

print 'counts for Black/African American'
c11 = sub1['H1GI6A'].value_counts(sort=False)
print(c11)

print 'percentages for Black/African American'
p11= sub1['H1GI6A'].value_counts(sort=False, normalize=True)
print (p11)

print 'counts for American Indian/Native American'
c12 = sub1['H1GI6B'].value_counts(sort=False)
print(c12)

print 'percentages for American Indian/Native American'
p12 = sub1['H1GI6B'].value_counts(sort=False, normalize=True)
print (p12)

print 'counts for Asian/Pacific Islander'
c13 = sub1['H1GI6C'].value_counts(sort=False)
print(c13)

print 'percentages for Asian/Pacific Islander'
p13 = sub1['H1GI6C'].value_counts(sort=False, normalize=True)
print (p13)

print 'counts for White'
c14 = sub1['H1GI6D'].value_counts(sort=False)
print(c14)

print 'percentages for White'
p14 = sub1['H1GI6D'].value_counts(sort=False, normalize=True)
print (p14)

print 'counts for number of races/ethnicities endorsed'
c15 = sub1['NUMETHNIC'].value_counts(sort=False)
print(c15)

print 'counts for each Ethnic group'
c16 = sub1['ETHNICITY'].value_counts(sort=False)
print(c16)

print 'percentages for each Ethnic Group'
p16 = sub1['ETHNICITY'].value_counts(sort=False, normalize=True)
print (p16)


