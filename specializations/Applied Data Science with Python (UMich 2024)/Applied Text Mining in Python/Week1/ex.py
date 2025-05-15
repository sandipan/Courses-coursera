import pandas as pd

def date_sorter():
    
    # Your code here

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
    out.to_csv('date_sorted.csv')
    #print(out['Year'].tolist())
    #print(set([x for x in all_indices if all_indices.count(x) > 1]))    
    #print(odf[set([x for x in all_indices if all_indices.count(x) > 1])])
    #print(odf[72])
    #print(odf[272])
    #print(odf[401])
    #print(odf[271])
    return pd.Series([i[0] for i in out.index.tolist()], index=list(range(out.shape[0]))).astype(int)

date_sorter()