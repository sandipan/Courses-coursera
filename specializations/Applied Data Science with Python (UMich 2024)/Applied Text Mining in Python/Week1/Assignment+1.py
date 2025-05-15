
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.0** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-text-mining/resources/d9pwm) course resource._
# 
# ---

# # Assignment 1
# 
# In this assignment, you'll be working with messy medical data and using regex to extract relevant infromation from the data. 
# 
# Each line of the `dates.txt` file corresponds to a medical note. Each note has a date that needs to be extracted, but each date is encoded in one of many formats.
# 
# The goal of this assignment is to correctly identify all of the different date variants encoded in this dataset and to properly normalize and sort the dates. 
# 
# Here is a list of some of the variants you might encounter in this dataset:
# * 04/20/2009; 04/20/09; 4/20/09; 4/3/09
# * Mar-20-2009; Mar 20, 2009; March 20, 2009;  Mar. 20, 2009; Mar 20 2009;
# * 20 Mar 2009; 20 March 2009; 20 Mar. 2009; 20 March, 2009
# * Mar 20th, 2009; Mar 21st, 2009; Mar 22nd, 2009
# * Feb 2009; Sep 2009; Oct 2010
# * 6/2008; 12/2009
# * 2009; 2010
# 
# Once you have extracted these date patterns from the text, the next step is to sort them in ascending chronological order accoring to the following rules:
# * Assume all dates in xx/xx/xx format are mm/dd/yy
# * Assume all dates where year is encoded in only two digits are years from the 1900's (e.g. 1/5/89 is January 5th, 1989)
# * If the day is missing (e.g. 9/2009), assume it is the first day of the month (e.g. September 1, 2009).
# * If the month is missing (e.g. 2010), assume it is the first of January of that year (e.g. January 1, 2010).
# 
# With these rules in mind, find the correct date in each note and return a pandas Series in chronological order of the original Series' indices.
# 
# For example if the original series was this:
# 
#     0    1999
#     1    2010
#     2    1978
#     3    2015
#     4    1985
# 
# Your function should return this:
# 
#     0    2
#     1    4
#     2    0
#     3    1
#     4    3
# 
# Your score will be calculated using [Kendall's tau](https://en.wikipedia.org/wiki/Kendall_rank_correlation_coefficient), a correlation measure for ordinal data.
# 
# *This function should return a Series of length 500 and dtype int.*

# In[2]:

import pandas as pd

doc = []
with open('dates.txt') as file:
    for line in file:
        doc.append(line)

df = pd.Series(doc)
print(df.shape)
df.head(10)


# In[3]:

def date_sorter():
    
    # Your code here
    import pandas as pd

    doc = []
    with open('dates.txt') as file:
        for line in file:
            doc.append(line)

    df = pd.Series(doc)
    #print(df.shape)
    df.head(10)

    regex_strs = [r'(?P<Date>(?P<Month>(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[^,\s\.-]*)[,\s\.-]+(?P<Day>\d?\d)[a-z,\s-]+(?P<Year>[12]?[90]?\d\d))',
                 r'(?P<Date>(?P<Day>\d?\d)[,\s\.-]+(?P<Month>(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[^,\s\.-]*)[,\s\.-]+(?P<Year>[12]?[90]?\d\d))',
                 r'(?P<Date>(?P<Month>(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[^,\s\.-]*)[,\s\.-]+(?P<Year>[12]?[90]?\d\d))',
                 r'(?P<Date>(?P<Month>[0-1]?\d)[-/](?P<Day>[0-3]?\d)[-/](?P<Year>[12]?[90]?\d\d)[^\d])',
                 #r'(?P<Date>(?P<Month>[0-1]?\d)[-/](?P<Year>[12]?[90]?\d\d[^\d]))',
                 r'(?P<Date>(?P<Month>[0-1]?\d)[-/](?P<Year>[12][90]\d\d)[^\d])',
                 r'(?P<Date>(?P<Month>[0-1]?\d)[-/](?P<Year>\d\d)[^\d])',
                 r'(?P<Date>(?P<Year>[12][90]\d\d))']
    
    months = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
    odf = df.copy()
    all_indices = []
    indices = list(range(df.shape[0]))
    out = pd.DataFrame()
    for i in range(len(regex_strs)):
        regex_str = regex_strs[i] 
        df = df[indices]
        df1 = df.str.extractall(regex_str)
        #print(df1.shape)
        if not 'Month' in df1.columns:
            df1['Month'] = 1
        else:
            for mon in months:
                df1['Month'] = df1['Month'].str.replace(mon + '.*', str(months[mon]))
                #df1[df1['Month'].str.contains(mon)]['Month'] = 
        if not 'Day' in df1.columns:
            df1['Day'] = 1
        #df1['Year'] = df1['Year'].str.replace(r'[^\d](\d\d)[^\d]', lambda x: '19' + x.groups()[0])
        df1.ix[df1['Year'].str.len()==2,'Year'] = '19' + df1[df1['Year'].str.len()==2]['Year']
        #print(df1[['Day', 'Month', 'Year']].head())
        out = out.append(df1[['Day', 'Month', 'Year']])
        current_indices = [i[0] for i in df1.index.tolist()]
        #if 72 in current_indices: print(df1.iloc[72])
        indices = list(set(indices) - set(current_indices)) #indices = [j for j in indices if j not in current_indices]
        all_indices += current_indices
    #print(out.head())  
    out[['Year', 'Month', 'Day']] = out[['Year', 'Month', 'Day']].astype(int)
    out.sort_values(['Year', 'Month', 'Day'], ascending=[True, True, True], inplace=True)
    #print(out.head(500))  
    #print(out['Year'].tolist())
    #print(set([x for x in all_indices if all_indices.count(x) > 1]))    
    #print(odf[set([x for x in all_indices if all_indices.count(x) > 1])])
    #print(odf[72])
    #print(odf[272])
    #print(odf[401])
    #print(odf[271])
    return pd.Series([i[0] for i in out.index.tolist()], index=list(range(out.shape[0]))).astype(int)

date_sorter()


# In[ ]:



