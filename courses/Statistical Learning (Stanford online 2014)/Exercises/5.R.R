require(boot)
setwd("C:/Users/sandipan/Desktop/Statistical Learning")

load("5.R.Rdata")
head(Xy)

m <- lm(y ~ ., data=Xy)
summary(m)
matplot(Xy,type="l",col=c("red","green","blue"))

rsq <- function(formula, data, indices) {
  d <- data[indices,] # allows boot to select sample 
  #d <- data
  fit <- lm(formula, data=d)
  return(fit$coefficients[2])
  #return(summary(fit)$r.square)
} 

boot.out=boot(Xy, rsq, R=1000,formula=y~.)
boot.out
plot(boot.out)

# block boot for time series
#boot.out=tsboot(Xy, rsq, R=1000, sim="fixed", l=1, formula=y~.)
boot.out=tsboot(Xy, rsq, R=1000, sim="fixed", l=100, formula=y~.)
boot.out
plot(boot.out)
