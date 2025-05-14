import pandas as pd
import json
from calculator import fscore as f_score

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
            'f_score': f_score.calcF_score(company)
        }

        dataToSave.append(info)
    df = pd.DataFrame(dataToSave)
    df.to_csv('Analysis.csv', index=False, encoding='utf-8')

def saveToJson(companies):
    for company in companies:
        companyData = {'ticker': company.ticker, 'financials': [company.currentYearData, company.pastYearData, company.pastYear2Data] }
        with open(company.ticker+'.json', 'w') as file:
            json.dump(companyData,file ,indent=4)
            file.close()
