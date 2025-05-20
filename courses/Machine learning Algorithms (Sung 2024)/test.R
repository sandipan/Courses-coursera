# W1 W2
# P(~W2|W1) = 80/99         # W1 => 19 / 99

# P(S) = 0.5, P(cash|S) = 0.95, P(cash|~spam) = 0.02
# P(S | cash) = P(cash | S)P(S) / P(cash)
0.95*0.5 / (0.95*0.5 + 0.02*0.5)
1 / (1 + 2 / 95)
95 / 97

library(rpart)
library(rattle)
library(rpart.plot)
library(RColorBrewer)

train <- data.frame(
  A = c(F,T,T,T),
  B = c(F,F,T,T),
  C = c(F,T,F,T),
  Y = c(F,T,T,F)
)

mytree <- rpart(
  Y ~ ., 
  data = train, 
  method = "class", 
  minsplit = 2, 
  minbucket = 1
)
fancyRpartPlot(mytree, caption = NULL)
