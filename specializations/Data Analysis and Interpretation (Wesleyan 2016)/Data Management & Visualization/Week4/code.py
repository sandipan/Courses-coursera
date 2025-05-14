# -*- coding: utf-8 -*-
"""
Created on Mon May 09 23:12:07 2016
@author: Sandipan.Dey
"""

import pandas
import numpy
import seaborn
import matplotlib.pyplot as plt

data = pandas.read_csv('C:\\courses\\Coursera\\Current\\Data Visualization\\Week4\\literacy.csv')

#setting variables you will be working with to numeric
data['Total.Persons'] = data['Total.Persons'].convert_objects(convert_numeric=True)
data['Total.Males'] = data['Totl.Males'].convert_objects(convert_numeric=True)
data['Total.Females'] = data['Total.Females'].convert_objects(convert_numeric=True)
data['Rural.Persons'] = data['Rural.Persons'].convert_objects(convert_numeric=True)
data['Rural.Males'] = data['Rural.Males'].convert_objects(convert_numeric=True)
data['Rural.Females'] = data['Rural.Females'].convert_objects(convert_numeric=True)
data['Urban.Persons'] = data['Urban.Persons'].convert_objects(convert_numeric=True)
data['Urban.Males'] = data['Urban.Males'].convert_objects(convert_numeric=True)
data['Urban.Females'] = data['Urban.Females'].convert_objects(convert_numeric=True)

literate = data[data.Status == 'Literate']
illiterate = data[data.Status == 'Illiterate']

# univariate graphs
seaborn.distplot(literate['Total.Persons'], kde=False)
plt.xlabel('Total Literate Persons')
plt.ylabel('Count of Ages')
plt.title('Distribution of Total Literate Persons in India in 2011')

seaborn.distplot(illiterate['Total.Persons'], kde=False)
plt.xlabel('Total Illiterate Persons')
plt.ylabel('Count of Ages')
plt.title('Distribution of Total Illiterate Persons in India in 2011')

g = seaborn.FacetGrid(data, col="Status")
g = g.map(plt.hist, "Total.Persons")
g.set_xticklabels(rotation=90)

g = seaborn.FacetGrid(data, col="Status")
g = g.map(plt.hist, "Total.Males")
g.set_xticklabels(rotation=90)

g = seaborn.FacetGrid(data, col="Status")
g = g.map(plt.hist, "Total.Females")
g.set_xticklabels(rotation=90)

g = seaborn.FacetGrid(data, col="Status")
g = g.map(plt.hist, "Rural.Persons")
g.set_xticklabels(rotation=90)

g = seaborn.FacetGrid(data, col="Status")
g = g.map(plt.hist, "Rural.Males")
g.set_xticklabels(rotation=90)

g = seaborn.FacetGrid(data, col="Status")
g = g.map(plt.hist, "Rural.Females")
g.set_xticklabels(rotation=90)

g = seaborn.FacetGrid(data, col="Status")
g = g.map(plt.hist, "Urban.Persons")
g.set_xticklabels(rotation=90)

g = seaborn.FacetGrid(data, col="Status")
g = g.map(plt.hist, "Urban.Males")
g.set_xticklabels(rotation=90)

g = seaborn.FacetGrid(data, col="Status")
g = g.map(plt.hist, "Urban.Females")
g.set_xticklabels(rotation=90)

print literate['Total.Persons'].describe()
print literate['Total.Males'].describe()
print literate['Total.Females'].describe()

data['Percent.Total.Males'] =  data['Total.Males'] / data['Total.Persons']
data['Percent.Rural.Males'] =  data['Rural.Males'] / data['Rural.Persons']
data['Percent.Urban.Males'] =  data['Urban.Males'] / data['Urban.Persons']

# bivariate graphs

#basic scatterplot:  Q->Q
seaborn.lmplot(x="Age", y="Total.Persons", hue='Status', col='Status', fit_reg=True, lowess=True, data=data)
seaborn.lmplot(x="Age", y="Percent.Total.Males", hue='Status', col='Status', fit_reg=True, lowess=True, data=data)
seaborn.lmplot(x="Age", y="Percent.Rural.Males", hue='Status', col='Status', fit_reg=True, lowess=True, data=data)
seaborn.lmplot(x="Age", y="Percent.Urban.Males", hue='Status', col='Status', fit_reg=True, lowess=True, data=data)

#split the age into 4 groups
data1 = data.copy()
data1['AgeGRP4']=pandas.cut(data1.Age, [0, 25, 50, 75, 100])
data1.groupby(['AgeGRP4', 'Status']).sum()

g = seaborn.lmplot(x="Total.Males", y="Total.Females", hue='Status', col='AgeGRP4', fit_reg=True, data=data1, palette='Set1')
g.set_xticklabels(rotation=90)

seaborn.lmplot(x="Age", y="Rural.Persons", hue='Status', fit_reg=False, data=data)
plt.title('Scatterplot for the Association Between Age and literate / illeterate Rural Persons')
seaborn.lmplot(x="Age", y="Urban.Persons", hue='Status', fit_reg=False, data=data)
plt.title('Scatterplot for the Association Between Age and literate / illeterate Urban Persons')

# bivariate bar graph C->Q
seaborn.factorplot(x='AgeGRP4', y='Total.Persons', hue='Status', data=data1, kind="bar", ci=None)
plt.xlabel('Age group')
plt.ylabel('Total Persons')

seaborn.factorplot(x='AgeGRP4', y='Urban.Persons', hue='Status', data=data1, kind="bar", ci=None)
plt.xlabel('Age group')
plt.ylabel('Urban Persons')

seaborn.factorplot(x='AgeGRP4', y='Rural.Persons', hue='Status', data=data1, kind="bar", ci=None)
plt.xlabel('Age group')
plt.ylabel('Rural Persons')

print data1.sort(['AgeGRP4'], ascending=[1])

