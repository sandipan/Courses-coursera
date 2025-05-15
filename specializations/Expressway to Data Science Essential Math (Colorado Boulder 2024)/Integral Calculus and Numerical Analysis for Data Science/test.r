eps <- 1e-6

bisect <- function(a, b, f) {
  stopifnot(f(a) < 0 & f(b) > 0)
  m <- (a + b) / 2
  i <- 1
  while (abs(f(m)) > eps) {
    print(paste(i, m))
    if (f(m) < 0) {
      a <- m
    } else {
      b <- m
    }
    m <- (a + b) / 2
    i <- i + 1
  }
  return(m);
}

newton <- function(a, f, df) {
  maxit <- 100
  i <- 0
  while ((abs(f(a)) > eps) && (i < maxit)) {
    print(paste(i, a))
    a <- a - f(a) / df(a)
    i <- i + 1
  }
  return(a);
}

f <- function(x) {
  return (x**2 - 3)
  #return (x**2 - 2)
}

df <- function(x) {
  return(2*x)
}

#bisect(1, 2, f)
#bisect(0, 4, f)
#newton(2, f, df)
#newton(1.5, f, df)

A <- matrix(c(-4,4,6,-4,6,4,-8,4,10), ncol=3)
eigen(A)

A <- matrix(c(4,11,14,8,7,-2), nrow=2, byrow=TRUE)
svd(A)
eigen(A%*%t(A))
eigen(t(A)%*%A)

4/3
integrate(function(x) x^2-1, -1, 1)
abs(2*integrate(function(x) x^2-1, 0, 1)$val)


library(rSymPy)
sympy("var('x')")
sympy("integrate(x*exp(x))")
sympy("integrate(x*exp(x), (x, 0, 2))")
integrate(function(x) x*exp(x), 0, 2)
exp(1)^2+1