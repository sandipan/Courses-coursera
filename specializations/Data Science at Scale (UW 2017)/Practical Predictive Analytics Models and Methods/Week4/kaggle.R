setwd("C:/courses/Coursera/Past/Specialization-UW Data Science at Scale/Practical Predictive Analytics Models and Methods/Week4")

library(dplyr)
library(caret)

process.dates <- function(data) {
  index <- which(names(data)=='Date')
  dates <- do.call(rbind, strsplit(data$Date, '-'))
  dates <- as.data.frame(dates, stringsAsFactors=FALSE)
  names(dates) <- c('year', 'month', 'day')
  dates <- as.data.frame(sapply(dates, function(x) as.integer(x)))
  data$year <- dates$year
  data$month <- dates$month
  data$day <- dates$day
  return(data[,-index])
}

character.to.factor <- function(df) {
  df[sapply(df, is.character)] <- lapply(df[sapply(df, is.character)], as.factor) # character to factor
  print(sapply(df, class))
  return(df)
}

train <- read.csv("train.csv", stringsAsFactors=FALSE)
train <- process.dates(train)
train <- train[,-which(names(train) == 'Customers')]
train <- train %>% filter(Open == 1)
train <- train[,-which(names(train)=='Open')]

months <- c('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec')
stores <- read.csv("store.csv", stringsAsFactors=FALSE)

#stores$promo.startednew <- as.integer(grepl(months[train$month], stores$PromoInterval))

#stores$promo.Jan <- as.integer(grepl('Jan', stores$PromoInterval))
#stores$promo.Feb <- as.integer(grepl('Feb', stores$PromoInterval))
#stores$promo.Mar <- as.integer(grepl('Mar', stores$PromoInterval))
#stores$promo.Apr <- as.integer(grepl('Apr', stores$PromoInterval))
#stores$promo.May <- as.integer(grepl('May', stores$PromoInterval))
#stores$promo.Jun <- as.integer(grepl('Jun', stores$PromoInterval))
#stores$promo.Jul <- as.integer(grepl('Jul', stores$PromoInterval))
#stores$promo.Aug <- as.integer(grepl('Aug', stores$PromoInterval))
#stores$promo.Sept <- as.integer(grepl('Sept', stores$PromoInterval))
#stores$promo.Oct <- as.integer(grepl('Oct', stores$PromoInterval))
#stores$promo.Nov <- as.integer(grepl('Nov', stores$PromoInterval))
#stores$promo.Dec <- as.integer(grepl('Dec', stores$PromoInterval))
#stores <- stores[,-(which(names(stores)=='PromoInterval'))]
stores[is.na(stores)] <- 0

train.store <- merge(train, stores, by.x='Store', by.y='Store')

index.month <- which(names(train.store)=='month')
index.promoint <- which(names(train.store)=='PromoInterval')
train.store$Promo.startednew <- as.integer(apply(train.store, 1, function(x) {grepl(months[as.integer(x[index.month])], x[index.promoint])}))
train.store <- train.store[,-(which(names(train.store)=='PromoInterval'))]
compOpenTotalMonth <- 12*train.store$CompetitionOpenSinceYear - train.store$CompetitionOpenSinceMonth
train.store$CompetitionOpenTotalMonth <- 0
train.store$CompetitionOpenTotalMonth[compOpenTotalMonth != 0] <- 12*train.store[compOpenTotalMonth != 0,]$year + train.store[compOpenTotalMonth != 0,]$month - compOpenTotalMonth[compOpenTotalMonth != 0]
train.store <- train.store[,-which(names(train.store) %in% c('CompetitionOpenSinceMonth', 'CompetitionOpenSinceYear'))]
train.store <- character.to.factor(train.store)

test <- read.csv("test.csv", stringsAsFactors=FALSE)  

test <- process.dates(test)
test.ids <- test[,1]
test <- test[,-1]

library(mice)
imp <- mice(test, m=10)
print(imp)
test <- complete(imp)

test.ids.open <- test.ids[test$Open == 1]
test.ids.closed <- setdiff(test.ids, test.ids.open)

test <- test %>% filter(Open == 1)
test <- test[,-which(names(test)=='Open')]

test.store <- merge(test, stores, by.x='Store', by.y='Store')
index.month <- which(names(test.store)=='month')
index.promoint <- which(names(test.store)=='PromoInterval')
test.store$Promo.startednew <- as.integer(apply(test.store, 1, function(x) {grepl(months[as.integer(x[index.month])], x[index.promoint])}))
test.stores <- test.store[,-(which(names(test.store)=='PromoInterval'))]
compOpenTotalMonth <- 12*test.store$CompetitionOpenSinceYear - test.store$CompetitionOpenSinceMonth
test.store$CompetitionOpenTotalMonth <- 0
test.store$CompetitionOpenTotalMonth[compOpenTotalMonth != 0] <- 12*test.store[compOpenTotalMonth != 0,]$year + test.store[compOpenTotalMonth != 0,]$month - compOpenTotalMonth[compOpenTotalMonth != 0]
test.store <- test.store[,-which(names(test.store) %in% c('CompetitionOpenSinceMonth', 'CompetitionOpenSinceYear'))]
test.store <- character.to.factor(test.store)

train_stores <- sort(unique(train$Store))
test_stores <- sort(unique(test$Store))
length(train_stores)
length(test_stores)
all(test_stores %in% train_stores)
train_counts <- train %>% group_by(Store) %>% summarise(count=n())
summary(train_counts$count)

pred <- data.frame(Id=test.ids.closed, Sales=0)

#train.store <- train.store %>% filter(Store %in% test_stores)

for (store in test_stores) {
  
  train_sub <- train.store %>% filter(Store == store)
  split <- createDataPartition(train_sub$Sales, p = 3/4)[[1]]
  train1 <- train_sub[split,]
  valid1 <- train_sub[-split,]  
  print(store)
  print(nrow(train1))
  print(100 * nrow(train1) / nrow(train_sub))

  rfFit <- train(Sales ~ ., data=train1, method="rf")
  pyrf <- predict(rfFit, newdata=valid1)
  rmse <- sqrt(mean((valid1$Sales - pyrf)^2))
  print(rmse)
  mape <- mean(abs(2*(valid1$Sales - pyrf)/(valid1$Sales + pyrf)))
  print(mape)
  
  indices <- which(test.store$Store == store)
  test_sub <- test.store[indices,]
  pyrf <- predict(rfFit, newdata=test_sub)
  pred <- rbind(pred, data.frame(Id=test.ids.open[indices], Sales=pyrf))  
}
pred <- pred[order(pred$Id),]
write.csv(pred, 'pred.csv', row.names=FALSE)

