df <- read.csv('C:\\courses\\Coursera\\Past\\Specialization-UW Machine Learning\\ML Regression\\Week5\\weights2.csv')
library(reshape2)
df <- melt(df[-1], id='lambda')
library(ggplot2)
ggplot(df, aes(lambda, value, col=variable)) + 
  scale_x_log10() +
  geom_point() + geom_line() +
  guides(color=guide_legend(title="coef"))