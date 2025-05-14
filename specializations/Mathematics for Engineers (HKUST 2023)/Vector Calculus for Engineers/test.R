x <- 0:3
y <- c(1,3,3,4)
n <- length(x)
sx <- sum(x)
sy <- sum(y)
sx2 <- sum(x**2)
sxy <- sum(x*y)
b0 <- (sx2*sy - sxy*sx) / (n*sx2-sx^2)
b1 <- (n*sxy - sx*sy) / (n*sx2-sx^2)
X <- cbind(rep(1,n), x)
solve(t(X)%*%X, t(X)%*%y)
lm(y~x)

x <- 0:2
y <- c(1,3,4)
n <- length(x)
sx <- sum(x)
sy <- sum(y)
sx2 <- sum(x**2)
sxy <- sum(x*y)
b0 <- (sx2*sy - sxy*sx) / (n*sx2-sx^2)
b1 <- (n*sxy - sx*sy) / (n*sx2-sx^2)
X <- cbind(rep(1,n), x)
solve(t(X)%*%X, t(X)%*%y)
lm(y~x)

integrate(function(r) (10-9*r)*2*pi*r, 0, 1)
integrate(function(r) (10-r)*4*pi*r**2, 0, 5)
integrate(function(r) (1+9*r)*2*pi*r, 0, 1)
integrate(function(r) (4+r/5)*4*pi*r**2, 0, 20)$value / (4*pi*20**3/3)

library(rSymPy)  
x <- Var("x")
sympy("integrate(x*exp(2*x),x)")          # indefinite integral
sympy("integrate((1+2*x)*exp(2*x),x)")          # indefinite integral
sympy("integrate((1+2*x**2)*exp(2*x),x)")          # indefinite integral
