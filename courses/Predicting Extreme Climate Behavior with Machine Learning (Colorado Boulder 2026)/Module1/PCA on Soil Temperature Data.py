#!/usr/bin/env python
# coding: utf-8

# ## PCA on Soil Temperature Data

# Parquet is a columnar storage file format optimized for use with large-scale data processing frameworks. It is efficient in terms of both storage and query performance, especially with large datasets.

# In[3]:


# Importing the libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pyarrow

# Importing the libraries for PCA
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


# In[4]:


# Reading final datset

df = pd.read_parquet('pueblo.parquet')

df.head()

# note that cfs stands for cubic feet/person 

# gwl stands for ground water level 


# In[5]:


num_rows, num_cols = df.shape

print(f"Number of rows: {num_rows}")
print(f"Number of columns: {num_cols}")


# In[6]:


# We can see that we have 3 different type of soil temperature data. 
# With PCA we aim to reduce the dimensionality of the data, here particularly the soil temperature data.

# creating feature list for soil moisture data
pca_st_list = ['st_20cm', 'st_50cm', 'st_100cm']

X = df[pca_st_list]

X


# Scaling is a crucial step in Principal Component Analysis (PCA) for several reasons. Here’s why scaling (or standardizing) the data is important before applying PCA:
# 
# 1. ***Equal Weighting of Features***
# 
# **Variance Differences**: Different features in your dataset may have different units and scales (e.g., height in centimeters vs. weight in kilograms). If the features are not scaled to a common range, those with larger scales will dominate the principal components. This can lead to misleading results, where the principal components reflect the scale of the features rather than their actual importance or relationships.
# Standardization: Scaling (typically standardizing) transforms the data so that each feature has a mean of 0 and a standard deviation of
# one. This ensures that all features contribute equally to the analysis.
# 
# 2. ***Improving PCA Performance***
# 
# **Covariance Matrix**: PCA involves the calculation of the covariance matrix of the features. If the features have different scales, the covariance matrix will be dominated by features with larger variances, skewing the principal components towards those features.
# Numerical Stability: Scaling the data can also help improve the numerical stability and accuracy of the PCA computation, as large differences in scale can lead to numerical issues during matrix operations.
# 
# 3. ***Interpretability***
# 
# **Consistent Units**: By scaling the data, all features are transformed to a common scale, making the results of PCA easier to interpret. The principal components then reflect the underlying relationships between features rather than their scale.

# In[7]:


# Standardizing the features
X_scaled = StandardScaler().fit_transform(X)
X_scaled


# ###  Explained Variance in PCA
# 
# PCA is a dimensionality reduction technique that transforms the data into a new coordinate system where the axes (principal components) are ordered by the amount of variance they capture from the original data. Here's what explained variance signifies:
# 
# ### Variance Explained by Each Component:
# 
# **Explained variance** measures how much of the total variability (or variance) in the data is captured by each principal component.
# For each principal component, the explained variance quantifies the proportion of the total variance that this component captures.
# 
# ### Mathematical Aspect:
# 
# In PCA, each principal component is a linear combination of the original features. The variance of each component is derived from the eigenvalues of the covariance matrix of the original data.
# The explained variance for a principal component is proportional to its corresponding eigenvalue.
# Cumulative Explained Variance:
# 
# **Cumulative explained** variance refers to the sum of the explained variances of the principal components up to a certain point.
# It helps to determine how many principal components are needed to capture a desired amount of the total variance in the data.

# In[8]:


# Performing PCA with 3 components and plotting the explained variance

pca = PCA(n_components=3)
principalComponents = pca.fit_transform(X_scaled)
principalDf = pd.DataFrame(data = principalComponents
             , columns = ['principal component 1', 'principal component 2', 'principal component 3'])

# Plotting the explained variance as bar plot

plt.figure(figsize=(10,5))
plt.bar(range(1,4), pca.explained_variance_ratio_)
plt.xlabel('Principal Component')
plt.ylabel('Explained Variance')
plt.title('Explained Variance by Principal Component for Soil Temperature')
plt.show()


# #### We can see from the plots, the first principal component explains  more than 90% of the variance for soil temperature data

# In[9]:


# We can use the first principal component to represent the soil temperature data.

# Adding the first principal component to the dataframe
df['st_pca'] = principalDf['principal component 1']


# In[10]:


# Reseting the index and dropping the old index
df.reset_index(drop=True, inplace=True)


# In[ ]:


# Saving the final dataframe with PCA data

# This is if you want to save it 

# df.to_parquet('data/final_data/pueblo_pca.parquet')


# For your programming assignment, you will be repeating this exercise but this time using `Soil Moisture` data

# In[ ]:




