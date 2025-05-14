library(arules)
library(arulesViz)

data("Adult")

params <- list(support = 0.5, maxlen = 5)
## Mine itemsets with minimum support of 0.1 and 5 or less items
itemsets <- eclat(Adult,
                  parameter = params)
itemsets
## Create rules from the frequent itemsets
rules <- ruleInduction(itemsets, confidence = .9)
rules
DATAFRAME(rules, separate = TRUE)[1:10,]


rules <- apriori(Adult, parameter = params)
DATAFRAME(rules, separate = TRUE)[1:10,]

library(arules)
library(microbenchmark)
library(ggplot2)
set.seed(123)
tm <- microbenchmark(eclat(Adult,
                           parameter = list(supp = 0.5, maxlen = 5)),
                     apriori(Adult, 
                           parameter = list(support = 0.5, maxlen = 5)), 
                     times=100L)
autoplot(tm)