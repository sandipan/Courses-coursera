# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 10:50:43 2015

@author: ldierker
"""
import pandas
import numpy
# any additional libraries would be imported here

data = pandas.read_csv('C:\\courses\\Coursera\\Current\\Data Visualization\\Week2\\nesarc_pds.csv', low_memory=False)

print (len(data)) #number of observations (rows)
print (len(data.columns)) # number of variables (columns)

#setting variables you will be working with to numeric
data['TAB12MDX'] = data['TAB12MDX'].convert_objects(convert_numeric=True)
data['CHECK321'] = data['CHECK321'].convert_objects(convert_numeric=True)
data['S3AQ3B1'] = data['S3AQ3B1'].convert_objects(convert_numeric=True)
data['S3AQ3C1'] = data['S3AQ3C1'].convert_objects(convert_numeric=True)
data['AGE'] = data['AGE'].convert_objects(convert_numeric=True)

#counts and percentages (i.e. frequency distributions) for each variable
c1 = data['TAB12MDX'].value_counts(sort=False)
print (c1)

p1 = data['TAB12MDX'].value_counts(sort=False, normalize=True)
print (p1)

c2 = data['CHECK321'].value_counts(sort=False)
print(c2)

p2 = data['CHECK321'].value_counts(sort=False, normalize=True)
print (p2)

c3 = data['S3AQ3B1'].value_counts(sort=False)
print(c3)

p3 = data['S3AQ3B1'].value_counts(sort=False, normalize=True)
print (p3)

c4 = data['S3AQ3C1'].value_counts(sort=False)
print(c4)

p4 = data['S3AQ3C1'].value_counts(sort=False, normalize=True)
print (p4)

c4 = data['S3AQ3C1'].value_counts(sort=False)
print(c4)

p4 = data['S3AQ3C1'].value_counts(sort=False, normalize=True)
print (p4)

#ADDING TITLES
print 'counts for TAB12MDX'
c1 = data['TAB12MDX'].value_counts(sort=False)
print (c1)
#print (len(data['TAB12MDX'])) #number of observations (rows)

print 'percentages for TAB12MDX'
p1 = data['TAB12MDX'].value_counts(sort=False, normalize=True)
print (p1)

print 'counts for CHECK321'
c2 = data['CHECK321'].value_counts(sort=False)
print(c2)

print 'percentages for CHECK321'
p2 = data['CHECK321'].value_counts(sort=False, normalize=True)
print (p2)

print 'counts for S3AQ3B1'
c3 = data['S3AQ3B1'].value_counts(sort=False, dropna=False)
print(c3)
#print (len(data['S3AQ3B1'])) #number of observations (rows)

print 'percentages for S3AQ3B1'
p3 = data['S3AQ3B1'].value_counts(sort=False, normalize=True)
print (p3)

print 'counts for S3AQ3C1'
c4 = data['S3AQ3C1'].value_counts(sort=False, dropna=False)
print(c4)

print 'percentages for S3AQ3C1'
p4 = data['S3AQ3C1'].value_counts(sort=False, dropna=False, normalize=True)
print (p4)

#ADDING MORE DESCRIPTIVE TITLES
print 'counts for TAB12MDX – nicotine dependence in the past 12 months, yes=1'
c1 = data['TAB12MDX'].value_counts(sort=False)
print (c1)

print 'percentages for TAB12MDX nicotine dependence in the past 12 months, yes=1'
p1 = data['TAB12MDX'].value_counts(sort=False, normalize=True)
print (p1)

print 'counts for CHECK321 smoked in the past year, yes=1'
c2 = data['CHECK321'].value_counts(sort=False)
print(c2)

print 'percentages for CHECK321 smoked in the past year, yes=1'
p2 = data['CHECK321'].value_counts(sort=False, normalize=True)
print (p2)

print 'counts for S3AQ3B1 –usual frequency when smoked cigarettes'
c3 = data['S3AQ3B1'].value_counts(sort=False)
print(c3)

print 'percentages for S3AQ3B1 - usual frequency when smoked cigarettes'
p3 = data['S3AQ3B1'].value_counts(sort=False, normalize=True)
print (p3)

print 'counts for S3AQ3C1 usual quantity when smoked cigarettes'
c4 = data['S3AQ3C1'].value_counts(sort=False)
print(c4)

print 'percentages for S3AQ3C1 usual quantity when smoked cigarettes'
p4 = data['S3AQ3C1'].value_counts(sort=False, normalize=True)
print (p4)

# freqeuncy disributions using the 'bygroup' function
ct1= data.groupby('TAB12MDX').size()
print ct1

pt1 = data.groupby('TAB12MDX').size() * 100 / len(data)
print pt1

ct2= data.groupby('CHECK321').size()
print ct2

pt2 = data.groupby('CHECK321').size() * 100 / len(data)
print pt2

ct3= data.groupby('S3AQ3B1').size()
print ct3

pt3 = data.groupby('S3AQ3B1').size() * 100 / len(data)
print pt3

ct4= data.groupby('S3AQ3C1').size()
print ct4

pt4 = data.groupby('S3AQ3C1').size() * 100 / len(data)
print pt4

#subset data to young adults age 18 to 25 who have smoked in the past 12 months
sub1=data[(data['AGE']>=18) & (data['AGE']<=25) & (data['CHECK321']==1)]

#make a copy of my new subsetted data
sub2 = sub1.copy()

# frequency distritions on new sub2 data frame
print 'counts for AGE'
c5 = sub2['AGE'].value_counts(sort=False)
print(c5)

print 'percentages for AGE'
p5 = sub2['AGE'].value_counts(sort=False, normalize=True)
print (p5)

print 'counts for CHECK321'
c6 = sub2['CHECK321'].value_counts(sort=False)
print(c6)

print 'percentages for CHECK321'
p6 = sub2['CHECK321'].value_counts(sort=False, normalize=True)
print (p6)

#upper-case all DataFrame column names - place afer code for loading data aboave
data.columns = map(str.upper, data.columns)

# bug fix for display formats to avoid run time errors - put after code for loading data above
pandas.set_option('display.float_format', lambda x:'%f'%x)


