1-exp(-2)
integrate(function(x)3*x^2, 0,0.5)
integrate(function(x)x*3*x^2, 0,1)
integrate(function(x)x^2*3*x^2, 0,1)
0.6-0.75^2
integrate(function(x)(x-0.75)^2*3*x^2, 0,1)
pnorm(3, 1, 2)
integrate(function(x)exp(-2*abs(x)), -Inf, Inf)

#devtools::install_github("FedericoComoglio/rSymPy")

library(rSymPy)
x <- Var("x")
k <- Var("k")
sympy("integrate(1-k*abs(x), (x, -1/k, 1/k))")
sympy("integrate(exp(-x), (x, 0, oo))")  # definite integral

sympy("integrate(1-k*abs(x), (x, -1/k, 1/k))")

t <- seq(-10,10,0.1)
plot(t, exp(-abs(t)), type='l', col='red')
lines(t, exp(-10*abs(t)), col='blue')

sympy("integrate(2*exp(-I*k*x)/(2*pi), (x, -1, 1))")  # definite integral
