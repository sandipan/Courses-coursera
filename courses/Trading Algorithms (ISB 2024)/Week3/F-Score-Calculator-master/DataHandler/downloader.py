import requests
import json
import re


# add error checking for missing data
def getData(ticker, year):
    data = []
    i, j, k = 0, 0, 0
    # BalanceSheet
    BS = requests.get(
        f"https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/{ticker}?period=quarter&apikey=yourapikey")
    BS = BS.json()

    # Income statement
    IS = requests.get(
        f"https://financialmodelingprep.com/api/v3/financials/income-statement/{ticker}?period=quarter&apikey=yourapikey")
    IS = IS.json()

    # Cashflow statement
    CF = requests.get(
        f'https://financialmodelingprep.com/api/v3/financials/cash-flow-statement/{ticker}?period=quarter&apikey=yourapikey')
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
