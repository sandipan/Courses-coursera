import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd
import os
import matplotlib.pyplot as plt

path = os.path.abspath(os.getcwd())
path = os.path.dirname(path)

snpReturn = -4.38
pd.set_option('display.max_rows', 84)

data_path = os.path.join(path, 'Data\AnalysisWithReturns.csv')
df = pd.read_csv(data_path)
print(df)


df= df.dropna()
print(df)

x_pred = df[['f_score']]
y = df[['Return']]

lm = LinearRegression()
lm.fit(x_pred,y)

r2 = lm.score(x_pred,y)

print(f'Linear Regression has a R-squared of{r2}')
mask = df['Return'] > snpReturn

print(df[mask])


plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = [10,15]
plt.scatter(x_pred, y,color = 'red')
plt.title('Returns vs F_score')
plt.xlabel('F_score end 2017', color='black')
plt.ylabel('Return end 2018', color='black')
plt.ylim([0,100])
plt.hist
plt.show()

