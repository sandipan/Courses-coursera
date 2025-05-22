library(caret)
library(ggplot2)
library(rpart)
library(rpart.plot)
library(randomForest)
library(e1071)
library(dplyr)
setwd('C:/courses/Coursera/Current/Practical Predictive Analytics Models and Methods/Week2/')
# Step 1: Read and summarize the data
df <- read.csv('seaflow_21min.csv')
summary(df)
df %>% group_by(pop) %>% summarise(count=n())
#set.seed(100)
# Step 2: Split the data into test and training sets
inTrain <- createDataPartition(y = df$pop, p = 0.5, list = FALSE)
training <- df[inTrain,]                               
testing <- df[-inTrain,]                               
nrow(training)
nrow(testing)
mean(training$time)
summary(training)
#training %>% select(time) %>% mean
# Step 3: Plot the data
ggplot(df, aes(pe, chl_small, color=pop)) + geom_point()

# Step 4: Train a decision tree.
#set.seed(100)
model.tree <- rpart(pop~fsc_small + fsc_perp + fsc_big + pe + chl_big + chl_small, method="class", data=training)
prp(model.tree)
model.tree
varImp(model.tree)
# Step 5: Evaluate the decision tree on the test data.
pred.tree <- predict(model.tree, newdata=testing, type='class')
accuracy.tree <- sum(pred.tree == testing$pop) /  nrow(testing)
accuracy.tree
# Step 6: Build and evaluate a random forest.
#set.seed(100)
model.forest <- randomForest(pop~fsc_small + fsc_perp + fsc_big + pe + chl_big + chl_small, data=training)
#sort(importance(model), decreasing=TRUE)
importance(model.forest)
max(importance(model.forest))
varImpPlot(model.forest)
pred.forest <- predict(model.forest, newdata=testing)
accuracy.forest <- sum(pred.forest == testing$pop) /  nrow(testing)
accuracy.forest
# Step 7: Train a support vector machine model and compare results.
#set.seed(100)
model.svm <- svm(pop~fsc_small + fsc_perp + fsc_big + pe + chl_big + chl_small, data=training)
pred.svm <- predict(model.svm, newdata=testing)
accuracy.svm <- sum(pred.svm == testing$pop) /  nrow(testing)
accuracy.svm
# Step 8: Construct confusion matrices
table(pred = pred.forest, true = testing$pop)
table(pred = pred.tree, true = testing$pop)
table(pred = pred.svm, true = testing$pop)

# Step 9: Sanity check the data
plot(df$fsc_small)
plot(df$fsc_perp)
plot(df$fsc_big)
plot(df$pe)
plot(df$chl_small)
plot(df$chl_big)
ggplot(df, aes(time, chl_big, color=pop)) + geom_point()

df <- df %>% filter(file_id != 208)
df %>% select(file_id) %>% unique
inTrain <- createDataPartition(y = df$pop, p = 0.5, list = FALSE)
training <- df[inTrain,]                               
testing <- df[-inTrain,]                               
#set.seed(100)
model <- svm(pop~fsc_small + fsc_perp + fsc_big + pe + chl_big + chl_small, data=training)
pred <- predict(model, newdata=testing)
accuracy <- sum(pred == testing$pop) /  nrow(testing)
accuracy
accuracy - accuracy.svm