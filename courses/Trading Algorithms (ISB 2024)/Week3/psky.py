import numpy as np
import pandas as pd
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename


def read_data():
    df = askopenfilename(filetypes=[('CSV', '*.csv',), ('Excel', ('*.xls', '*.xlsx'))],defaultextension='.xlsx')
    global data
    if df :
        if df .endswith('.xlsx'):
            data = pd.read_excel(df)

        else:
            data = pd.read_csv(df)
    root.destroy()
    
if __name__ == '__main__':
    root =tk.Tk()
    tk.Button(root, text='Open File', command = read_data).pack()
    root.geometry("150x150+400+200")
    root.configure(bg='blue')
    tk.mainloop()

        
#data=pd.read_excel('Data.xlsx')
name=data['Name'].unique().tolist();
N=len(data['Name'].unique());
names_values=[]
for i in range(0,N):
    tempData=data[data['Name']== data['Name'].unique()[i]];
        # Factor 1-4:
    ROA= tempData['net income']/tempData['T-Asset'];
    if ROA.iloc[-1] >0:
       F_ROA=1
    else:
       F_ROA=0
    
    CFO=tempData['CFO']/tempData['T-Asset'];
    if CFO.iloc[-1] >0:
       F_CFO=1
    else:
       F_CFO=0
    
    DROA=np.diff(ROA);
    if DROA[-1] >0:
       F_DROA=1
    else:
       F_DROA=0
    
    Accrual= ROA-CFO;
    if Accrual.iloc[-1] <0:
       F_Accrual=1
    else:
       F_Accrual=0
    
        # Factor 5: Delta leverage
    Leverage=tempData['T-LT-debt']/tempData['T-Asset'];
    DLeverage=np.diff(Leverage);
    if DLeverage[len(DLeverage)-1] <0:
       F_DLeverage=1
    else:
       F_DLeverage=0
    
         # Factor 6-	Delta Liquid
    Current_ratio= tempData['current assets']/tempData['current Liabilities'];
    Delta_Liquid=Current_ratio.iloc[-1]-Current_ratio.iloc[-2];
    if Delta_Liquid >0:
       F_Delta_Liquid=1
    else:
       F_Delta_Liquid=0
    
        # Factor 7-	Eq_offer 
    if (tempData['common_stock'].iloc[-1]-tempData['common_stock'].iloc[-2]) == 0:
       Eq_offer=1
    else: 
       Eq_offer=0
    
        # Factor 8-9  Delta margin  and Delta turnover
    margin= tempData['profit']/tempData['sales'];
    turnover=tempData['sales']/tempData['T-Asset'];
    Delta_margin=margin.iloc[-1]-margin.iloc[-2];
    Delta_turnover=turnover.iloc[-1]-turnover.iloc[-2];

    if (Delta_margin >0 and Delta_turnover>0) :
       F_Delta_margin=1
       F_Delta_turnover=1
    
    elif (Delta_margin >0 and Delta_turnover<0) :
         F_Delta_margin=1
         F_Delta_turnover=0
    elif (Delta_margin <0 and Delta_turnover>0) :
         F_Delta_margin=0
         F_Delta_turnover=1
    else:
         F_Delta_margin=0
         F_Delta_turnover=0
    value=F_ROA+F_CFO+F_DROA+F_Accrual+F_DLeverage+F_Delta_Liquid+Eq_offer+F_Delta_margin+F_Delta_turnover
    names_values.append([name[i],value])

K1=pd.DataFrame(sorted(names_values,reverse=False),columns=['Name','Value'])
K2=pd.DataFrame(np.arange(1, N+1, 1).tolist(),columns=['Rank'])
Final_outcome=pd.concat([K1,K2], axis=1, sort=False)

def save():
    import os
        
    formats=[('CSV', '*.csv'), ('Excel','*.xls'),('Excel', '*.xlsx')]
    export_output = asksaveasfilename(filetypes=formats,defaultextension='.csv',title='Output')
        
    if export_output.endswith('.csv'):
        Final_outcome.to_csv (export_output, index = False, header=True)
    if export_output.endswith('.xls') or export_output.endswith('.xlsx'):
        Final_outcome.to_excel (export_output, index = False, header=True)
    root.destroy()
    
    
    
if __name__ == '__main__':

    root =tk.Tk()
    tk.Button(root, text='Save the result', command = save).pack()
    root.geometry("150x150+400+200")
    root.configure(bg='green')
    tk.mainloop()