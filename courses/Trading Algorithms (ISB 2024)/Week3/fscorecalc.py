import requests
import json
import re

import pandas as pd

def roa(netIncome,totalAssets):
    roa = netIncome/totalAssets
    return roa

def cfo(opCashFlow,begYearTotalAssets):
    cfo = opCashFlow/begYearTotalAssets
    return cfo

def dRoa(roa1,roa2):
    dRoa = roa1-roa2
    return dRoa

def dLeverage(longTermDebt1,longTermDebt2,totalAssets1,totalAssets2):
    dLeverage = (longTermDebt1-longTermDebt2)/((totalAssets1+totalAssets2)/2)
    return dLeverage

def dLiquid(currentRatio1,currentRatio2):
    dLiquid = currentRatio1-currentRatio2
    return dLiquid

def currentRatio(currentAssets,currentLiabilities):
    currentRatio = currentAssets/currentLiabilities
    return currentRatio

def sharesIssued(wtdSharesOut1,wtdSharesOut2):
    sharesIssued = wtdSharesOut1-wtdSharesOut2
    return sharesIssued

def accrual(cfo,roa):
    accrual = cfo-roa
    return accrual

def dMargin(margin1,margin2):
    dMargin = margin1-margin2
    return dMargin

def margin(grossProfit,revenue):
    margin = grossProfit/revenue
    return margin

def dTurn(assetTOV1,assetTOV2):
    dTurn= assetTOV1-assetTOV2
    return dTurn

def assetTOV (revenue, begYearTotalAssets):
    assetTOV = revenue/begYearTotalAssets
    return assetTOV

class Company:
    def __init__(self,name, ticker, fin_cy, fin_py, fin_py2):
        self.name = name
        self.ticker = ticker
        self.currentYearData = fin_cy
        self.pastYearData = fin_py
        self.pastYear2Data = fin_py2
        # Required data from fin statements

        netIncome_cy = fin_cy['Net Income']
        revenue_cy = fin_cy['Revenue']
        grossMargin_cy = fin_cy['Gross Margin']
        totalAssets_cy = fin_cy['Total Assets']
        opCashFlow_cy = fin_cy['Operating Cash Flow']
        begYearTotalAssets_cy = fin_cy['Beginning Year Total Assets']
        longTermDebt_cy = fin_cy['Long Term Debt']
        currentAssets_cy = fin_cy['Current Assets']
        currentLiabilities_cy = fin_cy['Current Liabilities']
        currentRatio_cy = ratios.currentRatio(currentAssets_cy, currentLiabilities_cy)
        wtdAvgShareOut_cy = fin_cy['Weighted Average Shares Out']
        assetTOV_cy = ratios.assetTOV(revenue_cy, begYearTotalAssets_cy)

        revenue_py = fin_py['Revenue']
        netIncome_py = fin_py['Net Income']
        grossMargin_py = fin_py['Gross Margin']
        totalAssets_py = fin_py['Total Assets']
        opCashFlow_py = fin_py['Operating Cash Flow']
        begYearTotalAssets_py = fin_py['Beginning Year Total Assets']
        longTermDebt_py = fin_py['Long Term Debt']
        currentAssets_py = fin_py['Current Assets']
        currentLiabilities_py = fin_py['Current Liabilities']
        currentRatio_py = ratios.currentRatio(currentAssets_py, currentLiabilities_py)
        wtdAvgShareOut_py = fin_py['Weighted Average Shares Out']
        assetTOV_py = ratios.assetTOV(revenue_py, begYearTotalAssets_py)


        totalAssets_py2 = fin_py2['Total Assets']

        # metrics
        self.roa_cy = roa(netIncome_cy, totalAssets_cy)
        self.roa_py = roa(netIncome_py, totalAssets_py)
        self.cfo = cfo(opCashFlow_cy,begYearTotalAssets_cy);
        self.dRoa = dRoa(self.roa_cy,self.roa_py);
        self.accrual = accrual(self.cfo,self.roa_cy);
        self.dLeverage = dLeverage(longTermDebt_cy,longTermDebt_py,totalAssets_cy,totalAssets_py);
        self.dLiquid = dLiquid(currentRatio_cy,currentRatio_py);
        self.eqOffered = sharesIssued(wtdAvgShareOut_cy,wtdAvgShareOut_py);
        self.dMargin = dMargin(grossMargin_cy,grossMargin_py);
        self.dTurn = dTurn(assetTOV_cy,assetTOV_py);

