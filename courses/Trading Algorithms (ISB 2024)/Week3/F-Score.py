import requests
import json
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
import yfinance as yf
from Macrotrends import *

def main(ticker):
    stock = yf.Ticker(ticker)
    financials = stock.financials
    balanceSheet = stock.balance_sheet
    cashFlow = stock.cashflow
    dfFin = pd.DataFrame(financials)
    print(dfFin.head())
    dfBs = pd.DataFrame(balanceSheet)
    print(dfBs.head())
    dfCf = pd.DataFrame(cashFlow)
    print(dfCf.head())
    NI = dfFin.iloc[4][0]
    totalAssets = dfBs.iloc[3][0]
    ROA = NI / totalAssets
    OI = dfFin.iloc[8][0]
    CF = dfCf.iloc[10][0]
    LTD0 = dfBs.iloc[20][0]
    LTD1 = dfBs.iloc[20][1]
    CR0 = (dfBs.iloc[15][0]) / (dfBs.iloc[11][0])
    CR1 = (dfBs.iloc[15][1]) / (dfBs.iloc[11][1])
    c = getCOGS(ticker)
    n = getNetRevenue(ticker)

    NIScore = 0
    ROAScore = 0
    CFScore = 0
    CFNIScore = 0
    LTDScore = 0
    CRScore = 0

    if NI > 0:
        NIScore = 1
    if ROA > 0:
        ROAScore = 1
    if CF > 0:
        CFScore = 1
    if CF > NI:
        CFNIScore = 1
    if LTD0 < LTD1:
        LTDScore = 1
    if CR0 > CR1:
        CRScore = 1

    dilutionScore = getSharesOutstanding(ticker)
    grossMarginScore = getGrossMargin(n, c)
    assetTurnoverRatioScore = getAssetTurnoverRatio(ticker)

    """
    print(NIScore)
    print(ROAScore)
    print(CFScore)
    print(CFNIScore)
    print(LTDScore)
    print(CRScore)
    print(dilutionScore)
    print(grossMarginScore)
    print(assetTurnoverRatioScore)
    """

    totalScore = NIScore + ROAScore + CFScore + CFNIScore + LTDScore + CRScore + dilutionScore + grossMarginScore + assetTurnoverRatioScore

    print(totalScore)
    return dfFin

var = True
while var:
    stock = input("Enter the stock: ")
    stock.upper()
    if(stock != "QUIT"):
        main(stock)
        var = False
