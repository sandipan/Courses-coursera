import requests
import json
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
import yfinance as yf

headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0'}

def getAssetTurnoverRatio(ticker):
    url = 'https://csimarket.com/stocks/singleEfficiencyat.php?code=' + ticker.upper()
    response = Request(url, headers = headers)
    webpage = urlopen(response).read()
    table = pd.read_html(webpage, match='Asset Turnover Ratio')
    df = pd.DataFrame(table[2])
    ATR0 = df.iloc[3, 1]
    ATR1 = df.iloc[3, 5]
    if ATR0 > ATR1:
        return 1
    else:
        return 0