pred <- data.frame(Id=test.ids.closed, Sales=0)
for (store in test_stores) {
  
  train_sub <- train.store %>% filter(Store == store)
  split <- createDataPartition(train_sub$Sales, p = 3/4)[[1]]
  train1 <- train_sub[split,]
  valid1 <- train_sub[-split,]  
  print(store)
  print(nrow(train1))
  print(100 * nrow(train1) / nrow(train_sub))
  
  rfFit <- train(Sales ~ .-Store, data=train1, method="glmnet") #method="svmRadial")
  pyrf <- predict(rfFit, newdata=valid1)
  rmse <- sqrt(mean((valid1$Sales - pyrf)^2))
  print(rmse)
  mape <- mean(abs(2*(valid1$Sales - pyrf)/(valid1$Sales + pyrf)))
  print(mape)
  
  indices <- which(test.store$Store == store)
  test_sub <- test.store[indices,]
  pyrf <- predict(rfFit, newdata=test_sub)
  pred <- rbind(pred, data.frame(Id=test.ids.open[indices], Sales=pyrf))  
}
pred <- pred[order(pred$Id),]
write.csv(pred, 'pred3.csv', row.names=FALSE)

#train.store$CompetitionOpenSinceYear[train.store$CompetitionOpenSinceYear> 0] <- train.store$year - train.store$CompetitionOpenSinceYear[train.store$CompetitionOpenSinceYear> 0]
#train.store$Promo2SinceYear[train.store$Promo2SinceYear> 0] <- train.store$year - train.store$Promo2SinceYear[train.store$Promo2SinceYear> 0]

train.store$Store <- as.factor(as.character(train.store$Store))
train.store$DayOfWeek <- as.factor(as.character(train.store$DayOfWeek))
split <- createDataPartition(train.store$Sales, p = 3/4)[[1]]

train1 <- train.store[split,]
valid1 <- train.store[-split,]  
print(nrow(train1))
print(100 * nrow(train1) / nrow(train.store))
glmFit <- train(Sales ~ ., data=train1, method="glmnet")
pyglm <- predict(glmFit, newdata=valid1)

rmse <- sqrt(mean((valid1$Sales - pyglm)^2))
print(rmse)
mape <- mean(abs(2*(valid1$Sales - pyglm)/(valid1$Sales + pyglm)))
mape

pyglm <- predict(glmFit, newdata=test.store)

pred <- pred[order(pred$Id),]
write.csv(pred, 'pred1.1.csv', row.names=FALSE)


knnFit <- train(Sales ~ ., data=train1, method="knn")
rpartFit <- train(Sales ~ ., data=train1, method="rpart")
glmFit <- train(Sales ~ ., data=train1, method="glmnet")
enetFit <- train(Sales ~ ., data=train1, method="enet")
rfFit <- train(Sales ~ ., data=train1, method="rf")
svmFit <- train(Sales ~ ., data=train1, method="svmRadial", trControl = trainControl(method = "cv", savePredictions=TRUE))
gbmFit <- train(Sales ~ ., data=train1, method="gbm")

pyrpart <- predict(rpartFit, newdata=valid1)
pyknn <- predict(knnFit, newdata=valid1)
pysvm <- predict(svmFit, newdata=valid1)
pygbm <- predict(gbmFit, newdata=valid1)
pyglm <- predict(glmFit, newdata=valid1)

rmse <- sqrt(mean((valid1$Sales - pyglm)^2))
print(rmse)
#mape <- mean(abs(2*(valid1$Sales - pyglm)/(valid1$Sales + pyglm)))
#mape

pyglm <- predict(glmFit, newdata=test.store)

pred <- pred[order(pred$Id),]
write.csv(pred, 'pred.csv', row.names=FALSE)

confusionMatrix(data = pyrf, valid1$Sales)
confusionMatrix(data = pygbm, valid1$Sales)
confusionMatrix(data = pysvm, valid1$Sales)
confusionMatrix(data = pyglm, valid1$Sales)

plot(pyglm, valid1$Sales, col=abs(pyglm-valid1$Sales))
pdf <- data.frame(Predicted=pyglm, Actual=valid1$Sales)
pdf$Diff=abs(pdf$Predicted-pdf$Actual)
ggplot(pdf, aes(Predicted, Actual, color=Diff)) + geom_point(size=2) +     
  scale_color_gradient2(low = "green", mid = "yellow", high = "red")

ggplot(pdf, aes(x=Diff)) + geom_histogram(binwidth=1, aes(fill=..count..)) +     
  scale_fill_gradient(low = "red", high = "green")



predDF <- data.frame(pyrf, pysvm, Cover_Type=valid1$Cover_Type)
combRFFit <- train(as.factor(Cover_Type) ~ ., data=predDF, method="rf")
combDF <- predict(combRFFit, predDF)
#confusionMatrix(data = pylda, valid1$Cover_Type)
#confusionMatrix(data = pyknn, valid1$Cover_Type)
#confusionMatrix(data = pyada, valid1$Cover_Type)
confusionMatrix(data = combDF, valid1$Cover_Type)





train <- as.data.frame(cbind(train[1:10], 
                             Wilderness_Area = apply(train[,11:14], 1, which.max), 
                             Soil_Type = apply(train[,15:54], 1, which.max), 
                             Cover_Type=train[,55]))

test <- as.data.frame(cbind(test[1:10], 
                            Wilderness_Area = apply(test[,11:14], 1, which.max), 
                            Soil_Type = apply(test[,15:54], 1, which.max)))



#vars <- c("Elevation", "Aspect", "Slope", "Horizontal_Distance_To_Hydrology",
#"Vertical_Distance_To_Hydrology", "Horizontal_Distance_To_Roadways",
#"Hillshade_9am", "Hillshade_Noon", "Hillshade_3pm", 
#"Horizontal_Distance_To_Fire_Points", "Wilderness_Area1", "Wilderness_Area2",
#"Wilderness_Area3", "Wilderness_Area4")

