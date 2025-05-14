#%% packages
import numpy as np
# %%
X = [0, 1]
w1 = [2, 3]
w2 = [0.4, 1.8]

# %% Question: which weight is more similar to input data X
dot_X_w1 = X[0] * w1[0] + X[1] * w1[1]
print(dot_X_w1)
#%%
dot_X_w2 = X[0] * w2[0] + X[1] * w2[1]
print(dot_X_w2)
# %%
print(np.dot(X, w1))
# %%
print(np.dot(X, w2))
# %%
