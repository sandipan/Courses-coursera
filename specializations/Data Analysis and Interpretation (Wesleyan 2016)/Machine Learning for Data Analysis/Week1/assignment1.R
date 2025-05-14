library(ggplot2)
library(rpart)
library(rpart.plot)
library(caret)
library(ROCR)

setwd('C:/courses/Coursera/Current/ML/Week1')
df <- read.csv('gapminder.csv')
df <- df[-1]
df <- df[!is.na(df$lifeexpectancy),]
ggplot(df, aes(x=lifeexpectancy)) + geom_histogram()
df$lifeexpectancy.factor <- as.factor(ifelse(df$lifeexpectancy > 70, 'High', 'Low'))
tr <- rpart(lifeexpectancy.factor~.-lifeexpectancy, df)
prp(tr, varlen=0)
ntrain <- nrow(df) * 0.6
train.index <- sample(1:nrow(df),ntrain)
train <- df[train.index,]
test <- df[-train.index,]
tr <- rpart(lifeexpectancy.factor~.-lifeexpectancy, train)
p <- predict(tr, newdata=test, type='class')
table(test$lifeexpectancy.factor, p)
sum(test$lifeexpectancy.factor == p) / nrow(test)