#head(train[vars])
#length(vars)
#head(train[,15:54])

ntrain <- nrow(train)
ntest <- nrow(test)

train1 <- NULL
for (i in 1:(length(unique(train$Cover_Type)))) {
  ctrain <- train[train$Cover_Type == i, ]
  train1 <- rbind(train1, ctrain[sample(1:(nrow(ctrain)), 500),])
}

train <- train1

split <- createDataPartition(train$Cover_Type, p = 3/4)[[1]]
train1 <- train[split,]
valid1 <- train[-split,]  
100 * nrow(train1) / nrow(train)	

#set.seed(62433)
rfFit <- train(as.factor(Cover_Type) ~ ., data=train1, method="rf")
#gbmFit <- train(as.factor(Cover_Type) ~ ., data=train1, "gbm", verbose=FALSE)
svmFit <- train(as.factor(Cover_Type) ~ ., data=train1, "svmRadial")
#ldaFit <- train(as.factor(Cover_Type) ~ ., data=train1, "lda")
#knnFit <- train(as.factor(Cover_Type) ~ ., data=train1, "knn")
#adaFit <- train(as.factor(Cover_Type) ~ ., data=train1, "ada")
pyrf <- predict(rfFit, newdata=valid1)
#pygbm <- predict(gbmFit, newdata=valid1)
pysvm <- predict(svmFit, newdata=valid1)
#pylda <- predict(ldaFit, newdata=valid1)
#pyknn <- predict(knnFit, newdata=valid1)
#pyada <- predict(adaFit, newdata=valid1)
predDF <- data.frame(pyrf, pysvm, Cover_Type=valid1$Cover_Type)
combRFFit <- train(as.factor(Cover_Type) ~ ., data=predDF, method="rf")
combDF <- predict(combRFFit, predDF)
confusionMatrix(data = pyrf, valid1$Cover_Type)
#confusionMatrix(data = pygbm, valid1$Cover_Type)
confusionMatrix(data = pysvm, valid1$Cover_Type)
#confusionMatrix(data = pylda, valid1$Cover_Type)
#confusionMatrix(data = pyknn, valid1$Cover_Type)
#confusionMatrix(data = pyada, valid1$Cover_Type)
confusionMatrix(data = combDF, valid1$Cover_Type)

rfFit <- train(as.factor(Cover_Type) ~ ., data=train, method="rf", 
               trControl = trainControl(method = "cv", classProbs=TRUE, savePredictions=TRUE))
gbmFit <- train(as.factor(Cover_Type) ~ ., data=train, "gbm", 
                trControl = trainControl(method = "cv", classProbs=TRUE, savePredictions=TRUE))
svmFit <- train(as.factor(Cover_Type) ~ ., data=train, "svmRadial", 
                trControl = trainControl(method = "cv", savePredictions=TRUE))
#ldaFit <- train(as.factor(Cover_Type) ~ ., data=train, "lda", 
#                trControl = trainControl(method = "cv", savePredictions=TRUE))
pyrf <- predict(rfFit)
pygbm <- predict(gbmFit)
pysvm <- predict(svmFit)
#pylda <- predict(ldaFit)
predDF <- data.frame(pyrf, pygbm, pysvm, Cover_Type=train$Cover_Type)
combRFFit <- train(as.factor(Cover_Type) ~ ., data=predDF, method="rf", 
                   trControl = trainControl(method = "cv", savePredictions=TRUE))

all.models <- list(rfFit, gbmFit, svmFit)
greedy <- caretEnsemble(all.models, iter=1000L)
sort(greedy$weights, decreasing=TRUE)
greedy$error

linear <- caretStack(all.models, method='glm', trControl=trainControl(method='cv', savePredictions=TRUE))
linear$error

tpyrf <- predict(rfFit, newdata=test)
tpygbm <- predict(gbmFit, newdata=test)
tpysvm <- predict(svmFit, newdata=test)
#tpylda <- predict(ldaFit, newdata=test)
tpredDF <- data.frame(tpyrf, tpygbm, tpysvm)
combDF <- predict(combRFFit, newdata=tpredDF)

#testout <- data.frame(Id=test.id, Cover_Type=as.integer(tpygbm == tpygbm))
testout <- data.frame(Id=test.id, Cover_Type=tpyrf)
write.csv(testout, "testout.csv", row.names=FALSE)






#### step
LOGm <- glm(as.factor(Cover_Type) ~ ., data=train, family='binomial')
RLOGm <- step(LOGm)
predicted.Cover_Type <- predict(RLOGm, newdata=valid1, type="response")
computeAccuracy(valid1, predicted.Cover_Type, valid1$Cover_Type, threshold)
combined <- combined[names(RLOGm$coefficients)[-1]]

ind = which(predicted.Cover_TypeRF < predicted.Cover_TypeSVM)
pred = predicted.Cover_TypeRF
pred[ind] <- predicted.Cover_TypeSVM[ind]
computeAccuracy(valid1, pred, valid1$Cover_Type, threshold)
computeAccuracy(valid1, apply(rbind(predicted.Cover_TypeRF, predicted.Cover_TypeADA, predicted.Cover_TypeSVM), 2, median), valid1$Cover_Type, threshold)
computeAccuracy(valid1, apply(rbind(predicted.Cover_TypeRF, predicted.Cover_TypeADA, predicted.Cover_TypeSVM), 2, mean), valid1$Cover_Type, threshold)
computeAccuracy(valid1, apply(rbind(predicted.Cover_TypeRF, predicted.Cover_TypeLOG, predicted.Cover_TypeSVM), 2, mean), valid1$Cover_Type, threshold)
computeAccuracy(valid1, apply(rbind(predicted.Cover_TypeRF, predicted.Cover_TypeLOG, predicted.Cover_TypeSVM), 2, median), valid1$Cover_Type, threshold)
computeAccuracy(valid1, apply(rbind(predicted.Cover_TypeRF, predicted.Cover_TypeLOG, predicted.Cover_TypeSVM, predicted.Cover_TypeADA, predicted.Cover_TypeNB), 2, median), valid1$Cover_Type, threshold)
computeAccuracy(valid1, apply(rbind(predicted.Cover_TypeRF, predicted.Cover_TypeLOG, predicted.Cover_TypeSVM, predicted.Cover_TypeADA, predicted.Cover_TypeNB), 2, mean), valid1$Cover_Type, threshold)
computeAccuracy(valid1, apply(rbind(predicted.Cover_TypeRF, predicted.Cover_TypeLOG, predicted.Cover_TypeADA), 2, mean), valid1$Cover_Type, threshold)