def calcF_score(company):
    roa = 1 if company.roa_cy > 0 else 0
    cfo = 1 if company.cfo > 0 else 0
    droa = 1 if (company.roa_cy - company.roa_py) > 0 else 0
    accrual = 1 if company.cfo > company.roa_cy else 0
    dlever = 1 if company.dLeverage < 0 else 0
    dLiquid = 1 if company.dLiquid > 0 else 0
    eqOffered = 1 if company.eqOffered <= 0 else 0
    dMargin = 1 if company.dMargin > 0 else 0
    dTurn = 1 if company.dTurn > 0 else 0

    return (roa + cfo + droa + accrual + dlever + dLiquid + eqOffered + dMargin + dTurn)



def saveToExcel(data):
    dataToSave = []
    for company in data:
        info = {
            'Ticker': company.ticker,
            'Name': company.name,
            'ROA': company.roa_cy,
            'CFO': company.cfo,
            'dROA': company.dRoa,
            'Accrual': company.accrual,
            'dLeverage': company.dLeverage,
            'dLiquid': company.dLiquid,
            'EQ_Offered': company.eqOffered,
            'dMargin': company.dMargin,
            'dTurn': company.dTurn,
            'f_score': calcF_score(company)
        }

        dataToSave.append(info)
    df = pd.DataFrame(dataToSave)
    df.to_csv('Analysis.csv', index=False, encoding='utf-8')

def getList(data_path):
    list = []
    df = pd.read_csv(data_path)

    print(df)

    tickers = df['Ticker'].tolist()
    names = df['Name'].tolist()

    for i in range(len(tickers)):

        list.append({'Ticker': tickers[i], 'Name': names[i]})

    return list

