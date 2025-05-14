m <- lm(hp ~ wt, data=mtcars)
predict(m, newdata=data.frame(wt=3))
m <- lm(Fertility ~., data=swiss)
coef(m)
predict(m, newdata = data.frame(Agriculture = 27.7, 
  Examination = 22,
  Education = 29,
  Catholic = 58.33,
  Infant.Mortality = 19.3))

n <- 5
J2n <- rep(1, 2*n)
X1 <- c(rep(1, n), rep(0,n))
X2 <- c(rep(0, n), rep(1,n))
X <- cbind(J2n, X1)
W <- cbind(J2n, X2)
Z <- cbind(X1, X2)
y <- rnorm(2*n)
y1  <- X %*% solve(t(X)%*%X, t(X)%*%y)
y2 <- W %*% solve(t(W)%*%W, t(W)%*%y)
y3 <- Z %*% solve(t(Z)%*%Z, t(Z)%*%y)

m <- lm(mpg ~ vs + wt, data=mtcars)
coef(m)
cond <- mtcars$vs==1
coef(lm(mpg ~ vs + wt, data=mtcars[cond,]))
coef(lm(mpg ~ vs + wt, data=mtcars[!cond,]))
#coef(lm(mpg ~ vs + wt + 0, data=mtcars))
X <- cbind(rep(1, length(mtcars$wt)), mtcars$wt)
y <- mtcars$mpg
solve(t(X[cond,])%*%X[cond,], t(X[cond,])%*%y[cond])
solve(t(X[!cond,])%*%X[!cond,], t(X[!cond,])%*%y[!cond])

library(dplyr)
X <- mtcars %>% select(mpg, hp, drat, wt, qsec)
res <- princomp(X, cor=TRUE)
cumsum(res$sdev^2) / sum(res$sdev^2)