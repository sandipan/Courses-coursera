import numpy as np
import matplotlib.mlab as mlab
import pandas as pd
import matplotlib.pylab as plt
from pandas.tools.plotting import scatter_matrix, andrews_curves, radviz
import seaborn as sns

AH_data = pd.read_csv("C:\\courses\\Coursera\\Current\\ML\\Week1\\tree_addhealth.csv")
data_clean = AH_data.dropna()

data_clean.dtypes
data_clean.describe()

#Split into training and testing sets

predictors = data_clean[['BIO_SEX','HISPANIC','WHITE','BLACK','NAMERICAN','ASIAN','age',
'ALCEVR1','ALCPROBS1','marever1','cocever1','inhever1','cigavail','DEP1','ESTEEM1','VIOL1',
'PASSIST','DEVIANT1','SCHCONN1','GPA1','EXPEL1','FAMCONCT','PARACTV','PARPRES']]

## pandas visualization

df2 = pd.DataFrame(predictors, columns=['age', 'GPA1', 'FAMCONCT'])

plt.figure()
df2.hist(alpha=0.5, bins=20)
df2.boxplot()
df2.plot(kind='area', stacked=False);
df2.plot(kind='scatter', x='age', y='GPA1', s=df2['FAMCONCT']*5);
df2.plot(kind='hexbin', x='age', y='GPA1', gridsize=25)
scatter_matrix(df2, alpha=0.2, figsize=(6, 6), diagonal='kde')
df2 = pd.DataFrame(predictors, columns=['age', 'GPA1', 'FAMCONCT', 'PARACTV', 'ASIAN', 'BIO_SEX', 'VIOL1'])
andrews_curves(df2, 'ASIAN')
radviz(df2, 'ASIAN')
g = sns.FacetGrid(df2, row="BIO_SEX", col="VIOL1", margin_titles=True)
g.map(sns.regplot, "age", "GPA1", order=2)


# matplotlib visualization
num_bins = 50
# the histogram of the data

n, bins, patches = plt.hist(df2.as_matrix(columns=df2.columns[0:1]), num_bins, normed=1, facecolor='green', alpha=0.5)
# add a 'best fit' line
plt.plot(bins, 'r--')
plt.xlabel('A')
plt.ylabel('B')
plt.title(r'C')
plt.subplots_adjust(left=0.15)
plt.show()

N = 4575
colors = np.random.rand(N)
plt.scatter(df2.as_matrix(columns=df2.columns[0:1]), df2.as_matrix(columns=df2.columns[1:2]), s=df2.as_matrix(columns=df2.columns[2:3])*2, c=colors, alpha=0.5)
plt.show()





plt.style.use('bmh')
from numpy.random import beta
def plot_beta_hist(a, b):
    plt.hist(beta(a, b, size=10000), histtype="stepfilled",
             bins=25, alpha=0.8, normed=True)
    return

plot_beta_hist(10, 10)
plot_beta_hist(4, 12)
plot_beta_hist(50, 12)
plot_beta_hist(6, 55)

plt.show()

N = 50
x = np.random.rand(N)
y = np.random.rand(N)
colors = np.random.rand(N)
area = np.pi * (15 * np.random.rand(N))**2  # 0 to 15 point radiuses

plt.scatter(x, y, s=area, c=colors, alpha=0.5)
plt.show()


x = np.arange(6)
y = np.arange(5)
z = x * y[:, np.newaxis]

for i in range(5):
    if i == 0:
        p = plt.imshow(z)
        fig = plt.gcf()
        plt.clim()   # clamp the color limits
        plt.title("Boring slide show")
    else:
        z = z + 2
        p.set_data(z)

    print("step", i)
    plt.pause(0.5)