import pandas as pd
from ggplot import *
df = pd.read_csv('weights1.csv')
df = df.melt(id_vars=['lambda'])
print df
ggplot(df, aes(x='lambda', y='value', col='variable')) + geom_line()
plt.show()