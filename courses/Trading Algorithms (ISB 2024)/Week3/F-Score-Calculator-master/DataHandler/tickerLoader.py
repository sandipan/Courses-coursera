import pandas as pd

def getList(data_path):
    list = []
    df = pd.read_csv(data_path)

    print(df)

    tickers = df['Ticker'].tolist()
    names = df['Name'].tolist()

    for i in range(len(tickers)):

        list.append({'Ticker': tickers[i], 'Name': names[i]})

    return list

