setwd('C:/courses/Coursera/Current/Strategic Business Analytics')

df <- read.csv('DATA_2.01_SKU.csv')
summary(df$CV)
fivenum(df$CV)

fit <- hclust(dist(scale(df)), "ward.D")
plot(fit)
groups <- cutree(fit, k=2)
rect.hclust(fit, k=2, border="red")
