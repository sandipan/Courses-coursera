import requests
import re
import pandas as pd
import json
import os

notebook_path = os.path.abspath(os.getcwd())
notebook_path = os.path.dirname(notebook_path)
print(notebook_path)
data_path = os.path.join(notebook_path, 'Data\list of companies historical.csv')
print(data_path)
df = pd.read_csv(data_path)

tickersFromFile =  df['Ticker'].tolist();
year = '2015'




data_path = os.path.join(notebook_path,'Data\\financial-statement-symbol-lists.json')
print (data_path)
with open(data_path) as file:
    availableTickers = json.load(file)



print(len(availableTickers))
tickersForAnalysis1 = []
for i in range(len(availableTickers)):
    for ticker in tickersFromFile:
        if ticker == availableTickers[i]:
            tickersForAnalysis1.append(ticker)
print(len(tickersForAnalysis1))
print(tickersForAnalysis1)
df2 = pd.DataFrame(tickersForAnalysis1)
print(df2)
tickersForAnalysis2 = []
for j in range (len(tickersForAnalysis1)): #total357
    print(tickersForAnalysis1[j])
    try:
        BS = requests.get(f"https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/{tickersForAnalysis1[j]}?period=quarter&apikey=yourapikey")
        BS = BS.json()
        print(len(BS['financials']))
    except KeyError:
        continue
    else:
        if len(BS['financials'])>23:
            for a in range(len(BS['financials'])):
                if re.search(f'{year}-\d\d-\d\d', BS['financials'][a]['date']):
                    tickersForAnalysis2.append(tickersForAnalysis1[j])
                    break

print(tickersForAnalysis2)


rslFrame = df[df['Ticker'].isin(tickersForAnalysis2)]
print(rslFrame)





rslFrame.to_csv('TickersForAnalysis1.csv', index=False, encoding='utf')