# maxauc 0.6863462

#for (k in seq(0.35, 0.45, 0.01)) {
for (k in seq(0.1, 0.9, 0.05)) {
  print(k)
  computeAccuracy(valid1, (k*predicted.Cover_TypeRF + (1-k)*predicted.Cover_TypeLOG), valid1$Cover_Type, threshold)
}
for (k in seq(0.1, 0.9, 0.05)) {
  print(k)
  computeAccuracy(valid1, (k*predicted.Cover_TypeRF + (1-k)*predicted.Cover_TypeSVM), valid1$Cover_Type, threshold)
}
for (k in seq(0.1, 0.9, 0.05)) {
  print(k)
  computeAccuracy(valid1, (k*predicted.Cover_TypeLOG + (1-k)*predicted.Cover_TypeSVM), valid1$Cover_Type, threshold)
}
for (k in seq(0.1, 0.9, 0.05)) {
  for (l in seq(0.1, 0.9, 0.05)) {
    print(paste(k,l))
    computeAccuracy(valid1, (k*predicted.Cover_TypeLOG + l*predicted.Cover_TypeSVM + (1-k-l)*predicted.Cover_TypeRF), valid1$Cover_Type, threshold)
  }
}
maxklm <- ''
maxauc <- 0
for (k in seq(0.1, 0.9, 0.1)) {
  for (l in seq(0.1, 0.9, 0.1)) {
    for (m in seq(0.1, 0.9, 0.1)) {
      auc <- getAUC(valid1, (k*predicted.Cover_TypeLOG + l*predicted.Cover_TypeSVM + m*predicted.Cover_TypeRF + (1-k-l-m)*predicted.Cover_TypeADA), valid1$Cover_Type, threshold)
      if (maxauc < auc & k+l+m <= 1) {
        maxauc <- auc
        maxklm <- paste(k,l,m)
      }
      #computeAccuracy(valid1, (k*predicted.Cover_TypeLOG + l*predicted.Cover_TypeSVM + m*predicted.Cover_TypeRF + (1-k-l-m)*predicted.Cover_TypeADA), valid1$Cover_Type, threshold)
    }
  }
}

computeAccuracy(valid1, (0.3*predicted.Cover_TypeLOG + 0.1*predicted.Cover_TypeSVM + 0.2*predicted.Cover_TypeRF + 0.4*predicted.Cover_TypeADA), valid1$Cover_Type, threshold) ####
computeAccuracy(valid1, (0.1*predicted.Cover_TypeLOG + 0.35*predicted.Cover_TypeSVM + 0.55*predicted.Cover_TypeRF), valid1$Cover_Type, threshold) #### 6893, 16
computeAccuracy(valid1, (0.8*predicted.Cover_TypeRF + predicted.Cover_TypeLOG) / 2, valid1$Cover_Type, threshold)
computeAccuracy(valid1, (0.4*predicted.Cover_TypeRF + 0.6*predicted.Cover_TypeLOG), valid1$Cover_Type, threshold)

predicted.Cover_TypeLOG <- classify(train, train, threshold, "classifyLOG")
predicted.Cover_TypeRF <- classify(train, train, threshold, "classifyRF")
predicted.Cover_TypeSVM <- classify(train, train, threshold, "classifySVM")
computeAccuracy(train, (0.1*predicted.Cover_TypeLOG + 0.35*predicted.Cover_TypeSVM + 0.55*predicted.Cover_TypeRF), train$Cover_Type, threshold)
predicted.Cover_TypeLOG <- classify(train, test, threshold, "classifyLOG", FALSE)
predicted.Cover_TypeRF <- classify(train, test, threshold, "classifyRF", FALSE)
predicted.Cover_TypeSVM <- classify(train, test, threshold, "classifySVM", FALSE)
#testout <- data.frame(UserID=test.id, Probability1=(0.4*predicted.Cover_TypeRF + 0.6*predicted.Cover_TypeLOG))
testout <- data.frame(UserID=test.id, Probability1=(0.1*predicted.Cover_TypeLOG + 0.35*predicted.Cover_TypeSVM + 0.55*predicted.Cover_TypeRF))
write.csv(testout, "testout.csv", row.names=FALSE)

computeAccuracy(valid1, (predicted.Cover_TypeRF + predicted.Cover_TypeLOG) / 2, valid1$Cover_Type, threshold)
computeAccuracy(valid1, (predicted.Cover_TypeRF + predicted.Cover_TypeSVM) / 2, valid1$Cover_Type, threshold)
computeAccuracy(valid1, (predicted.Cover_TypeRF + predicted.Cover_TypeADA) / 2, valid1$Cover_Type, threshold)
computeAccuracy(valid1, (predicted.Cover_TypeRF + predicted.Cover_TypeADA + predicted.Cover_TypeSVM) / 3, valid1$Cover_Type, threshold)

predicted.Cover_TypeRF <- classify(train, train, threshold, "classifyRF")
predicted.Cover_TypeLOG <- classify(train, train, threshold, "classifyLOG")
predicted.Cover_TypeSVM <- classify(train, train, threshold, "classifySVM")
#computeAccuracy(train, (predicted.Cover_TypeRF + predicted.Cover_TypeLOG) / 2, train$Cover_Type, threshold)
computeAccuracy(train, (0.1*predicted.Cover_TypeLOG + 0.35*predicted.Cover_TypeSVM + 0.55*predicted.Cover_TypeRF), train$Cover_Type, threshold)
predicted.Cover_TypeRF <- classify(train, test, threshold, "classifyRF", FALSE)
predicted.Cover_TypeLOG <- classify(train, test, threshold, "classifyLOG", FALSE)
predicted.Cover_TypeSVM <- classify(train, test, threshold, "classifySVM", FALSE)
#computeAccuracy(valid1, (0.8*predicted.Cover_TypeRF + predicted.Cover_TypeLOG) / 2, valid1$Cover_Type, threshold)
#testout <- data.frame(UserID=test.id, Probability1=(predicted.Cover_TypeRF + predicted.Cover_TypeLOG) / 2)
testout <- data.frame(UserID=test.id, Probability1=(0.1*predicted.Cover_TypeLOG + 0.35*predicted.Cover_TypeSVM + 0.55*predicted.Cover_TypeRF))
write.csv(testout, "testout.csv", row.names=FALSE)

