setwd("C:/Users/SANDIPAN DEY/Desktop/coursera/Developing Data Products/Quiz")

if (!require("yhat", character.only = TRUE)) {
  install.packages("yhat", dep=TRUE)
}
if (!require("yhatr", character.only = TRUE)) {
  install.packages("yhatr", dep=TRUE)
}
if (!require("roxygen2", character.only = TRUE)) {
  install.packages("roxygen2", dep=TRUE)
}

#4
library(yhat)
library(yhatr)

yhat.config <- c(
  username = "sandipan.dey@gmail.com",
  apikey = "46a2a7bd2be69c45ff55f315d13bd1c9",
  env = "http://cloud.yhathq.com/"
)

df <- iris
df$Sepal.Width_sq <- df$Sepal.Width^2
fit <- glm(I(Species)=="virginica" ~ ., data=df)

model.require <- function() {
  # require("randomForest")
}

model.transform <- function(df) {
  df$Sepal.Width_sq <- df$Sepal.Width^2
  df
}
model.predict <- function(df) {
  data.frame("prediction"=predict(fit, df, type="response"))
}
yhat.deploy.to.file("irisModel")
#yhat.deploy("irisModel")

#5
#  Create R Package
library(roxygen2)
roxygenize("DDPQuiz3")
library(devtools)
build('DDPQuiz3')
install('DDPQuiz3')
library(DDPQuiz3)
createmean(c(1,2,3,4))
?createmean

#R CMD build DDPQuiz3
#R CMD check DDPQuiz3_1.0.tar.gz
#R CMD INSTALL DDPQuiz3_1.0.tar.gz 