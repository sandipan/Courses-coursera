import pandas as pd
import numpy as np

np.random.seed(12345)
df = pd.DataFrame([np.random.normal(32000,200000,3650),
                   np.random.normal(43000,100000,3650),
                   np.random.normal(43500,140000,3650),
                   np.random.normal(48000,70000,3650)],
                  index=[1992,1993,1994,1995])
import matplotlib.pyplot as plt
import scipy.stats as st
import matplotlib.colors as col
import matplotlib.cm as cm
%matplotlib widget
df_mean = df.mean(axis=1)
df_std = df.std(axis=1)
n = df.shape[1]
mean = np.mean(df_mean.values)
y = mean
yerr = df_std / np.sqrt(n) * st.norm.ppf(1 - 0.05 / 2)
conf_ints = [
    st.norm.interval(alpha=0.95, loc=m, scale=s)
    for m, s in zip(df_mean, df_std / np.sqrt(n))
]
def compute_probobality(y, conf_int):
    if y < np.min(conf_int):
        result = 1.0
    elif y > np.max(conf_int):
        result = 0.0
    else:
        result = (np.max(conf_int) - y) / (np.max(conf_int) - np.min(conf_int))
    return result
probobality = [compute_probobality(y, c) for c in conf_ints]
cc = ['seismic', 'coolwarm','bwr']
cmap = cm.get_cmap(cc[2])
cpick = cm.ScalarMappable(cmap=cmap, norm=col.Normalize(vmin=0, vmax=1.0))
cpick.set_array([])
plt.figure()
bars = plt.bar(range(len(df)),
               df_mean,
               edgecolor='gray',
               yerr=yerr,
               alpha=0.8,
               color=cpick.to_rgba(probobality),
               capsize=7)
cbar = plt.colorbar(cpick, orientation="vertical")
[plt.gca().spines[loc].set_visible(False) for loc in ['top', 'right']]
hoz_line = plt.axhline(y=y, color='gray', linewidth=2, linestyle='--')
plt.title('Even Harder Option')
plt.xlabel('Year')
plt.ylabel('Value')
plt.xticks(range(len(df)), df.index)
yt_o = plt.gca().get_yticks()
yt = np.append(yt_o, y)
plt.gca().set_yticks(yt)
y_text = plt.text(1.5, 55000, 'y = %d' % y, bbox=dict(fc='white', ec='k'))
def on_click(event):
    y = event.ydata
    hoz_line.set_ydata(event.ydata)
    yt = np.append(yt_o, y)
    plt.gca().set_yticks(yt)
    y_text = plt.text(1.5, 55000, 'y = %d' % y, bbox=dict(fc='white', ec='k'))

    probobality = [compute_probobalty(y, c) for c in conf_ints]
    for i in range(len(df)):
        bars[i].set_color(cpick.to_rgba(probobality[i]))
        bars[i].set_edgecolor('gray')


plt.gcf().canvas.mpl_connect('button_press_event', on_click)
plt.show()