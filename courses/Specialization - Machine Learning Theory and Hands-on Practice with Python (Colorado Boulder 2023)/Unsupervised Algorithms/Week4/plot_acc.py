res_df = pd.DataFrame({'train data percent': [100, 50, 20, 10], 
                       'SVC acc train': [1, 1, 1, 1],
                       'SVC acc test': [0.9678, 0.94638, 0.91689, 0.53619],
                       'NMF acc train': [0.91316, 0.89964, 0.73094,  0.6036],
                       'NMF acc test': [0.8981, 0.9008, 0.67024, 0.571046]})
for col in res_df.columns.values[1:3]: 
    plt.plot(res_df['train data percent'], res_df[col], label = col)
plt.xlabel('train data percent', size=15)
plt.ylabel('accuracy', size=15)
plt.title('Accuracy with SVC')
plt.legend()
plt.show()
for col in res_df.columns.values[3:]: 
    plt.plot(res_df['train data percent'], res_df[col], label = col)
plt.xlabel('train data percent', size=15)
plt.ylabel('accuracy', size=15)
plt.title('Accuracy with NMF')
plt.legend()
plt.show()