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