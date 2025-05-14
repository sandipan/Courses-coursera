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
