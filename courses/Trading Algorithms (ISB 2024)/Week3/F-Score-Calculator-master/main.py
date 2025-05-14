from DataHandler import tickerLoader
from DataHandler import downloader
from models import company
from DataHandler import writer


import os

path = os.path.abspath(os.getcwd())
data_path = os.path.join(path, 'Data\TickersForAnalysis1.csv')

year = '2017'

#tickers and names
tickerList = tickerLoader.getList(data_path)


print(tickerList)

companies = []
#Financial Info
for ticker in tickerList:
    print(ticker['Ticker'])
    try:
        finData = downloader.getData(ticker['Ticker'], year)
        row = company.Company(ticker['Name'], ticker['Ticker'], finData[0], finData[1], finData[2])
    except TypeError:
        continue
    except ValueError:
        continue
    except ZeroDivisionError:
        continue
    else:
        companies.append(row)

writer.saveToJson(companies)
writer.saveToExcel(companies)






