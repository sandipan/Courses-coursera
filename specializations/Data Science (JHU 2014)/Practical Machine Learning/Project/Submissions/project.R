setwd("C:/Users/SANDIPAN DEY/Desktop/coursera/Practical ML")

library(caret)
library(rpart.plot)
library(rattle)

getTestResults <- function(trainFile, testFile) {

  training <- read.csv(trainFile) # preprocessed training
  testing <- read.csv(testFile)   # preprocessed testing
  training <- training[c(names(testing)[-ncol(testing)], "classe")]
  
  users <- sort(unique(training$user_name))
  #sort(unique(testing$user_name))

  sink("output.txt")
  results <- NULL
  for (user in users) { #users) {
    
    print(user)
    
    trainingUser <- subset(training, user_name == user)[-1]
    trainingUser <- trainingUser[sample(1:nrow(trainingUser), 200), ]
    inTrain = createDataPartition(trainingUser$classe, p = 3/4, list = FALSE)
    trainingSet = trainingUser[inTrain,]
    validationSet = trainingUser[-inTrain,]
  
    rpartFit <- train(classe ~ ., data=trainingSet, method = "rpart")
    gbmFit <- train(trainingSet, trainingSet$classe, method = "gbm", verbose=FALSE)
    rfFit <- train(classe ~ ., data=trainingSet, method = "rf")
    #ldaFit <- train(classe ~ ., data=trainingSet, method = "lda")
    
    png(paste(user, '.png', sep=""), height=700, width=650)
    fancyRpartPlot(rpartFit$finalModel)
    dev.off()
    
    prpart <- predict(rpartFit, newdata=validationSet)
    pgbm <- predict(gbmFit, newdata=validationSet)
    prf <- predict(rfFit, newdata=validationSet)
    #plda <- predict(ldaFit, newdata=validationSet)
  
    #predDF <- data.frame(prpart, prf, pgbm, plda, classe=validationSet$classe)
    predDF <- data.frame(prpart, prf, pgbm, classe=validationSet$classe)
    #predDF <- data.frame(prf, pgbm, classe=validationSet$classe)
    combRFFit <- train(as.factor(classe) ~ ., data=predDF, method="rf")
    pcomb <- predict(combRFFit, predDF)
    
    print(confusionMatrix(data = prpart, validationSet$classe))
    print(confusionMatrix(data = pgbm, validationSet$classe))
    print(confusionMatrix(data = prf, validationSet$classe))
    #confusionMatrix(data = plda, validationSet$classe)
    print(confusionMatrix(data = pcomb, validationSet$classe))
    
    testingUser <- subset(testing, user_name == user)[-1]
    
    prpart <- predict(rpartFit, newdata=testingUser)
    pgbm <- predict(gbmFit, newdata=testingUser)
    prf <- predict(rfFit, newdata=testingUser)
    #plda <- predict(ldaFit, newdata=testingUser)
    
    #predDF <- data.frame(prpart, prf, pgbm, plda)
    predDF <- data.frame(prpart, prf, pgbm)
    #predDF <- data.frame(prf, pgbm)
    pcomb <- predict(combRFFit, newdata=predDF)
    
    results <- rbind(results, cbind(id=testingUser$problem_id, pred=pcomb))
    #print(results)
  }
  print(results)
  
  sink()
  #unlink("output.txt")
  return(results)
}


#answers = rep("A", 20)
trainFile <- "pml-training.csv"
testFile <- "pml-testing.csv"
answers <- getTestResults(trainFile, testFile)
#pml_write_files(answers)




setwd("C:/Users/SANDIPAN DEY/Desktop/coursera/Practical ML")

library(caret)
library(rpart.plot)
library(rattle)
#install_github('caretEnsemble', 'zachmayer') #Install zach's caretEnsemble package
#library(caretEnsemble)

getTestResults <- function(trainFile, testFile) {
  
  training <- read.csv(trainFile) # preprocessed training
  testing <- read.csv(testFile)   # preprocessed testing
  training <- training[c(names(testing)[-ncol(testing)], "classe")]
  myControl <- trainControl(method='cv', number=10)
  
  users <- sort(unique(training$user_name))
  #sort(unique(testing$user_name))
  
  results <- NULL
  for (user in users) { 
    
    print(user)
    
    trainingUser <- subset(training, user_name == user)[-1]
    
    rpartFit <- train(trainingUser, trainingUser$classe, method = "rpart", trControl = myControl)
    gbmFit <- train(trainingUser, trainingUser$classe, method = "gbm", verbose=FALSE, trControl = myControl)
    rfFit <- train(classe ~ ., data=trainingUser, method = "rf", trControl = myControl)
    #enFit <- caretStack(list(gbmFit, rfFit, method='rf', trControl=trainControl(method='cv')))
    
    print(rpartFit$finalModel)
    print(gbmFit$finalModel)
    print(rfFit$finalModel)
    
    testingUser <- subset(testing, user_name == user)[-1]
    
    pgbm <- predict(gbmFit, newdata=testingUser)
    prf <- predict(rfFit, newdata=testingUser)
    #pef <- predict(enFit, newdata=testingUser)
    
    results <- rbind(results, cbind(id=testingUser$problem_id, pred1=as.factor(pgbm), pred2=as.factor(prf))) #, pred3=as.factor(pef)))
    
    print(results)
  }
  return(results)
}

pml_write_files = function(x){
  classes = c('A', 'B', 'C', 'D', 'E')
  n = length(x)
  for(i in 1:n){
    filename = paste0("problem_id_",i,".txt")
    write.table(classes[x[i]],file=filename,quote=FALSE,row.names=FALSE,col.names=FALSE)
  }
}

#pml_write_files(results)

#answers = rep("A", 20)
trainFile <- "pml-training.csv"
testFile <- "pml-testing.csv"
answers <- getTestResults(trainFile, testFile)
answers <- as.data.frame(answers)
answers <- answers[order(answers$id),]
pml_write_files(answers$pred2)