predicted.Cover_TypeRF <- classifyWithClustering(train1, valid1, k, threshold, "classifySVM")

threshold <- 0.5
KNN1 <- train(Cover_Type ~ ., data = train1, method = "knn", trControl = trainControl(method = "cv"))
predicted.Cover_TypeKNN <- predict(KNN1, newdata = train1, type = "raw")
computeAccuracy(train1, predicted.Cover_TypeKNN, train1$Cover_Type, threshold)
predicted.Cover_TypeKNN <- predict(KNN1, newdata = valid1, type = "raw")
computeAccuracy(valid1, predicted.Cover_TypeKNN, valid1$Cover_Type, threshold)

RFm1 <- train(as.factor(Cover_Type) ~ ., data = train1, method = "rf", trControl = trainControl(method = "cv"))
predicted.Cover_TypeRF <- predict(RFm1, newdata = valid1, type = "raw")
computeAccuracy(train1, predicted.Cover_TypeRF, valid1$Cover_Type, threshold)
GBMm1 <- train(as.factor(Cover_Type) ~ ., data = train, method = "gbm", trControl = trainControl(method = "cv"))
predicted.Cover_TypeGBM <- predict(GBMm1, newdata = NULL, type = "raw")
computeAccuracy(train1, predicted.Cover_TypeGBM, train1$Cover_Type, threshold)


predict(knnFit, newdata = test, type = "raw")





RFm1 <- randomForest(as.factor(Cover_Type) ~ ., data = train1, type="classification")
SVMm1 <- svm(as.factor(Cover_Type) ~ ., data = train1, type="C-classification", probability=TRUE)
ADAm1 <- ada(as.factor(Cover_Type) ~ ., data = train1)
LOGm1 <- glm(as.factor(Cover_Type) ~ ., data=train1, family='binomial')
#RLOGm1 <- glmnet(train1[-83], as.factor(train1$Cover_Type), family='binomial')
NBm1 <- naiveBayes(as.factor(Cover_Type) ~ ., data = train1, type="raw")
GBMm1 <- gbm(as.factor(Cover_Type) ~ ., data=train1, dist="adaboost", n.tree = 500, shrinkage = 1)


