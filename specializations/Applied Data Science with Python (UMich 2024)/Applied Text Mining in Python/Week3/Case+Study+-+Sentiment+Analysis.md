
---

_You are currently looking at **version 1.0** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-text-mining/resources/d9pwm) course resource._

---

*Note: Some of the cells in this notebook are computationally expensive. To reduce runtime, this notebook is using a subset of the data.*

# Case Study: Sentiment Analysis

### Data Prep


```python
import pandas as pd
import numpy as np

# Read in the data
df = pd.read_csv('Amazon_Unlocked_Mobile.csv')

# Sample the data to speed up computation
# Comment out this line to match with lecture
df = df.sample(frac=0.1, random_state=10)

df.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Product Name</th>
      <th>Brand Name</th>
      <th>Price</th>
      <th>Rating</th>
      <th>Reviews</th>
      <th>Review Votes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>394349</th>
      <td>Sony XPERIA Z2 D6503 FACTORY UNLOCKED Internat...</td>
      <td>NaN</td>
      <td>244.95</td>
      <td>5</td>
      <td>Very good one! Better than Samsung S and iphon...</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>34377</th>
      <td>Apple iPhone 5c 8GB (Pink) - Verizon Wireless</td>
      <td>Apple</td>
      <td>194.99</td>
      <td>1</td>
      <td>The phone needed a SIM card, would have been n...</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>248521</th>
      <td>Motorola Droid RAZR MAXX XT912 M Verizon Smart...</td>
      <td>Motorola</td>
      <td>174.99</td>
      <td>5</td>
      <td>I was 3 months away from my upgrade and my Str...</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>167661</th>
      <td>CNPGD [U.S. Office Extended Warranty] Smartwat...</td>
      <td>CNPGD</td>
      <td>49.99</td>
      <td>1</td>
      <td>an experience i want to forget</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>73287</th>
      <td>Apple iPhone 7 Unlocked Phone 256 GB - US Vers...</td>
      <td>Apple</td>
      <td>922.00</td>
      <td>5</td>
      <td>GREAT PHONE WORK ACCORDING MY EXPECTATIONS.</td>
      <td>1.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Drop missing values
df.dropna(inplace=True)

# Remove any 'neutral' ratings equal to 3
df = df[df['Rating'] != 3]

# Encode 4s and 5s as 1 (rated positively)
# Encode 1s and 2s as 0 (rated poorly)
df['Positively Rated'] = np.where(df['Rating'] > 3, 1, 0)
df.head(10)
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Product Name</th>
      <th>Brand Name</th>
      <th>Price</th>
      <th>Rating</th>
      <th>Reviews</th>
      <th>Review Votes</th>
      <th>Positively Rated</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>34377</th>
      <td>Apple iPhone 5c 8GB (Pink) - Verizon Wireless</td>
      <td>Apple</td>
      <td>194.99</td>
      <td>1</td>
      <td>The phone needed a SIM card, would have been n...</td>
      <td>1.0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>248521</th>
      <td>Motorola Droid RAZR MAXX XT912 M Verizon Smart...</td>
      <td>Motorola</td>
      <td>174.99</td>
      <td>5</td>
      <td>I was 3 months away from my upgrade and my Str...</td>
      <td>3.0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>167661</th>
      <td>CNPGD [U.S. Office Extended Warranty] Smartwat...</td>
      <td>CNPGD</td>
      <td>49.99</td>
      <td>1</td>
      <td>an experience i want to forget</td>
      <td>0.0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>73287</th>
      <td>Apple iPhone 7 Unlocked Phone 256 GB - US Vers...</td>
      <td>Apple</td>
      <td>922.00</td>
      <td>5</td>
      <td>GREAT PHONE WORK ACCORDING MY EXPECTATIONS.</td>
      <td>1.0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>277158</th>
      <td>Nokia N8 Unlocked GSM Touch Screen Phone Featu...</td>
      <td>Nokia</td>
      <td>95.00</td>
      <td>5</td>
      <td>I fell in love with this phone because it did ...</td>
      <td>0.0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>100311</th>
      <td>Blackberry Torch 2 9810 Unlocked Phone with 1....</td>
      <td>BlackBerry</td>
      <td>77.49</td>
      <td>5</td>
      <td>I am pleased with this Blackberry phone! The p...</td>
      <td>0.0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>251669</th>
      <td>Motorola Moto E (1st Generation) - Black - 4 G...</td>
      <td>Motorola</td>
      <td>89.99</td>
      <td>5</td>
      <td>Great product, best value for money smartphone...</td>
      <td>0.0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>279878</th>
      <td>OtterBox 77-29864 Defender Series Hybrid Case ...</td>
      <td>OtterBox</td>
      <td>9.99</td>
      <td>5</td>
      <td>I've bought 3 no problems. Fast delivery.</td>
      <td>0.0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>406017</th>
      <td>Verizon HTC Rezound 4G Android Smarphone - 8MP...</td>
      <td>HTC</td>
      <td>74.99</td>
      <td>4</td>
      <td>Great phone for the price...</td>
      <td>0.0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>302567</th>
      <td>RCA M1 Unlocked Cell Phone, Dual Sim, 5Mp Came...</td>
      <td>RCA</td>
      <td>159.99</td>
      <td>5</td>
      <td>My mom is not good with new technoloy but this...</td>
      <td>4.0</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Most ratings are positive
df['Positively Rated'].mean()
```




    0.7471776686078667




```python
from sklearn.model_selection import train_test_split

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(df['Reviews'], 
                                                    df['Positively Rated'], 
                                                    random_state=0)
```


```python
print('X_train first entry:\n\n', X_train.iloc[0])
print('\n\nX_train shape: ', X_train.shape)
```

    X_train first entry:
    
     Everything about it is awesome!
    
    
    X_train shape:  (23052,)


