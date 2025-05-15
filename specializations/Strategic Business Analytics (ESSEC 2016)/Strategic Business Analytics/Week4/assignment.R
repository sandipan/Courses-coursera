library(ggplot2)
library(scales)

setwd('C:/courses/Coursera/Current/Strategic Business Analytics/Week4')

df <- read.csv('day.csv')
df$dteday <- as.Date(df$dteday)
df$Total <- df$cnt
ggplot(df, aes(x=dteday)) + 
  geom_point(aes(y = Total, colour = "Total")) + 
  geom_line(aes(y = Total, colour = "Total")) + 
  geom_point(aes(y = casual, colour = "casual")) + 
  geom_line(aes(y = casual, colour = "casual")) + 
  geom_point(aes(y = registered, colour = "registered")) + 
  geom_line(aes(y = registered, colour = "registered")) + 
  scale_x_date(breaks=date_breaks("10 day"), labels=date_format("%Y-%m-%d")) +
  scale_y_continuous(breaks=seq(0, 9000, 250)) + 
  #facet_wrap(~weekday, scale='free') +
  facet_wrap(~workingday, scale='free') +
  xlab('Date') +
  ylab('Total number of Bikes') +
  theme(axis.text.x = element_text(angle = 90, hjust = 1), text = element_text(size = 15))

df1 <- df[order(df$Total, decreasing=TRUE),][1:50,]
ggplot(df1, aes(x=reorder(dteday,-Total), y=Total, fill=Total)) + 
  geom_bar(stat="identity") +
  facet_wrap(~workingday, scale='free') +
  xlab('Date') +
  ylab('Total number of Bikes') +
  theme(axis.text.x = element_text(angle = 90, hjust = 1), text = element_text(size = 15))

df <- read.csv('hour.csv')
df$dteday <- as.Date(df$dteday)
days <- c(df1[df1$workingday==1,][1,]$dteday, df1[df1$workingday==0,][1,]$dteday)
df2 <- df[df$dteday %in% days,]
df2$Total <- df2$cnt
ggplot(df2, aes(x=hr)) + 
  geom_point(aes(y = Total, colour = "Total"), size=2) + 
  geom_line(aes(y = Total, colour = "Total")) + 
  geom_point(aes(y = casual, colour = "casual"), size=2) + 
  geom_line(aes(y = casual, colour = "casual")) + 
  geom_point(aes(y = registered, colour = "registered"), size=2) + 
  geom_line(aes(y = registered, colour = "registered")) + 
  scale_x_continuous(breaks=0:24) +
  #scale_y_continuous(breaks=seq(0, 9000, 250)) + 
  xlab('Hour') +
  ylab('Total number of Bikes') +
  facet_wrap(~dteday, scale='free')

#df <- read.csv('RejectStatsA.csv')
#df$Debt.To.Income.Ratio <- as.numeric(gsub('%', '', df$Debt.To.Income.Ratio))

ggplot(df, aes(x=cnt)) + geom_histogram() + facet_grid(weathersit~season, scales = 'free')

ggplot(df, aes(x=temp*41, y=hum)) + geom_histogram() + facet_grid(weathersit~season, scales = 'free')

hist(df$casual, col=rgb(1,0,0,0.5),xlim=c(0,7000), ylim=c(0,300), main='Count')
hist(df$registered, col=rgb(0,0,1,0.5), add=T)
#hist(df$cnt, col=rgb(0,1,0,0.5), add=T)
box()

symbols(df$temp*41, df$windspeed*67, circles=sqrt(df$cnt/pi), bg=df$casual)

ggplot(df, aes(temp*41, windspeed*67)) + 
  geom_point(aes(size = cnt, color=as.factor(season))) + 
  scale_size_area() #+ scale_color_gradient(low = "green", high='red')


df <- df[-1]
df <- df[!is.na(df$lifeexpectancy),]
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