#NNm1 <- nnet(as.factor(Cover_Type) ~ ., data = train1, size=10)
#SLOGm1 <- step(LOGm1)
#CARTm1 <- rpart(as.factor(Cover_Type) ~ ., data=train1, method="class")
predicted.Cover_TypeRF <- predict(RFm1, type="prob")
predicted.Cover_TypeSVM <- predict(SVMm1, train1, decision.values = TRUE, probability=TRUE)
predicted.Cover_TypeNB <- predict(NBm1, train1, type="raw")
predicted.Cover_TypeADA <- predict(ADAm1, newdata=train1, type="prob")
predicted.Cover_TypeLOG <- predict(LOGm1, newdata=train1, type="response")
predicted.Cover_TypeRLOG <- predict(LOGm1, newdata=train1, type="response")
#gbm.perf(GBMm1)
#confusion(predict(fit.gbm1, test.data2, n.trees = gbm.perf(GBMm1)) > 0, test.data2$y > 0)
predicted.Cover_TypeGBM <- predict(GBMm1, newdata=valid1, n.trees = gbm.perf(GBMm1), type="response")
#predicted.Cover_TypeNN <- predict(NNm1, newdata=train1, type="raw")
computeAccuracy(train1, predicted.Cover_TypeRF[,2], train1$Cover_Type, threshold)
computeAccuracy(train1, attr(predicted.Cover_TypeSVM, "probabilities")[,1], train1$Cover_Type, threshold)
computeAccuracy(train1, predicted.Cover_TypeNB[,2], train1$Cover_Type, threshold)
#computeAccuracy(train1, predicted.Cover_TypeNN, train1$Cover_Type, threshold)
computeAccuracy(train1, predicted.Cover_TypeADA[,2], train1$Cover_Type, threshold)
computeAccuracy(train1, predicted.Cover_TypeLOG, train1$Cover_Type, threshold)
computeAccuracy(train1, (predicted.Cover_TypeRF[,2] + attr(predicted.Cover_TypeSVM, "probabilities")[,1]) / 2, train1$Cover_Type, threshold)
computeAccuracy(train1, (predicted.Cover_TypeRF[,2] + predicted.Cover_TypeADA[,2]) / 2, train1$Cover_Type, threshold)
computeAccuracy(train1, (predicted.Cover_TypeRF[,2] + predicted.Cover_TypeADA[,2] + attr(predicted.Cover_TypeSVM, "probabilities")[,1]) / 3, train1$Cover_Type, threshold)
predicted.Cover_TypeRF <- predict(RFm1, newdata=valid1, type="prob")
predicted.Cover_TypeSVM <- predict(SVMm1, newdata=valid1, decision.values = TRUE, probability=TRUE)
predicted.Cover_TypeNB <- predict(NBm1, newdata=valid1,type="raw")
predicted.Cover_TypeADA <- predict(ADAm1, newdata=valid1, type="prob")
predicted.Cover_TypeLOG <- predict(LOGm1, newdata=valid1, type='response')
rdf <- as.data.frame(cbind(predicted.Cover_TypeRF[,2],attr(predicted.Cover_TypeSVM, "probabilities")[,1],predicted.Cover_TypeLOG,predicted.Cover_TypeNB[,2], predicted.Cover_TypeADA[,2], valid1$Cover_Type))
names(rdf) <- c("rf", "svm", "log", "nb", "ada", "Cover_Type")
write.csv(rdf, "out.csv")
#predicted.Cover_TypeNN <- predict(NNm1, newdata=valid1, type="raw")
#predicted.Cover_TypeSLOG <- predict(SLOGm1, newdata=valid1, type='response')
#predicted.Cover_TypeCART <- predict(CARTm1, newdata=valid1, type="prob")
computeAccuracy(valid1, predicted.Cover_TypeRF[,2], valid1$Cover_Type, threshold)
computeAccuracy(valid1, attr(predicted.Cover_TypeSVM, "probabilities")[,1], valid1$Cover_Type, threshold)
computeAccuracy(valid1, predicted.Cover_TypeNB[,2], valid1$Cover_Type, threshold)
computeAccuracy(valid1, predicted.Cover_TypeADA[,2], valid1$Cover_Type, threshold)
computeAccuracy(valid1, predicted.Cover_TypeLOG, valid1$Cover_Type, threshold)
#computeAccuracy(valid1, predicted.Cover_TypeNN, valid1$Cover_Type, threshold)
#computeAccuracy(valid1, predicted.Cover_TypeSLOG, valid1$Cover_Type, threshold)
computeAccuracy(valid1, (predicted.Cover_TypeRF[,2] + attr(predicted.Cover_TypeSVM, "probabilities")[,1]) / 2, valid1$Cover_Type, threshold)
computeAccuracy(valid1, (predicted.Cover_TypeADA[,2] + attr(predicted.Cover_TypeSVM, "probabilities")[,1]) / 2, valid1$Cover_Type, threshold)
#computeAccuracy(valid1, (predicted.Cover_TypeLOG + predicted.Cover_TypeADA[,2] + attr(predicted.Cover_TypeSVM, "probabilities")[,1]) / 3, valid1$Cover_Type, threshold)
computeAccuracy(valid1, (predicted.Cover_TypeRF[,2] + predicted.Cover_TypeADA[,2]) / 2, valid1$Cover_Type, threshold)
computeAccuracy(valid1, (predicted.Cover_TypeRF[,2] + predicted.Cover_TypeLOG) / 2, valid1$Cover_Type, threshold)
computeAccuracy(valid1, (predicted.Cover_TypeNB[,2] + predicted.Cover_TypeLOG) / 2, valid1$Cover_Type, threshold)
#computeAccuracy(valid1, (predicted.Cover_TypeRF[,2] + predicted.Cover_TypeSLOG) / 2, valid1$Cover_Type, threshold)
computeAccuracy(valid1, (predicted.Cover_TypeRF[,2] + predicted.Cover_TypeADA[,2] + attr(predicted.Cover_TypeSVM, "probabilities")[,1]) / 3, valid1$Cover_Type, threshold)
computeAccuracy(valid1, (predicted.Cover_TypeRF[,2] + predicted.Cover_TypeADA[,2] + attr(predicted.Cover_TypeSVM, "probabilities")[,1] + predicted.Cover_TypeLOG) / 4, valid1$Cover_Type, threshold)
computeAccuracy(valid1, (predicted.Cover_TypeRF[,2] + attr(predicted.Cover_TypeSVM, "probabilities")[,1] + predicted.Cover_TypeLOG) / 3, valid1$Cover_Type, threshold)
#computeAccuracy(valid1, predicted.Cover_TypeCART[,2], valid1$Cover_Type, threshold)
#computeAccuracy(valid1, (predicted.Cover_TypeRF[,2] + predicted.Cover_TypeADA[,2] + attr(predicted.Cover_TypeSVM, "probabilities")[,1] + predicted.Cover_TypeLOG + predicted.Cover_TypeCART[,2]) / 5, valid1$Cover_Type, threshold)
#computeAccuracy(valid1, (predicted.Cover_TypeRF[,2] + predicted.Cover_TypeADA[,2] + attr(predicted.Cover_TypeSVM, "probabilities")[,1] + predicted.Cover_TypeSLOG) / 4, valid1$Cover_Type, threshold)
#computeAccuracy(valid1, (predicted.Cover_TypeRF[,2] + predicted.Cover_TypeADA[,2] + predicted.Cover_TypeNB[,2] + attr(predicted.Cover_TypeSVM, "probabilities")[,1] + predicted.Cover_TypeLOG) / 5, valid1$Cover_Type, threshold)
#computeAccuracy(valid1, (predicted.Cover_TypeRF[,2] + predicted.Cover_TypeADA[,2] + predicted.Cover_TypeNB[,2] + predicted.Cover_TypeLOG) / 4, valid1$Cover_Type, threshold)


LOGm <- glm(as.factor(Cover_Type) ~ ., data=train1, family='binomial')
summary(LOGm)
predicted.Cover_Type <- predict(LOGm, type='response')
computeAccuracy(train1, predicted.Cover_Type, train1$Cover_Type, threshold)
predicted.Cover_Type <- predict(LOGm, newdata=valid1, type='response')
computeAccuracy(valid1, predicted.Cover_Type, valid1$Cover_Type, threshold)

CARTm <- rpart(as.factor(Cover_Type) ~ ., data=train1, method="class")
prp(CARTm)
#predicted.Cover_Type <- predict(CARTm, type="class")
predicted.Cover_Type <- predict(CARTm, type="prob")
computeAccuracy(train1, predicted.Cover_Type[,2], train1$Cover_Type, threshold)
#predicted.Cover_Type <- predict(CARTm, newdata=valid1, type="class")
predicted.Cover_Type <- predict(CARTm, newdata=valid1, type="prob")
computeAccuracy(valid1, predicted.Cover_Type[,2], valid1$Cover_Type, threshold)

RFm <- randomForest(as.factor(Cover_Type) ~ ., data = train1, type="classification")
varImpPlot(RFm)
#predicted.Cover_Type <- predict(RFm, type="class")
predicted.Cover_Type <- predict(RFm, type="prob")
computeAccuracy(train1, predicted.Cover_Type[,2], train1$Cover_Type, threshold)
#predicted.Cover_Type <- predict(RFm, newdata=valid1, type="class")
#RFm <- randomForest(as.factor(Cover_Type) ~ ., data = train1, type="classification", maxnode=5, ntree=1000)
predicted.Cover_Type <- predict(RFm, newdata=valid1, type="prob")
computeAccuracy(valid1, predicted.Cover_Type[,2], valid1$Cover_Type, threshold)