# CountVectorizer


```python
from sklearn.feature_extraction.text import CountVectorizer

# Fit the CountVectorizer to the training data
vect = CountVectorizer().fit(X_train)
```


```python
vect.get_feature_names()[::2000]
```




    ['00',
     'arroja',
     'comapañias',
     'dvds',
     'golden',
     'lands',
     'oil',
     'razonable',
     'smallsliver',
     'tweak']




```python
len(vect.get_feature_names())
```




    19601




```python
# transform the documents in the training data to a document-term matrix
X_train_vectorized = vect.transform(X_train)

X_train_vectorized
```




    <23052x19601 sparse matrix of type '<class 'numpy.int64'>'
    	with 613289 stored elements in Compressed Sparse Row format>




```python
from sklearn.linear_model import LogisticRegression

# Train the model
model = LogisticRegression()
model.fit(X_train_vectorized, y_train)
```




    LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
              intercept_scaling=1, max_iter=100, multi_class='ovr', n_jobs=1,
              penalty='l2', random_state=None, solver='liblinear', tol=0.0001,
              verbose=0, warm_start=False)




```python
from sklearn.metrics import roc_auc_score

# Predict the transformed test documents
predictions = model.predict(vect.transform(X_test))

print('AUC: ', roc_auc_score(y_test, predictions))
```

    AUC:  0.897433277667



```python
# get the feature names as numpy array
feature_names = np.array(vect.get_feature_names())

# Sort the coefficients from the model
sorted_coef_index = model.coef_[0].argsort()

# Find the 10 smallest and 10 largest coefficients
# The 10 largest coefficients are being indexed using [:-11:-1] 
# so the list returned is in order of largest to smallest
print('Smallest Coefs:\n{}\n'.format(feature_names[sorted_coef_index[:10]]))
print('Largest Coefs: \n{}'.format(feature_names[sorted_coef_index[:-11:-1]]))
```

    Smallest Coefs:
    ['worst' 'terrible' 'slow' 'junk' 'poor' 'sucks' 'horrible' 'useless'
     'waste' 'disappointed']
    
    Largest Coefs: 
    ['excelent' 'excelente' 'excellent' 'perfectly' 'love' 'perfect' 'exactly'
     'great' 'best' 'awesome']


# Tfidf


```python
from sklearn.feature_extraction.text import TfidfVectorizer

# Fit the TfidfVectorizer to the training data specifiying a minimum document frequency of 5
vect = TfidfVectorizer(min_df=5).fit(X_train)
len(vect.get_feature_names())
```




    5442




```python
X_train_vectorized = vect.transform(X_train)

model = LogisticRegression()
model.fit(X_train_vectorized, y_train)

predictions = model.predict(vect.transform(X_test))

print('AUC: ', roc_auc_score(y_test, predictions))
```

    AUC:  0.889951006492



```python
feature_names = np.array(vect.get_feature_names())

sorted_tfidf_index = X_train_vectorized.max(0).toarray()[0].argsort()

print('Smallest tfidf:\n{}\n'.format(feature_names[sorted_tfidf_index[:10]]))
print('Largest tfidf: \n{}'.format(feature_names[sorted_tfidf_index[:-11:-1]]))
```

    Smallest tfidf:
    ['61' 'printer' 'approach' 'adjustment' 'consequences' 'length' 'emailing'
     'degrees' 'handsfree' 'chipset']
    
    Largest tfidf: 
    ['unlocked' 'handy' 'useless' 'cheat' 'up' 'original' 'exelent' 'exelente'
     'exellent' 'satisfied']



```python
sorted_coef_index = model.coef_[0].argsort()

print('Smallest Coefs:\n{}\n'.format(feature_names[sorted_coef_index[:10]]))
print('Largest Coefs: \n{}'.format(feature_names[sorted_coef_index[:-11:-1]]))
```

    Smallest Coefs:
    ['not' 'slow' 'disappointed' 'worst' 'terrible' 'never' 'return' 'doesn'
     'horrible' 'waste']
    
    Largest Coefs: 
    ['great' 'love' 'excellent' 'good' 'best' 'perfect' 'price' 'awesome' 'far'
     'perfectly']



```python
# These reviews are treated the same by our current model
print(model.predict(vect.transform(['not an issue, phone is working',
                                    'an issue, phone is not working'])))
```

    [0 0]


# n-grams


```python
# Fit the CountVectorizer to the training data specifiying a minimum 
# document frequency of 5 and extracting 1-grams and 2-grams
vect = CountVectorizer(min_df=5, ngram_range=(1,2)).fit(X_train)

X_train_vectorized = vect.transform(X_train)

len(vect.get_feature_names())
```




    29072




```python
model = LogisticRegression()
model.fit(X_train_vectorized, y_train)

predictions = model.predict(vect.transform(X_test))

print('AUC: ', roc_auc_score(y_test, predictions))
```

    AUC:  0.91106617946



```python
feature_names = np.array(vect.get_feature_names())

sorted_coef_index = model.coef_[0].argsort()

print('Smallest Coefs:\n{}\n'.format(feature_names[sorted_coef_index[:10]]))
print('Largest Coefs: \n{}'.format(feature_names[sorted_coef_index[:-11:-1]]))
```

    Smallest Coefs:
    ['no good' 'junk' 'poor' 'slow' 'worst' 'broken' 'not good' 'terrible'
     'defective' 'horrible']
    
    Largest Coefs: 
    ['excellent' 'excelente' 'excelent' 'perfect' 'great' 'love' 'awesome'
     'no problems' 'good' 'best']



```python
# These reviews are now correctly identified
print(model.predict(vect.transform(['not an issue, phone is working',
                                    'an issue, phone is not working'])))
```

    [1 0]

