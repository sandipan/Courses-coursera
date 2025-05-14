# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 18:17:30 2015

@author: sandipan
from IPython.display import HTML
HTML('''<script>
code_show=true; 
function code_toggle() {
 if (code_show){
 $('div.input').hide();
 } else {
 $('div.input').show();
 }
 code_show = !code_show
} 
$( document ).ready(code_toggle);
</script>
The raw code for this IPython notebook is by default hidden for easier reading.
To toggle on/off the raw code, click <a href="javascript:code_toggle()">here</a>.''')
%matplotlib inline
ipython nbconvert --to html notebook.ipynb
"""

import pandas
import scipy.stats
import seaborn
import matplotlib.pyplot as plt
import statsmodels.stats.multicomp as multi 

data = pandas.read_csv('C:\\courses\\Coursera\\Current\\Data Analysis Tools\\Week2\\gapminder.csv')
data.drop('country', 1)

df1 = pandas.DataFrame(data, columns=['lifeexpectancy', 'alcconsumption', 'urbanrate'])
#df1 = data.copy()
df1['alcconsumption'] = pandas.to_numeric(df1['alcconsumption'], errors='coerce')
df1['urbanrate'] = pandas.to_numeric(df1['urbanrate'], errors='coerce')
df1['lifeexpectancy'] = pandas.to_numeric(df1['lifeexpectancy'], errors='coerce')
df1 = df1.dropna()
df1.describe()

plt.figure()
df1.hist(alpha=0.5, bins=10, xrot=90)

df1['alcconsumption'] = pandas.cut(df1.alcconsumption, bins=[0,2.5,6,10,25])

seaborn.factorplot(x="alcconsumption", y="lifeexpectancy", data=df1, kind="bar", ci=None)
plt.xlabel('Alcohol Consumption (litres)')
plt.ylabel('Life Expectancy (years)')

df1['urbanrate'] = pandas.cut(df1.urbanrate, bins=[0,30,50,70,100])

seaborn.factorplot(x="urbanrate", y="lifeexpectancy", data=df1, kind="bar", ci=None)
plt.xlabel('Urban Rate (%)')
plt.ylabel('Life Expectancy (years)')

df1['lifeexpectancy'] = pandas.cut(df1.lifeexpectancy, bins=[0,70,100])
df1.head()

# contingency table of observed counts
ct1=pandas.crosstab(df1['alcconsumption'], df1['lifeexpectancy'])
print (ct1)
# column percentages
colsum=ct1.sum(axis=0)
colpct=ct1/colsum
print(colpct)
# chi-square
print ('chi-square value, p value, expected counts')
cs1= scipy.stats.chi2_contingency(ct1)
print (cs1)
# post-hoc to avoid type I errors
recode2 = {'(0, 2.5]': '(0, 2.5]', '(2.5, 6]': '(2.5, 6]'}
df1['alcconsumption2.5v6']= df1['alcconsumption'].map(recode2)
# contingency table of observed counts
ct2=pandas.crosstab(df1['alcconsumption2.5v6'], df1['lifeexpectancy'])
print (ct2)
# column percentages
colsum=ct2.sum(axis=0)
colpct=ct2/colsum
print(colpct)
print ('chi-square value, p value, expected counts')
cs2= scipy.stats.chi2_contingency(ct2)
print (cs2)
recode2 = {'(0, 2.5]': '(0, 2.5]', '(10, 25]': '(10, 25]'}
df1['alcconsumption2.5v25']= df1['alcconsumption'].map(recode2)
# contingency table of observed counts
ct2=pandas.crosstab(df1['alcconsumption2.5v25'], df1['lifeexpectancy'])
print (ct2)
# column percentages
colsum=ct2.sum(axis=0)
colpct=ct2/colsum
print(colpct)
print ('chi-square value, p value, expected counts')
cs2= scipy.stats.chi2_contingency(ct2)
print (cs2)

# contingency table of observed counts
ct1=pandas.crosstab(df1['urbanrate'], df1['lifeexpectancy'])
print (ct1)
# column percentages
colsum=ct1.sum(axis=0)
colpct=ct1/colsum
print(colpct)
# chi-square
print ('chi-square value, p value, expected counts')
cs1= scipy.stats.chi2_contingency(ct1)
print (cs1)
mc1 = multi.MultiComparison(df1['lifeexpectancy'], df1['urbanrate'])
res1 = mc1.tukeyhsd()
print(res1.summary())