ADAm <- ada(as.factor(Cover_Type) ~ ., data = train1)
#predicted.Cover_Type <- predict(RFm, type="class")
predicted.Cover_Type <- predict(ADAm, newdata=train1, type="prob")
computeAccuracy(train1, predicted.Cover_Type[,2], train1$Cover_Type, threshold)
#predicted.Cover_Type <- predict(RFm, newdata=valid1, type="class")
predicted.Cover_Type <- predict(ADAm, newdata=valid1, type="prob")
computeAccuracy(valid1, predicted.Cover_Type[,2], valid1$Cover_Type, threshold)

SVMm <- svm(as.factor(Cover_Type) ~ ., data = train1, type="C-classification", probability=TRUE)
predicted.Cover_Type <- predict(SVMm, train1, decision.values = TRUE, probability=TRUE)
computeAccuracy(train1, attr(predicted.Cover_Type, "probabilities")[,1], train1$Cover_Type, threshold)
SVMm <- svm(as.factor(Cover_Type) ~ ., data = train1, type="C-classification", kernel="linear", cost=1000, probability=TRUE) # linear polynomial 
#SVMm <- svm(as.factor(Cover_Type) ~ ., data = train1, type="C-classification", probability=TRUE, cross=10)
predicted.Cover_Type <- predict(SVMm, newdata=valid1, decision.values = TRUE, probability=TRUE)
computeAccuracy(valid1, attr(predicted.Cover_Type, "probabilities")[,1], valid1$Cover_Type, threshold)

SVMm <- svm(as.factor(Cover_Type) ~ ., data = train, type="C-classification",kernel = "linear", probability=TRUE)
LOGm <- glm(as.factor(Cover_Type) ~ ., data = train, family='binomial')
ADAm <- ada(as.factor(Cover_Type) ~ ., data = train)
RFm <- randomForest(as.factor(Cover_Type) ~ ., data = train, type="classification")
GBMm <- gbm(as.factor(Cover_Type) ~ ., data = train)
CARTm <- rpart(as.factor(Cover_Type) ~ ., data=train, method="class")
predicted.Cover_TypeSVM <- predict(SVMm, train, decision.values = TRUE, probability=TRUE)
predicted.Cover_TypeLOG <- predict(LOGm, train, type='response')
predicted.Cover_TypeCART <- predict(CARTm, train, type="prob")
predicted.Cover_TypeADA <- predict(ADAm, train, type="prob")
predicted.Cover_TypeGBM <- predict(GBMm, train, type="response", n.trees=100)
predicted.Cover_TypeRF <- predict(RFm, train, type="prob")
computeAccuracy(train, attr(predicted.Cover_TypeSVM, "probabilities")[,1], train$Cover_Type, threshold)
computeAccuracy(train, predicted.Cover_TypeLOG, train$Cover_Type, threshold)
computeAccuracy(train, predicted.Cover_TypeCART[,2], train$Cover_Type, threshold)
computeAccuracy(train, predicted.Cover_TypeADA[,2], train$Cover_Type, threshold)
computeAccuracy(train, predicted.Cover_TypeGBM[,2], train$Cover_Type, threshold)
computeAccuracy(train, predicted.Cover_TypeRF[,2], train$Cover_Type, threshold)
computeAccuracy(train, (predicted.Cover_TypeRF[,2] + attr(predicted.Cover_TypeSVM, "probabilities")[,1]) / 2, train$Cover_Type, threshold)

threshold <- 0.53

predicted.Cover_TypeRF <- predict(RFm, newdata=test, type="prob")
testout1 <- data.frame(UserID=test.id, Probability1=predicted.Cover_TypeRF[,2])
predicted.Cover_TypeSVM <- predict(SVMm, newdata=test, decision.values = TRUE, probability=TRUE)
testout2 <- data.frame(UserID=test.id, Probability1=attr(predicted.Cover_TypeSVM, "probabilities")[,1])
plot(testout$Probability1, testout1$Probability1)
testout12 <- data.frame(UserID=test.id, Probability1=(predicted.Cover_TypeRF[,2] + attr(predicted.Cover_TypeSVM, "probabilities")[,1]) / 2)
predicted.Cover_TypeADA <- predict(ADAm, test, type="prob")
testout3 <- data.frame(UserID=test.id, Probability1=predicted.Cover_TypeADA[,2])
predicted.Cover_TypeLOG <- predict(LOGm, test, type="response")
testout4 <- data.frame(UserID=test.id, Probability1=predicted.Cover_TypeLOG[,2])
testout1234 <- data.frame(UserID=test.id, Probability1=(predicted.Cover_TypeRF[,2] + attr(predicted.Cover_TypeSVM, "probabilities")[,1] + predicted.Cover_TypeADA[,2] + predicted.Cover_TypeLOG) / 4)
plot(testout$Probability1, testout2$Probability1)
testout13 <- data.frame(UserID=test.id, Probability1=rowMeans(cbind(testout1$Probability1, testout3$Probability1)))
testout14 <- data.frame(UserID=test.id, Probability1=(predicted.Cover_TypeRF[,2] + predicted.Cover_TypeLOG) / 2)
testout124 <- data.frame(UserID=test.id, Probability1=(predicted.Cover_TypeRF[,2] + attr(predicted.Cover_TypeSVM, "probabilities")[,1] + predicted.Cover_TypeLOG) / 3)

#write.csv(testout, "testout.csv", row.names=FALSE)
#write.csv(testout1, "testout.csv", row.names=FALSE)
#write.csv(testout2, "testout.csv", row.names=FALSE)
#write.csv(testout3, "testout.csv", row.names=FALSE)
#write.csv(testout12, "testout.csv", row.names=FALSE)
#write.csv(testout1234, "testout.csv", row.names=FALSE)
write.csv(testout14, "testout.csv", row.names=FALSE)