# add error checking for missing data
def getData(ticker, year):
    data = []
    i, j, k = 0, 0, 0
    # BalanceSheet
    BS = requests.get(
        f"https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/{ticker}?period=quarter&apikey={yourapikey}")
    BS = BS.json()
    print(pd.DataFrame.from_dict(pd.json_normalize(BS), orient='columns'))

    # Income statement
    IS = requests.get(
        f"https://financialmodelingprep.com/api/v3/financials/income-statement/{ticker}?period=quarter&apikey={yourapikey}")
    IS = IS.json()

    # Cashflow statement
    CF = requests.get(
        f'https://financialmodelingprep.com/api/v3/financials/cash-flow-statement/{ticker}?period=quarter&apikey={yourapikey}')
    CF = CF.json()

    for a in range(len(BS['financials'])):
        if re.search(f'{year}-\d\d-\d\d', BS['financials'][a]['date']):
            i = a
            j = i + 4
            k = i + 8
            break

    # Calculated Income Items
    # Current Year
    revenue = float(IS['financials'][i]['Revenue']) + float(IS['financials'][i + 1]['Revenue']) + float(
        IS['financials'][i + 2]['Revenue']) + float(IS['financials'][i + 3]['Revenue'])
    gross_margin = (float(IS['financials'][i]['Gross Margin']) + float(IS['financials'][i + 1]['Gross Margin']) + float(
        IS['financials'][i + 2]['Gross Margin']) + float(IS['financials'][i + 3]['Gross Margin'])) / 4
    net_income = float(IS['financials'][i]['Net Income']) + float(IS['financials'][i + 1]['Net Income']) + float(
        IS['financials'][i + 2]['Net Income']) + float(IS['financials'][i + 3]['Net Income'])

    # Past Year
    revenue_py = float(IS['financials'][j]['Revenue']) + float(IS['financials'][j + 1]['Revenue']) + float(
        IS['financials'][j + 2]['Revenue']) + float(IS['financials'][j + 3]['Revenue'])
    gross_margin_py = (float(IS['financials'][j]['Gross Margin']) + float(
        IS['financials'][j + 1]['Gross Margin']) + float(IS['financials'][j + 2]['Gross Margin']) + float(
        IS['financials'][j + 3]['Gross Margin'])) / 4
    net_income_py = float(IS['financials'][j]['Net Income']) + float(IS['financials'][j + 1]['Net Income']) + float(
        IS['financials'][j + 2]['Net Income']) + float(IS['financials'][j + 3]['Net Income'])

    # Past Year 2
    revenue_py2 = float(IS['financials'][k]['Revenue']) + float(IS['financials'][k + 1]['Revenue']) + float(
        IS['financials'][k + 2]['Revenue']) + float(IS['financials'][k + 3]['Revenue'])
    gross_margin_py2 = (float(IS['financials'][k]['Gross Margin']) + float(
        IS['financials'][k + 1]['Gross Margin']) + float(IS['financials'][k + 2]['Gross Margin']) + float(
        IS['financials'][k + 3]['Gross Margin'])) / 4
    net_income_py2 = float(IS['financials'][k]['Net Income']) + float(IS['financials'][k + 1]['Net Income']) + float(
        IS['financials'][k + 2]['Net Income']) + float(IS['financials'][k + 3]['Net Income'])

    # Calculated Cashflow Items
    # Current Year
    cashflow_op = float(CF['financials'][i]["Operating Cash Flow"]) + float(
        CF['financials'][i + 1]["Operating Cash Flow"]) + float(CF['financials'][i + 2]["Operating Cash Flow"]) + float(
        CF['financials'][i + 3]["Operating Cash Flow"])

    # Past Year
    cashflow_op_py = float(CF['financials'][j]["Operating Cash Flow"]) + float(
        CF['financials'][j + 1]["Operating Cash Flow"]) + float(CF['financials'][j + 2]["Operating Cash Flow"]) + float(
        CF['financials'][j + 3]["Operating Cash Flow"])

    # Past Year2
    cashflow_op_py2 = float(CF['financials'][k]["Operating Cash Flow"]) + float(
        CF['financials'][k + 1]["Operating Cash Flow"]) + float(CF['financials'][k + 2]["Operating Cash Flow"]) + float(
        CF['financials'][k + 3]["Operating Cash Flow"])

    # Calculated Balance Items
    # Current Year
    begYearTotalAssets = float(BS['financials'][i + 4]["Total assets"])

    # Past Year
    begYearTotalAssets_py = float(BS['financials'][j + 4]["Total assets"])

    # Past Year2
    begYearTotalAssets_py2 = float(BS['financials'][k + 4]["Total assets"])

    fin_cy = {'Date': IS["financials"][i]['date'],
              'Net Income': net_income,
              'Total Assets': float(BS["financials"][i]['Total assets']),
              'Operating Cash Flow': cashflow_op,
              'Beginning Year Total Assets': begYearTotalAssets,
              'Long Term Debt': float(BS["financials"][i]['Long-term debt']),
              'Current Assets': float(BS["financials"][i]['Total current assets']),
              'Current Liabilities': float(BS["financials"][i]['Total current liabilities']),
              'Weighted Average Shares Out': float(IS['financials'][i]['Weighted Average Shs Out']),
              'Gross Margin': gross_margin,
              'Revenue': revenue
              }

    fin_py = {'Date': IS["financials"][j]['date'],
              'Net Income': net_income_py,
              'Total Assets': float(BS["financials"][j]['Total assets']),
              'Operating Cash Flow': cashflow_op_py,
              'Beginning Year Total Assets': begYearTotalAssets_py,
              'Long Term Debt': float(BS["financials"][j]['Long-term debt']),
              'Current Assets': float(BS["financials"][j]['Total current assets']),
              'Current Liabilities': float(BS["financials"][j]['Total current liabilities']),
              'Weighted Average Shares Out': float(IS['financials'][j]['Weighted Average Shs Out']),
              'Gross Margin': gross_margin_py,
              'Revenue': revenue_py
              }

    fin_py2 = {'Date': IS["financials"][k]['date'],
               'Net Income': net_income_py2,
               'Total Assets': float(BS["financials"][k]['Total assets']),
               'Operating Cash Flow': cashflow_op_py2,
               'Beginning Year Total Assets': begYearTotalAssets_py2,
               'Long Term Debt': float(BS["financials"][k]['Long-term debt']),
               'Current Assets': float(BS["financials"][k]['Total current assets']),
               'Current Liabilities': float(BS["financials"][k]['Total current liabilities']),
               'Weighted Average Shares Out': float(IS['financials'][k]['Weighted Average Shs Out']),
               'Gross Margin': gross_margin_py2,
               'Revenue': revenue_py2
               }
    data.append(fin_cy)
    data.append(fin_py)
    data.append(fin_py2)

    return data

'''

import os

path = os.path.abspath(os.getcwd())
data_path = os.path.join(path, 'TickersForAnalysis1.csv')

year = '2022'

#tickers and names
tickerList = getList(data_path)
tickerList = [{'Ticker': 'AAPL', 'Name': 'Apple Inc.'}]

print(tickerList)

companies = []
#Financial Info
for ticker in tickerList:
    print(ticker['Ticker'])
    try:
        finData = getData(ticker['Ticker'], year)
        row = Company(ticker['Name'], ticker['Ticker'], finData[0], finData[1], finData[2])
    except TypeError:
        continue
    except ValueError:
        continue
    except ZeroDivisionError:
        continue
    else:
        companies.append(row)

saveToJson(companies)
saveToExcel(companies)
'''

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import certifi
import json

def get_jsonparsed_data(url):
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)

yourapikey = '2crg30sdW90uhqdlinMHRibqHxSaAktI'
url = (f"https://financialmodelingprep.com/api/v3/income-statement/AAPL?apikey={yourapikey}")
df = get_jsonparsed_data(url)
df = pd.DataFrame(df)
print(df.head())
#df = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v3/historical-chart/5min/AAPL?from=2023-10-10&to=2023-08-10&apikey={yourapikey}")
