############################################################
#     Foundation to Strategic Business Analytics           #
#       Module 3 - Understanding causes and consequences	 #
#                                                  				 #
#                                                          #
# 	Author: Nicolas Glady & Pauline Glikman                #
#                   ESSEC BUSINESS SCHOOL                  #
############################################################

############################################################
# Disclaimer: this script is used to produce the examples  #
#  presented during the course Strategic Business          #
#  Analytics. The author is not responsible in any way     #
#  for any problem encountered during this code execution. #
############################################################

############################################################
####     EXAMPLE N°1 - CREDIT SCORING                   ####
############################################################

# Set your directory to the folder where you have downloaded the Credit Scoring dataset 
setwd('C:/courses/Coursera/Current/Strategic Business Analytics/Week2')

# To clean up the memory of your current R session run the following line
rm(list=ls(all=TRUE))

# Let's load our dataset and call it data
data=read.table('DATA_3.01_CREDIT.csv',sep=',',header=TRUE) # The function read.table enables us to read flat files such as .csv files

# Now let's have a look at our variables and see some summary statistics
str(data) # The str() function shows the structure of your dataset and details the type of variables that it contains
summary(data) # The summary() function provides for each variable in your dataset the minimum, mean, maximum and quartiles

hist(data$Rating) # Produce a histogram of the credit scores
cor(data[,c(1:5,10)]) # Compute the correlation between all the numerical variables of the sample

linreg=lm(Rating~.,data=data) # Estimate a linear regression model of Rating as a function of everything else.

cor(linreg$fitted.values,data$Rating) # Computes the correlation between the fitted values and the actual ones
plot(data$Rating,linreg$fitted.values) # Plot the fitted values vs. the actual ones

summary(linreg) # Reports the results of the regression

linreg=lm(Rating~Income+Cards+Married,data=data) # Estimate a linear regression model of Rating as a function of everything else.
summary(linreg) # Reports the results of the regression

plot(data$Balance,data$Rating) # Allows to visualize the relationship between Balance and Rating
plot(data$Income,data$Rating) # Allows to visualize the relationship between Income and Rating
plot(data$Student,data$Rating) # Allows to visualize the relationship between Income and Rating
plot(data$Education,data$Rating) # Allows to visualize the relationship between Income and Rating
plot(data$Gender,data$Rating) # Allows to visualize the relationship between Income and Rating

############################################################
####        EXAMPLE N°2 - HR ANALYTICS 2                ####
############################################################
# Set your directory to the folder where you have downloaded the HR Analytics 2 dataset

# To clean up the memory of your current R session run the following line
rm(list=ls(all=TRUE))

# Let's load our dataset and call it datatot
datatot=read.table('DATA_3.02_HR2.csv', header = T,sep=',')

# Now let's have a look at our variables and see some summary statistics
str(datatot) # The str() function shows the structure of your dataset and details the type of variables that it contains
summary(datatot) # The summary() function provides for each variable in your dataset the minimum, mean, maximum and quartiles

table(datatot$left) # look at the frequencies for the left variable
table(datatot$left)/nrow(datatot) # look at percentages for the left variable
hist(datatot$left) # alternatively, plot a histogram

cor(datatot) # Let's check out the correlations

logreg = glm(left ~ ., family=binomial(logit), data=datatot) # Estimate the drivers of attrition

hist(logreg$fitted.values) # See the proportion of employee attrition according to the model
cor(logreg$fitted.values,datatot$left) # Assess the correlation between estimated attrition and actual



cutoff=.3 # Cutoff to determine when P[leaving] should be considered as a leaver or not. Note you can play with it...

cutoff=.5

sum(logreg$fitted.values<=cutoff)/nrow(datatot)
sum(logreg$fitted.values>cutoff)/nrow(datatot)
mean((logreg$fitted.values>cutoff)==(datatot$left==1)) # Compute the overall percentage of correctly classified employees

sum(datatot$left==1)/nrow(datatot)

(1-sum(logreg$fitted.values>cutoff)/nrow(datatot))^3
(1-sum(datatot$left==1)/nrow(datatot))^3

sum((logreg$fitted.values<=cutoff)&(datatot$left==0))/sum(datatot$left==0) # Compute the percentage of correctly classified employees who stayed
sum((logreg$fitted.values>cutoff)&(datatot$left==1))/sum(datatot$left==1) # Compute the percentage of correctly classified employees who left
mean((logreg$fitted.values>cutoff)==(datatot$left==1)) # Compute the overall percentage of correctly classified employees

summary(logreg) # Report the results of the logistic regression

# Let's use a more visual way to see the effect of one of the most important driver: TIC

plot(datatot$TIC,datatot$left,main= "Time and Employee Attrition", ylab="Attrition", xlab= "Time spent")

# An aggregated plot
tempdata=datatot
aggbTimeRank=aggregate(left~ TIC, data=tempdata, FUN=mean) # We compute the average attrition rate for each value of TIC
plot(aggbTimeRank$TIC,aggbTimeRank$left,main= "Time and Employee Attrition", ylab="Average Attrition Rate", xlab= "Time spent")

# An even better one!
cntbTimeRank=aggregate(left~ TIC, data=tempdata, FUN=length) # We compute the number of employees for each value of TIC
symbols(aggbTimeRank$TIC,aggbTimeRank$left,circles=cntbTimeRank$left, inches=.75, fg="white", bg="red",main= "Time and Employee Attrition", ylab="Average Attrition Rate", xlab= "Time spent") # we 

# Let's use a more visual way to see the effect of the most important driver: Satisfaction
tempdata=datatot
tempdata$rankSatis = round(rank(-tempdata$S)/600) # We create categories of employee satisfaction ranking. We create 20 groups (because it will work well later...)
aggbSatisRank = aggregate(left~ rankSatis, data=tempdata, FUN=mean) # We compute the average attrition rate for each category
cntbSatisRank = aggregate(left~ rankSatis, data=tempdata, FUN=length) # We compute the number of employees for each value of TIC
symbols(aggbSatisRank$rankSatis,aggbSatisRank$left,circles=cntbSatisRank$left, inches=.2, fg="white", bg="red",main= "Satisfaction and Employee Attrition", ylab="Average Attrition Rate", xlab= "Rank of Satisfaction")