testout$algo <- "RF"
testout1$algo <- "SVM"
testout2$algo <- "ADA"
#ggplot(testout,aes(UserID,Probability1))+geom_line(aes(color="First line"))+
#  geom_line(data=testout1,aes(color="Second line"))+
#  labs(color="Legend text")
predicted <- as.data.frame(rbind(testout, testout1, testout2))
#qplot(UserID, Probability1, data = predicted, group = as.factor(algo), colour = as.factor(algo), geom = "line")
ggplot(predicted,aes(x=UserID,y=Probability1 > threshold,colour=as.factor(algo),group=as.factor(algo))) + geom_point()
d <- data.frame(UserID=testout$UserID, RF=testout$Probability1>threshold, SVM=testout1$Probability1>threshold, ADA=testout2$Probability1>threshold)






predictedSVM.Cover_Type <- predict(SVMm, train, decision.values = TRUE, probability=TRUE)
predictedSVM.Cover_Type <- attr(predictedSVM.Cover_Type, "probabilities")[,1]
predictedLOG.Cover_Type <- predict(LOGm, type="response")
#predicted.Cover_Type <- (predictedSVM.Cover_Type + predictedLOG.Cover_Type) / 2
predicted.Cover_Type <- cbind(predictedSVM.Cover_Type, predictedLOG.Cover_Type, threshold)

predictedSVM.Cover_Type[predictedSVM.Cover_Type > threshold] <- 1
predictedSVM.Cover_Type[predictedSVM.Cover_Type <= threshold] <- 0
predictedLOG.Cover_Type[predictedLOG.Cover_Type > threshold] <- 1
predictedLOG.Cover_Type[predictedLOG.Cover_Type <= threshold] <- 0
predicted.Cover_Type[predicted.Cover_Type > threshold] <- 1
predicted.Cover_Type[predicted.Cover_Type <= threshold] <- 0

computeAccuracy(train, predictedSVM.Cover_Type, train$Cover_Type)
computeAccuracy(train, predictedLOG.Cover_Type, train$Cover_Type)
computeAccuracy(train, predicted.Cover_Type, train$Cover_Type)

predictedSVM.Cover_Type <- predict(SVMm, newdata=test, decision.values = TRUE, probability=TRUE)
predictedSVM.Cover_Type <- attr(predictedSVM.Cover_Type, "probabilities")[,1]
predictedLOG.Cover_Type <- predict(LOGm, newdata=test, type="response")
testout <- data.frame(UserID=test.id, Probability1=predictedSVM.Cover_Type, Probability2=predictedLOG.Cover_Type)
plot(testout$Probability1, testout$Probability2)
testout <- data.frame(UserID=test.id, Probability1=predictedLOG.Cover_Type)
write.csv(testout, "testout.csv", row.names=FALSE)


predictedLOG.Cover_Type <- predict(LOGm, type="response")
predictedLOG.Cover_Type[predictedLOG.Cover_Type > threshold] <- 1
predictedLOG.Cover_Type[predictedLOG.Cover_Type <= threshold] <- 0
computeAccuracy(train, predictedLOG.Cover_Type, train$Cover_Type)


sort(unique(train$YOB))
sort(unique(test$YOB))
unique(train$age)
train$age <- 2014 - train$YOB
test$age <- 2014 - test$YOB
unique(train$EducationLevel)
test.id <- test[1]
train <- train[-c(1,2)]
test <- test[-c(1,2)]
names(train)
head(train)
dim(train)
dim(test)

train[train == ""] <- NA
test[test == ""] <- NA

require(lattice)
imp <- mice(train, maxit=1)
### density plot of head circumference per imputation
### blue is observed, red is imputed
densityplot(train, ~Cover_Type|.imp)
### All combined in one panel.
densityplot(imp, ~Cover_Type)

# nhanes example without .id
imp <- mice(train, print = FALSE)
X <- complete(imp, action = "long", include = TRUE)[, -2]
test <- as.mids(X, .id = NULL)
is.mids(test)
test.dat <- complete(test, action = "long", include = TRUE)

imp <- mice(nhanes, seed = 23109)
print(imp)
imp$imp$bmi
complete(imp)
stripplot(imp, pch = 20, cex = 1.2)
xyplot(imp, bmi ~ chl | .imp, pch = 20, cex = 1.4)

imp <- mice(train[,1:6], m=10)
print(imp)
train[,1:6] <- complete(imp)
stripplot(imp, pch = 20, cex = 1.2)
xyplot(imp, bmi ~ chl | .imp, pch = 20, cex = 1.4)

#with(train, impute(age, median))

#preproc = preProcess(train)
#train = predict(preproc, train)
#test = predict(preproc, test)
#train.mod <- missForest(train, verbose=TRUE)
train.num <- train
for (i in 8:108) {
  train.num[,i] <- as.integer(train.num[,i])
}
X <- train.num[,8:108]
#pc.cr <- princomp(X, cor = TRUE) #screeplot(pc.cr) #screeplot(pc.cr, type="lines") #ld <- with(pc.cr, unclass(loadings)) #aload <- abs(ld)
#pcs <- sweep(aload, 2, colSums(aload), "/") #head(pcs) #colSums(pcs) #plot(pc.cr$sdev^2) #lines(pc.cr$sdev^2)

CARTm <- rpart(Cover_Type ~ ., data=train.num, method="class")
prp(CARTm)
p <- predict(CARTm, type="class")
sum(p == train.num$Cover_Type) / nrow(train.num)

CARTm <- rpart(Cover_Type ~ ., data=train, method="class")
prp(CARTm)
p <- predict(CARTm, type="class")
sum(p == train$Cover_Type) / nrow(train)
p <- predict(CARTm, newdata=test, type="class")
p1 <- predict(CARTm, newdata=test)
testout <- data.frame(UserID=test.id,Probability1=p1, Class=p)
write.csv(testout, "testout.csv")

vs <- c("Gender", "Income", "HouseholdStatus", "EducationLevel", "Party", "votes", "Cover_Type")
tvs <- rfImpute(Cover_Type ~ Gender + Income + HouseholdStatus + EducationLevel + Party + votes, train[vs])
for (v in vs) {
  train[v] <- tvs[v]
}

train <- rfImpute(Cover_Type ~ ., train)
rfm <- randomForest(Cover_Type ~ ., data = train)
p <- predict(rfm)
sum(p == train$Cover_Type) / nrow(train)
