
## AI for Medicine Course 1 Week 1 lecture exercises

# Patient Overlap and Data Leakage

Patient overlap in medical data is a part of a more general problem in machine learning called **data leakage**.  To identify patient overlap in this week's graded assignment, you'll check to see if a patient's ID appears in both the training set and the test set. You should also verify that you don't have patient overlap in the training and validation sets, which is what you'll do here.

Below is a simple example showing how you can check for and remove patient overlap in your training and validations sets.


```python
# Import necessary packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
import os
import seaborn as sns
sns.set()
```

### Read in the data from a csv file

First, you'll read in your training and validation datasets from csv files. Run the next two cells to read these csvs into `pandas` dataframes.


```python
# Read csv file containing training data
train_df = pd.read_csv("nih/train-small.csv")
# Print first 5 rows
print(f'There are {train_df.shape[0]} rows and {train_df.shape[1]} columns in the training dataframe')
train_df.head()
```

    There are 1000 rows and 16 columns in the training dataframe





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Image</th>
      <th>Atelectasis</th>
      <th>Cardiomegaly</th>
      <th>Consolidation</th>
      <th>Edema</th>
      <th>Effusion</th>
      <th>Emphysema</th>
      <th>Fibrosis</th>
      <th>Hernia</th>
      <th>Infiltration</th>
      <th>Mass</th>
      <th>Nodule</th>
      <th>PatientId</th>
      <th>Pleural_Thickening</th>
      <th>Pneumonia</th>
      <th>Pneumothorax</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>00008270_015.png</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>8270</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>00029855_001.png</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>29855</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>00001297_000.png</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1297</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>00012359_002.png</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>12359</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>00017951_001.png</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>17951</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Read csv file containing validation data
valid_df = pd.read_csv("nih/valid-small.csv")
# Print first 5 rows
print(f'There are {valid_df.shape[0]} rows and {valid_df.shape[1]} columns in the validation dataframe')
valid_df.head()
```

    There are 109 rows and 16 columns in the validation dataframe





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Image</th>
      <th>Atelectasis</th>
      <th>Cardiomegaly</th>
      <th>Consolidation</th>
      <th>Edema</th>
      <th>Effusion</th>
      <th>Emphysema</th>
      <th>Fibrosis</th>
      <th>Hernia</th>
      <th>Infiltration</th>
      <th>Mass</th>
      <th>Nodule</th>
      <th>PatientId</th>
      <th>Pleural_Thickening</th>
      <th>Pneumonia</th>
      <th>Pneumothorax</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>00027623_007.png</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>27623</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>00028214_000.png</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>28214</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>00022764_014.png</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>22764</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>00020649_001.png</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>20649</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>00022283_023.png</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>22283</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>



### Extract and compare the PatientId columns from the train and validation sets
By running the next four cells you will do the following:
1. Extract patient IDs from the train and validation sets
2. Convert these arrays of numbers into `set()` datatypes for easy comparison
3. Identify patient overlap in the intersection of the two sets


```python
# Extract patient id's for the training set
ids_train = train_df.PatientId.values
# Extract patient id's for the validation set
ids_valid = valid_df.PatientId.values
```


```python
# Create a "set" datastructure of the training set id's to identify unique id's
ids_train_set = set(ids_train)
print(f'There are {len(ids_train_set)} unique Patient IDs in the training set')
# Create a "set" datastructure of the validation set id's to identify unique id's
ids_valid_set = set(ids_valid)
print(f'There are {len(ids_valid_set)} unique Patient IDs in the validation set')
```

    There are 928 unique Patient IDs in the training set
    There are 97 unique Patient IDs in the validation set



```python
# Identify patient overlap by looking at the intersection between the sets
patient_overlap = list(ids_train_set.intersection(ids_valid_set))
n_overlap = len(patient_overlap)
print(f'There are {n_overlap} Patient IDs in both the training and validation sets')
print('')
print(f'These patients are in both the training and validation datasets:')
print(f'{patient_overlap}')
```

    There are 11 Patient IDs in both the training and validation sets
    
    These patients are in both the training and validation datasets:
    [20290, 27618, 9925, 10888, 22764, 19981, 18253, 4461, 28208, 8760, 7482]


### Identify rows (indices) of overlapping patients and remove from either the train or validation set
Run the next two cells to do the following:
1. Create lists of the overlapping row numbers in both the training and validation sets. 
2. Drop the overlapping patient records from the validation set (could also choose to drop from train set)


```python
train_overlap_idxs = []
valid_overlap_idxs = []
for idx in range(n_overlap):
    train_overlap_idxs.extend(train_df.index[train_df['PatientId'] == patient_overlap[idx]].tolist())
    valid_overlap_idxs.extend(valid_df.index[valid_df['PatientId'] == patient_overlap[idx]].tolist())
    
print(f'These are the indices of overlapping patients in the training set: ')
print(f'{train_overlap_idxs}')
print(f'These are the indices of overlapping patients in the validation set: ')
print(f'{valid_overlap_idxs}')
```

    These are the indices of overlapping patients in the training set: 
    [306, 186, 797, 98, 408, 917, 327, 913, 10, 51, 276]
    These are the indices of overlapping patients in the validation set: 
    [104, 88, 65, 13, 2, 41, 56, 70, 26, 75, 20, 52, 55]



```python
# Drop the overlapping rows from the validation set
valid_df.drop(valid_overlap_idxs, inplace=True)
```

### Check that everything worked as planned by rerunning the patient ID comparison between train and validation sets.

When you run the next two cells you should see that there are now fewer records in the validation set and that the overlap problem has been removed!


```python
# Extract patient id's for the validation set
ids_valid = valid_df.PatientId.values
# Create a "set" datastructure of the validation set id's to identify unique id's
ids_valid_set = set(ids_valid)
print(f'There are {len(ids_valid_set)} unique Patient IDs in the validation set')
```

    There are 86 unique Patient IDs in the validation set



```python
# Identify patient overlap by looking at the intersection between the sets
patient_overlap = list(ids_train_set.intersection(ids_valid_set))
n_overlap = len(patient_overlap)
print(f'There are {n_overlap} Patient IDs in both the training and validation sets')
```

    There are 0 Patient IDs in both the training and validation sets


### Congratulations! You removed overlapping patients from the validation set! 

You could have just as well removed them from the training set. 

Always be sure to check for patient overlap in your train, validation and test sets.
