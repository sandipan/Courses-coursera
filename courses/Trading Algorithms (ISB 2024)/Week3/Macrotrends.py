import requests
import json
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
import yfinance as yf
from re import sub
from decimal import Decimal
import contextlib

headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0'}

def url_open(response):
    with contextlib.closing(urlopen(response)) as x:
        webpage = x.read()
    return webpage

#ROA
def getData(ticker):
    companyName = yf.Ticker(ticker)
    companyName = companyName.info['shortName']
    c = companyName.split(" ")
    url = 'https://www.macrotrends.net/stocks/charts/' + ticker.upper() + '/' + c[0] + '/roa'
    response = Request(url, headers = headers)
    webpage = url_open(response)
    table = pd.read_html(webpage, match='Return on Assets Historical Data')
    df = pd.DataFrame(np.concatenate(table))
    df.columns = ['Date', 'TTM Net Income', 'Total Assets', 'Return on Assets']

    return df

def getROA(df):
    roa = df.iloc[0]['Return on Assets']
    roa = float(roa.strip('%'))
    if roa > 0:
        return 1
    else:
        return 0

def changeInROA(df):
    roa = df.iloc[0]['Return on Assets']
    roaOld = df.iloc[1]['Return on Assets']
    roa = float(roa.strip('%'))
    roaOld = float(roaOld.strip('%'))
    if roa > roaOld:
        return 1
    else:
        return 0

#Shares Outstanding
def getSharesOutstanding(ticker):
    companyName = yf.Ticker(ticker)
    companyName = companyName.info['shortName']
    c = companyName.split(" ")
    url = 'https://www.macrotrends.net/stocks/charts/' + ticker.upper() + '/' + c[0] + '/shares-outstanding'
    response = Request(url, headers = headers)
    webpage  = url_open(response)
    table = pd.read_html(webpage, match='Annual Shares Outstanding')
    df = pd.DataFrame(np.concatenate(table))
    df.columns = ['Date', 'Shares']
    SO0 = df.iloc[0][1]
    SO1 = df.iloc[1][1]

    if SO0 <= SO1:
        return 1
    else:
        return 0

def getNetRevenue(ticker):
    companyName = yf.Ticker(ticker)
    companyName = companyName.info['shortName']
    c = companyName.split(" ")
    url = 'https://www.macrotrends.net/stocks/charts/' + ticker.upper() + '/' + c[0] + '/revenue'
    response = Request(url, headers = headers)
    webpage = url_open(response)
    table = pd.read_html(webpage, match='Annual Revenue')
    df = pd.DataFrame(np.concatenate(table))
    df.columns = ['Date', 'Net Revenue']
    NR0 = df.iloc[0][1]
    NR1 = df.iloc[1][1]
    NR = [NR0, NR1]

    return NR

def getCOGS(ticker):
    companyName = yf.Ticker(ticker)
    companyName = companyName.info['shortName']
    c = companyName.split(" ")
    url = 'https://www.macrotrends.net/stocks/charts/' + ticker.upper() + '/' + c[0] + '/cost-goods-sold'
    print(url)
    response = Request(url, headers = headers)
    webpage = url_open(response)
    table = pd.read_html(webpage, match='Annual Cost of Goods Sold')
    df = pd.DataFrame(np.concatenate(table))
    df.columns = ['Date', 'COGS']
    COGS0 = df.iloc[0][1]
    COGS1 = df.iloc[1][1]
    COGS = [COGS0, COGS1]

    return COGS

def getGrossMargin(NR, COGS):
    NR0 = Decimal(sub(r'[^\d.]', '', NR[0]))
    NR1 = Decimal(sub(r'[^\d.]', '', NR[1]))
    COGS0 = Decimal(sub(r'[^\d.]', '', COGS[0]))
    COGS1 = Decimal(sub(r'[^\d.]', '', COGS[1]))

    GM0 = NR0 - COGS0
    GM1 = NR1 - COGS1

    if GM0 > GM1:
        return 1
    else:
        return 0

def getAssetTurnoverRatio(ticker):
    companyName = yf.Ticker(ticker)
    companyName = companyName.info['shortName']
    c = companyName.split(" ")
    url = 'https://www.macrotrends.net/stocks/charts/' + ticker.upper() + '/' + c[0] + '/shares-outstanding'
    response = Request(url, headers = headers)
    webpage = url_open(response)
    table = pd.read_html(webpage, match='Annual Shares Outstanding')
    df = pd.DataFrame(np.concatenate(table))
    df.columns = ['Date', 'Shares']
    SO0 = df.iloc[0][1]
    SO1 = df.iloc[1][1]

    if SO0 <= SO1:
        return 1
    else:
        return 0

c = getCOGS("AAPL")
n = getNetRevenue("AAPL")
getGrossMargin(n, c)
