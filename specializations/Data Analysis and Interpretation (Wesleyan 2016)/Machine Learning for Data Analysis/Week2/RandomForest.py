import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import sklearn.metrics
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from pandas.tools.plotting import scatter_matrix, andrews_curves, radviz

#Load the dataset
GM_data = pd.read_csv("C:\\courses\\Coursera\\Current\\ML\\Week2\\gapminder.csv")
data_clean = GM_data.dropna()

data_clean.dtypes
data_clean.describe()

data_clean.drop('country', 1)
data_clean = data_clean.convert_objects(convert_numeric=True) #.dtypes

data_clean['lifeexpectancy'] = pd.cut(data_clean.lifeexpectancy, bins=[0,60,100])
data_clean = data_clean.dropna(subset = ['lifeexpectancy'])

predictors = data_clean[['incomeperperson','alcconsumption','armedforcesrate','breastcancerper100th','co2emissions','femaleemployrate','hivrate', \
					     'internetuserate','oilperperson','polityscore','relectricperperson','suicideper100th','employrate','urbanrate']]

# fill missing data
predictors = predictors.fillna(predictors.median())

targets = data_clean.lifeexpectancy
pred_train, pred_test, tar_train, tar_test  = train_test_split(predictors, targets, test_size=.4)


#cutoff = np.hstack([np.array(data_clean['lifeexpectancy'][0]), data_clean['lifeexpectancy'].values])
#Split into training and testing sets

#predictors = data_clean[['BIO_SEX','HISPANIC','WHITE','BLACK','NAMERICAN','ASIAN','age',
#'ALCEVR1','ALCPROBS1','marever1','cocever1','inhever1','cigavail','DEP1','ESTEEM1','VIOL1',
#'PASSIST','DEVIANT1','SCHCONN1','GPA1','EXPEL1','FAMCONCT','PARACTV','PARPRES']]

#targets = data_clean.TREG1

pred_train.shape
pred_test.shape
tar_train.shape
tar_test.shape

#Build model on training data
classifier=RandomForestClassifier(n_estimators=25, compute_importances=True)
classifier=classifier.fit(pred_train,tar_train)

# Predict on the test data
predictions=classifier.predict(pred_test)

pd.crosstab(tar_test, predictions, rownames=['Actual'], colnames=['Predicted'])

from collections import OrderedDict
RANDOM_STATE = 123
# NOTE: Setting the `warm_start` construction parameter to `True` disables
# support for paralellised ensembles but is necessary for tracking the OOB
# error trajectory during training.
ensemble_clfs = [
    ("RandomForestClassifier, max_features='sqrt'",
        RandomForestClassifier(oob_score=True,
                               max_features="sqrt",
                               random_state=RANDOM_STATE)),
    ("RandomForestClassifier, max_features='log2'",
        RandomForestClassifier(max_features='log2',
                               oob_score=True,
                               random_state=RANDOM_STATE)),
    ("RandomForestClassifier, max_features=None",
        RandomForestClassifier(max_features=None,
                               oob_score=True,
                               random_state=RANDOM_STATE))
]

# Map a classifier name to a list of (<n_estimators>, <error rate>) pairs.
error_rate = OrderedDict((label, []) for label, _ in ensemble_clfs)

# Range of `n_estimators` values to explore.
min_estimators = 15
max_estimators = 175

for label, clf in ensemble_clfs:
    for i in range(min_estimators, max_estimators + 1):
        clf.set_params(n_estimators=i)
        clf.fit(pred_train,tar_train)

        # Record the OOB error for each `n_estimators=i` setting.
        oob_error = 1 - clf.oob_score_
        error_rate[label].append((i, oob_error))

# Generate the "OOB error rate" vs. "n_estimators" plot.
for label, clf_err in error_rate.items():
    xs, ys = zip(*clf_err)
    plt.plot(xs, ys, label=label)

plt.xlim(min_estimators, max_estimators)
plt.xlabel("n_estimators")
plt.ylabel("OOB error rate")
plt.legend(loc="upper right")
plt.show()

#classifier.get_params()
#for i in range(1, 51):
    #classifier=RandomForestClassifier(n_estimators=i, oob_score=True)
    #classifier.set_params(n_estimators=i, oob_score=True)
    #classifier=classifier.fit(pred_train,tar_train)
    #print i, classifier.oob_score_
    
## pandas visualization

df2 = pd.DataFrame(data_clean, columns=['lifeexpectancy', 'incomeperperson', 'hivrate', 'alcconsumption', 'suicideper100th', 'employrate'])
plt.figure()
df2.hist(alpha=0.5, bins=20)
df2.boxplot()
df2.plot(kind='area'); #, stacked=False);
colors={'(0, 60]':'red','(60, 100]':'green'}
df2.plot(kind='scatter', x='hivrate', y='incomeperperson', color=df2.lifeexpectancy.apply(lambda x:colors[x]));
df2.plot(kind='hexbin', x='age', y='GPA1', gridsize=25)
scatter_matrix(df2, alpha=0.5, figsize=(10, 10), diagonal='hist')
df2 = pd.DataFrame(predictors, columns=['age', 'GPA1', 'FAMCONCT', 'PARACTV', 'ASIAN', 'BIO_SEX', 'VIOL1'])
andrews_curves(df2, 'ASIAN')
radviz(df2, 'ASIAN')
g = sns.FacetGrid(df2, row="BIO_SEX", col="VIOL1", margin_titles=True)
g.map(sns.regplot, "age", "GPA1", order=2)

## variable importance

importances = classifier.feature_importances_
std = np.std([tree.feature_importances_ for tree in classifier.estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]

# Print the feature ranking
print("Feature ranking:")

for f in range(pred_train.shape[1]):
    print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

# Plot the feature importances of the forest
plt.figure()
plt.title("Feature importances")
plt.bar(range(pred_train.shape[1]), importances[indices],
       color="r", yerr=std[indices], align="center")
plt.xticks(range(pred_train.shape[1]), predictors.columns.values[indices])
locs, labels = plt.xticks()
plt.setp(labels, rotation=90)
plt.xlim([-1, pred_train.shape[1]])
plt.show()

sklearn.metrics.confusion_matrix(tar_test,predictions)
sklearn.metrics.accuracy_score(tar_test, predictions)

####



# fit an Extra Trees model to the data
model = ExtraTreesClassifier()
model.fit(pred_train,tar_train)
# display the relative importance of each attribute
print(model.feature_importances_)


"""
Running a different number of trees and see the effect
 of that on the accuracy of the prediction
"""

trees=range(25)
accuracy=np.zeros(25)

for idx in range(len(trees)):
   classifier=RandomForestClassifier(n_estimators=idx + 1)
   classifier=classifier.fit(pred_train,tar_train)
   predictions=classifier.predict(pred_test)
   accuracy[idx]=sklearn.metrics.accuracy_score(tar_test, predictions)
   
plt.cla()
plt.plot(trees, accuracy)


