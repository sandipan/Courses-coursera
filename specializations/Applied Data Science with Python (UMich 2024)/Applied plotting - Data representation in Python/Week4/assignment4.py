import pandas as pd
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
import matplotlib.colors as col
import matplotlib.cm as cm
import re
import seaborn as sb
df_lions=pd.read_html('https://en.wikipedia.org/wiki/List_of_Detroit_Lions_seasons')[1][30:]
df_lions=df_lions.loc[:,['Season','Regular season']]
df_lions=df_lions.loc[0:93,:]
df_lions['Year']=df_lions['Season']['Season'].str[:4]
df_lions['Seasons']=df_lions['Season']['Season']
df_lions.set_index('Year',inplace=True)
df_lions['win%']=df_lions['Regular season']['W']/(df_lions['Regular season']['W']+df_lions['Regular season']['L'])
df_lions=df_lions.drop(['Regular season','Season'],axis=1)
#print(df_lions)
df_tigers=pd.read_html('https://en.wikipedia.org/wiki/List_of_Detroit_Tigers_seasons')[1][59:]
df_tigers=df_tigers.loc[:,['Season','Wins','Losses','Win%']]
df_tigers=df_tigers.loc[0:123,:]
df_tigers['Year']=df_tigers['Season'].str[:4]
df_tigers.set_index('Year',inplace=True)
df_tigers['Wins']=df_tigers['Wins'].astype(int)
df_tigers['Losses']=df_tigers['Losses'].astype(int)
df_tigers['win%']=df_tigers['Wins']/(df_tigers['Wins']+df_tigers['Losses'])
#print(df_tigers)
df_pistons=pd.read_html('https://en.wikipedia.org/wiki/List_of_Detroit_Pistons_seasons')[1][22:86]
df_pistons=df_pistons.loc[:,['Season','Wins','Losses','Win%']]
df_pistons['Year']=df_pistons['Season'].str[:4]
df_pistons.set_index('Year',inplace=True)
df_pistons['Wins']=df_pistons['Wins'].astype(int)
df_pistons['Losses']=df_pistons['Losses'].astype(int)
df_pistons['win%']=df_pistons["Wins"]/(df_pistons['Wins']+df_pistons['Losses'])
#print(df_pistons)
df_redwings=pd.read_html('https://en.wikipedia.org/wiki/List_of_Detroit_Red_Wings_seasons')[2][37:101]
df_redwings=df_redwings.loc[:,['NHL season','Regular season[3][6][7][8]']]
df_redwings=df_redwings.rename(columns={'Regular season[3][6][7][8]':'Regular season','NHL season':'Season'})
df_redwings['Year']=df_redwings['Season']['Season'].str[:4]
df_redwings.set_index('Year',inplace=True)
df_redwings['Seasons']=df_redwings['Season']['Season']
df_redwings['W']=df_redwings['Regular season']['W']
df_redwings['L']=df_redwings['Regular season']['L']
df_redwings.loc['2004',['W','L']]=df_redwings.loc['2003',['W','L']]
df_redwings['W']=df_redwings['W'].astype(int)
df_redwings['L']=df_redwings['L'].astype(int)
df_redwings['win%']=df_redwings['W']/(df_redwings['W']+df_redwings['L'])
df_redwings=df_redwings.drop(['Regular season','Season'],axis=1)
#print(df_redwings)
data1=pd.merge(df_lions,df_redwings,on='Year')
data1.rename(columns={'win%_x':'win%_of_lions','win%_y':'win%_of_redwings'},inplace=True)
data1.drop(['Seasons_x','Seasons_y','W','L'],axis=1,inplace=True)
data1.columns = ['_'.join(col) for col in data1.columns.values]
#print(data1)
data2=pd.merge(df_tigers,df_pistons,on='Year')
data2.rename(columns={'win%_x':'win%_of_tigers','win%_y':'win%_of_pistons'},inplace=True)
data2.drop(['Season_x','Wins_x','Losses_x','Win%_x','Season_y','Wins_y','Losses_y','Win%_y'],axis=1,inplace=True)
#print(data2)
data=pd.merge(data1,data2,on='Year')
data.rename(columns={'win%_of_lions_':'win%_of_lions','win%_of_redwings_':'win%_of_redwings'},inplace=True)
print(data)
lions=data['win%_of_lions'].rolling(10).mean()
tigers=data['win%_of_tigers'].rolling(10).mean()
pistons=data['win%_of_pistons'].rolling(10).mean()
redwings=data['win%_of_redwings'].rolling(10).mean()
print(lions.tail(10))
xtick_label=('1969','1975','1981','1987','1993','1999','2005','2011','2017','2023')
plt.figure(figsize=(6,10))
plt.plot(lions,label='Lions',linewidth=4,color='blue',alpha=0.7)
plt.plot(tigers,label='Tigers',linewidth=4,color='orange',alpha=0.7)
plt.plot(pistons,label='Pistons',linewidth=4,color='purple',alpha=0.7)
plt.plot(redwings,label='Red Wings',linewidth=4,color='red',alpha=0.7)
plt.yticks(np.linspace(0,1,5),alpha=0.8)
plt.xticks(np.linspace(9,65,10),labels=xtick_label,rotation=45)
plt.legend(loc='best',fontsize=10)
plt.title('Detroit Sports Team Win%\n(1960-2023,10 Years Moving Average)',loc='center')
plt.xlabel(xlabel='Year')
plt.ylabel(ylabel='10 Years Moving Average Win%')
plt.axis([9,65,0,1])
kde=data.plot.kde()
[kde.spines[loc].set_visible(False) for loc in ['top', 'right']]
kde.axis([0,1,0,6])
kde.set_title('KDE of Big4 Win% in Michigan\n(1960-2023)',alpha=0.7)
kde.legend(['Lions','Tigers','Pistons','Red Wings'],loc = 'best',frameon=False, title='Big4', fontsize=10)
plt.show()