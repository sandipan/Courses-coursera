# -*- coding: utf-8 -*-
"""
Created on Thu May 05 23:41:42 2016
@author: Sandipan Dey
"""

import pandas
import numpy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns

data = pandas.read_csv('C:\\courses\\Coursera\\Current\\Data Visualization\\Week3\\gapminder.csv')

# 3 variables seelcted to manage: lifeexpectancy, employrate, internetuserate
data['lifeexpectancy'] = data['lifeexpectancy'].convert_objects(convert_numeric=True)
data['employrate'] = data['employrate'].convert_objects(convert_numeric=True)
data['internetuserate'] = data['internetuserate'].convert_objects(convert_numeric=True)

#subset data to the countries with less than equal to life expectancy of 70
sub1 = data[(data['lifeexpectancy']<=70)]
sub2 = sub1.copy() #make a copy of my new subsetted data
sub2.describe()

# categorize quantitative variable based on customized splits using cut function
# splits employrate into 4 groups approximately along the quartiles of the variable employrate (as found from the summary)
sub2['employrate_group4']=pandas.cut(sub2.employrate, [0, 56.3, 63.8, 70.5, 100])
#counts and percentages (i.e. frequency distributions) for employrate
print sub2['employrate_group4'].value_counts(sort=False, dropna=False)
print sub2['employrate_group4'].value_counts(sort=False, normalize=True, dropna=False) #percentages for employrate_group4
# splits internetuserate into 3 groups (0-10, 10-20, 20-30)
sub2['internetuserate_group3'] = pandas.cut(sub2.internetuserate, [0, 10, 20, 30])
print sub2['internetuserate_group3'].value_counts(sort=False, dropna=False)
print sub2['internetuserate_group3'].value_counts(sort=False, normalize=True, dropna=False) #percentages for internetuserate_group3
# splits lifeexpectancy into 4 groups with quartile split
sub2['lifeexpectancy_group4'] = pandas.qcut(sub2.lifeexpectancy, 4, labels=["1=0%tile","2=25%tile","3=50%tile","4=75%tile"])
print sub2['lifeexpectancy_group4'].value_counts(sort=False)
print sub2['lifeexpectancy_group4'].value_counts(sort=False, normalize=True)

#crosstabs evaluating which ages were put into which internetuserate_group3
df = pandas.crosstab(sub2['internetuserate_group3'], sub2['employrate_group4'])
print df
sns.heatmap(df)
sns.boxplot(sub2.employrate_group4, sub2.lifeexpectancy)
sns.violinplot(sub2.internetuserate_group3, sub2.lifeexpectancy)
g = sns.FacetGrid(sub2, row="internetuserate_group3")
g = g.map(plt.hist, "lifeexpectancy")

sub2['>60'] = sub2.lifeexpectancy > 60
kws = dict(s=50, linewidth=.5, edgecolor="w")
g = sns.FacetGrid(sub2, col=">60",  hue=">60", palette="Set1", hue_order=[False, True])
g = (g.map(plt.scatter, "employrate", "internetuserate", **kws).add_legend())
#g = sns.FacetGrid(sub2, col="employrate_group4", hue="internetuserate_group3", hue_order=['(0, 10]', '(10, 20]', '(20, 30]'], size=4, aspect=.8)
g = sns.FacetGrid(sub2, col="employrate_group4", size=4, aspect=.8)
g = g.map(sns.boxplot, "internetuserate_group3", "lifeexpectancy")
#from ggplot import *
#p = ggplot(aes(x='date', y='value'), data=meat_lng)
#p + geom_hist() + facet_wrap("color")

# plot variables
fig, ax = plt.subplots(1, 2, figsize=(16,4))
sub2['employrate'].plot(kind='hist', ax=ax[0])
sub2['internetuserate'].plot(kind='hist', ax=ax[0]) 
sub2['lifeexpectancy'].plot(kind='hist', ax=ax[0]) 
ax[0].set_xlim(0,100) 
ax[0].set_title('Histograms of the Variables') 
ax[0].legend(loc='best')
#sub2['col'] = map(lambda(x): 'r' if x else 'b', sub2.lifeexpectancy > 60)
#ax[1].scatter(sub2.employrate, sub2.internetuserate, c=sub2.col, s=sub2.lifeexpectancy)
sub3 = sub2[(sub2.lifeexpectancy > 60)]
ax[1].set_ylim(0,50) 
ax[1].scatter(sub3.employrate, sub3.internetuserate, c='b', marker='o', s=50, label='lifeexpectancy > 60')
sub3 = sub2[(sub2.lifeexpectancy <= 60)]
ax[1].scatter(sub3.employrate, sub3.internetuserate, c='r', marker='x', s=60, label='lifeexpectancy <= 60')
ax[1].set_xlabel('employrate')
ax[1].set_ylabel('internetuserate')
ax[1].set_title('Scatter Plot of the Variables', fontsize=12)
ax[1].legend(loc='best',fancybox=True, shadow=True)
plt.show()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
cmhot = plt.cm.get_cmap("hot")
l = ax.scatter(sub3.employrate, sub3.internetuserate, sub3.lifeexpectancy, c=sub3.lifeexpectancy, cmap=cmhot, s=100)
ax.set_xlabel('employrate')
ax.set_ylabel('internetuserate')
ax.set_zlabel('lifeexpectancy')
ax.set_title('Scatter Plot of the Variables', fontsize=12)
fig.colorbar(l)
plt.show()
