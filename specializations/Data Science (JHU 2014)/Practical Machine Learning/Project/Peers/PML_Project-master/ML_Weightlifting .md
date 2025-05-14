Machine Learning with Weightlifting Data
========================================================

### Executive Summary

A K nearest neighbors model is fit to wearables data from weightlifting  to predict the classe of the exercises being performed. Cross validation is done to measure the accuracy of the model and PCA is used to reduce the dimensions of the data.


## Loading the data

Load necessary libraries and datasets

```r
library(caret)
```

```
## Loading required package: lattice
## Loading required package: ggplot2
```

```r
pml.training=read.csv("pml-training.csv")
pml.testing=read.csv("pml-testing.csv")
```


## Cleaning the data

All NA variables were removed. Remaining variables were converted to numeric type.


```r
cols1=unlist(lapply(pml.training, 
                   function(x) !any(is.na(x))),use.names=FALSE)

cols2=unlist(lapply(pml.testing, 
                    function(x) !any(is.na(x))),use.names=FALSE)

total.cols=(cols1 & cols2)

pml.training=pml.training[,total.cols]
classe=pml.training$classe

pml.training=data.frame(lapply(pml.training[,-60], 
                               function(x) as.numeric(x)))
pml.training$classe=classe
```

## Cross Validation

I partitioning the training set: 70% training, 30% testing

```r
inTrain=createDataPartition(y=pml.training$classe,p=0.7,list=FALSE)
training=pml.training[inTrain,]
testing=pml.training[-inTrain,]
```

## Preprocessing

PCA was used to reduce the dimensions while keeping 99% of the variance.


```r
preProc=preProcess(training[,-60],method="pca",thresh=.99)
pca.train=predict(preProc,training[,-60])
```



## Fitting a model
K nearest neighbors. A KNN model was fitted on the training partition.


```r
modelFit=train(training$classe~., method="knn",data=pca.train)
pca.test=predict(preProc,testing[,-60])
pred=predict(modelFit,pca.test)
```


## Error rate

Out of sample Error

```r
1-confusionMatrix(pred,testing$classe)$overall[[1]]
```

```
## [1] 0.03093
```

The lower error rate indicates that the model will fit the testing data well. However, the error rate will most likely be higher on the testing data, due to an overfitting of the data.




## Full Model

Another knn model was fit to the entire training set to include the 30% originally used for cross validation.

```r
preproc.full=preProcess(pml.training[,-60],method="pca",thresh=.99)
pca.full=predict(preproc.full,pml.training[,-60])
modelfit.full=train(pml.training$classe~., method="knn",data=pca.full)
```


## Preprocessing the testing data

```r
pml.testing=pml.testing[,total.cols]
pml.testing=data.frame(lapply(pml.testing[,-60], 
                               function(x) as.numeric(x)))

pca.final=predict(preproc.full,pml.testing)
pred.final=predict(modelfit.full,pca.final)

pred.final
```

```
##  [1] B A A A A C D B A A B A B A E E A B B B
## Levels: A B C D E
```

## Conclusion
17 out of the 20 predictions are correct. This model does fairly well at predicting the classe.  





