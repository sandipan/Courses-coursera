library(ggplot2)
setwd('C:\\courses\\Coursera\\Current\\Data Analysis Tools\\Week1\\')
df <- read.csv('gapminder.csv')

df1 <- df[c('lifeexpectancy', 'incomeperperson')]
df1 <- df1[complete.cases(df1),]
summary(df1)

#options(scipen = 999) # disable scientific notion
df1$incomeperperson <- cut(df1$incomeperperson, breaks=c(0,2385,52302), dig.lab=10) #breaks=data.frame(classIntervals(,n=3,method="quantile")[2])[,1], include.lowest=T,dig.lab=10) 
with(df1, tapply(lifeexpectancy, incomeperperson, length))
with(df1, tapply(lifeexpectancy, incomeperperson, mean))
with(df1, boxplot(lifeexpectancy ~ incomeperperson))
ggplot(aes(y = lifeexpectancy, x = incomeperperson, fill = incomeperperson), data = df1) + geom_boxplot()

#with(df1, oneway.test(lifeexpectancy~incomeperperson))
aov.out = aov(lifeexpectancy~incomeperperson, data=df1)
summary(aov.out)
TukeyHSD(aov.out)

df2 <- df[c('lifeexpectancy', 'alcconsumption')]
df2 <- df2[complete.cases(df2),]
summary(df2)

#options(scipen = 999) # disable scientific notion
df2$alcconsumption <- cut(df2$alcconsumption, breaks=c(0,3,6,10,25), dig.lab=10) #breaks=data.frame(classIntervals(,n=3,method="quantile")[2])[,1], include.lowest=T,dig.lab=10) 
with(df2, tapply(lifeexpectancy, alcconsumption, length))
with(df2, tapply(lifeexpectancy, alcconsumption, mean))
with(df2, boxplot(lifeexpectancy ~ alcconsumption))
ggplot(aes(y = lifeexpectancy, x = alcconsumption, fill = alcconsumption), data = df2) + geom_boxplot()

#with(df2, oneway.test(lifeexpectancy~alcconsumption))
aov.out = aov(lifeexpectancy~alcconsumption, data=df2)
summary(aov.out)
TukeyHSD(aov.out)