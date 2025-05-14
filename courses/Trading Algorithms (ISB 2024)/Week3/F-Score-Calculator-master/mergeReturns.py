import pandas as pd
import os
from DataHandler import returns

path = os.path.abspath(os.getcwd())
data_path = os.path.join(path, 'Data\\f_score Data\Analysis.csv')

year = '2017'

df = pd.read_csv(data_path)
print(df)

tickers = df['Ticker'].tolist()

data = []

for ticker in tickers:
    try:
        data.append({'Ticker': ticker, 'Return':returns.getPriceReturn(ticker, year)})
    except:
        data.append({'Ticker': ticker, 'Return':'NAN'})
        continue
returnInfo = pd.DataFrame(data)
finalFrame = df.merge(returnInfo, on='Ticker')
finalFrame.to_csv('Analysis.csv', index=False, encoding='utf-8')