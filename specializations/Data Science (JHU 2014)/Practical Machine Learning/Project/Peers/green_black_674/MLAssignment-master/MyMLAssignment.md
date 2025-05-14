## Loading DataSet
#### Loading Data

```r
pml.training <- read.csv("DataSet/pml-training.csv")
pml.testing <- read.csv("DataSet/pml-testing.csv")
```

#### Defining Columns for selecting from DataSet

```r
MyCols <- c("accel_arm_x", "accel_arm_y", "accel_belt_x", "accel_belt_y", "accel_belt_z", 
    "accel_dumbbell_x", "accel_dumbbell_y", "accel_dumbbell_z", "accel_forearm_z", 
    "gyros_arm_x", "gyros_arm_y", "gyros_belt_x", "gyros_belt_y", "gyros_belt_z", 
    "magnet_arm_x", "magnet_arm_y", "magnet_belt_x", "magnet_belt_y", "magnet_belt_z", 
    "magnet_dumbbell_x", "magnet_dumbbell_y", "magnet_dumbbell_z", "pitch_belt", 
    "roll_belt", "total_accel_belt", "total_accel_dumbbell", "yaw_belt", "yaw_dumbbell", 
    "classe")

MyCols2 <- c("accel_arm_x", "accel_arm_y", "accel_belt_x", "accel_belt_y", "accel_belt_z", 
    "accel_dumbbell_x", "accel_dumbbell_y", "accel_dumbbell_z", "accel_forearm_z", 
    "gyros_arm_x", "gyros_arm_y", "gyros_belt_x", "gyros_belt_y", "gyros_belt_z", 
    "magnet_arm_x", "magnet_arm_y", "magnet_belt_x", "magnet_belt_y", "magnet_belt_z", 
    "magnet_dumbbell_x", "magnet_dumbbell_y", "magnet_dumbbell_z", "pitch_belt", 
    "roll_belt", "total_accel_belt", "total_accel_dumbbell", "yaw_belt", "yaw_dumbbell")
```


We are using following columns from DataSet

```r
pml.training <- pml.training[, MyCols]
pml.testing <- pml.testing[, MyCols2]
```


## Defining training and cross validation dataset

```r
library(caret)
```

```
## Loading required package: lattice
## Loading required package: ggplot2
```

```r
inTrain <- createDataPartition(y = pml.training$classe, p = 0.3, list = FALSE)
myTrain <- pml.training[inTrain, ]

myCV <- pml.training[-inTrain, ]
```


## Training Algorithm

```r
ctrl = trainControl(method = "oob", number = 4)
modFit <- train(classe ~ ., data = myTrain, method = "rf", prox = TRUE, trControl = ctrl, 
    allowParallel = TRUE)
```

```
## Loading required package: randomForest
## randomForest 4.6-7
## Type rfNews() to see new features/changes/bug fixes.
```


## Prediction on 20 set Problems

```r
predict(modFit, pml.testing)
```

```
##  [1] B A B A A E D B A A B C B A E E A B B B
## Levels: A B C D E
```


## Acuracy and Sample Error

```r
myCvPred <- predict(modFit, myCV)
confusionMatrix(myCvPred, myCV$classe)
```

```
## Confusion Matrix and Statistics
## 
##           Reference
## Prediction    A    B    C    D    E
##          A 3878   97   15    7    1
##          B   13 2484   36    1    3
##          C   10   63 2325   79   24
##          D    4   10   19 2162   30
##          E    1    3    0    2 2466
## 
## Overall Statistics
##                                         
##                Accuracy : 0.97          
##                  95% CI : (0.967, 0.972)
##     No Information Rate : 0.284         
##     P-Value [Acc > NIR] : <2e-16        
##                                         
##                   Kappa : 0.961         
##  Mcnemar's Test P-Value : <2e-16        
## 
## Statistics by Class:
## 
##                      Class: A Class: B Class: C Class: D Class: E
## Sensitivity             0.993    0.935    0.971    0.960    0.977
## Specificity             0.988    0.995    0.984    0.995    0.999
## Pos Pred Value          0.970    0.979    0.930    0.972    0.998
## Neg Pred Value          0.997    0.985    0.994    0.992    0.995
## Prevalence              0.284    0.193    0.174    0.164    0.184
## Detection Rate          0.282    0.181    0.169    0.157    0.180
## Detection Prevalence    0.291    0.185    0.182    0.162    0.180
## Balanced Accuracy       0.990    0.965    0.978    0.977    0.988
```

