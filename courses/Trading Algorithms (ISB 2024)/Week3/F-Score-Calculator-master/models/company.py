from calculator import ratios as ratios



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
        self.roa_cy = ratios.roa(netIncome_cy, totalAssets_cy)
        self.roa_py = ratios.roa(netIncome_py, totalAssets_py)
        self.cfo = ratios.cfo(opCashFlow_cy,begYearTotalAssets_cy);
        self.dRoa = ratios.dRoa(self.roa_cy,self.roa_py);
        self.accrual = ratios.accrual(self.cfo,self.roa_cy);
        self.dLeverage = ratios.dLeverage(longTermDebt_cy,longTermDebt_py,totalAssets_cy,totalAssets_py);
        self.dLiquid = ratios.dLiquid(currentRatio_cy,currentRatio_py);
        self.eqOffered = ratios.sharesIssued(wtdAvgShareOut_cy,wtdAvgShareOut_py);
        self.dMargin = ratios.dMargin(grossMargin_cy,grossMargin_py);
        self.dTurn = ratios.dTurn(assetTOV_cy,assetTOV_py);
