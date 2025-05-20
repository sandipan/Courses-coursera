setwd("C:/courses/Coursera/Current/Excel/Week6")
df <- read.csv('test.csv')
df[2:7] <- scale(df[2:7])
#df$Default_Outcomes[df$Default_Outcomes==1] <- 3.5
#df$Default_Outcomes[df$Default_Outcomes==0] <- -3.5
train <- df[1:200,2:8]
test <- df[201:400,2:8]
m <- glm(Default_Outcomes~.-1,data=train, family='binomial')
summary(m)
p <- predict(m, type='response')
#(max1-min1)/(max-min)*(value-min)+min1
p1 <- 7 * p - 3.5
#table(ifelse(predict(m, type='response') > 0.5, 1, 0), train$Default_Outcomes)
library(rpart)
library(rpart.plot)
m <- rpart(Default_Outcomes~., data=train)
prp(m)

m <- lm(Default_Outcomes~years.at.employer+credit.card.debt-1,data=train) #, family='binomial')
summary(m)

750000 / (450 * 1000)

100 * 72 / 200

FPR = FP / (FP + TN)
TPR = TP / (TP + FN)
TI = (TP + FP) / (TP + FP + TN + FN)
PPV = TP / (TP + FP)
NPV = TN / (TN + FN)

FPR = FP / (FP + TN) = 1 / (1 + TN / FP)

TI = (TP + FP) / (TP + FP + TN + FN) = 1 / (1 + (TN + FN) / (TP + FP))

TN / FP   >  (TN + FN) / (TP + FP)

TN.TP + TN.FP > TN.FP + FP.FN

TP.TN > FP.FN

TPR = TP / (TP + FN) = 1 / (1 + FN / TP)

TP = FP = 36
FN = 14
TN = 116

FN / TP   <  (TN + FN) / (TP + FP)

FN.TP + FN.FP < TN.TP + TP.FN

FN.FP < TN.TP


#Recall that conditional entropy is written H(X|Y) and is determined as 
#(the test incidence, or probability of a positive classification)*H((+, -)| Y = Test is Positive) +
#(the probability of a negative classification)*H((+,-)| Y = Test is Negative)
-TIP * (PPV*log(PPV,2) + (1-PPV)*log(1-PPV,2)) - TIN * (NPV*log(NPV,2) + (1-NPV)*log(1-NPV,2))

.81128 - 0.6736587

100 * 0.1376213 / .81128

450 / 0.1376213

# Egortopia

1250 - 838
TP = 36
FP = 39
FN = 14
TN = 111
TPR = TP / (TP + FN)
PPV = TP / (TP + FP)
NPV = TN / (TN + FN)
TIP = (TP + FP) / (TP + FP + TN + FN) 
TIN = (TN + FN) / (TP + FP + TN + FN) 

-TIP * (PPV*log(PPV,2) + (1-PPV)*log(1-PPV,2)) - TIN * (NPV*log(NPV,2) + (1-NPV)*log(1-NPV,2))

.81128 - 0.6907666

100 * 0.1205134 / .81128

413 /  0.1205134

0.6736587 - 0.6907666

413 - 450

(413 - 450) / (0.6736587 - 0.6907666)



