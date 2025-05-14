integrate(function(x) 3/(x^4), 1, Inf)
integrate(function(x) 3*x/(x^4), 1, Inf)

res <- replicate(10000,
          {
            tr <- sample(c('H', 'T'), 10, TRUE)
            sum(tr == 'H')*1 + sum(tr=='T')*(-1)
          })
hist(res)
mean(res)
var(res)

#library(rSymPy)
#integrate(function(x) (k+1)*x^k, 1, Inf)

2*log(2)
sqrt(log(2))

1/(1+ .48/.75 * .7/.3)

compute_DLR <- function(sensitivity, specificity) {
  return(sensitivity / (1 - specificity))
}
compute_DLR(0.75, 0.52)

compute.bayes <- function(conds, priors, index) {
  return (conds[index]*priors[index] / sum(conds*priors))
}
compute.bayes(c(1, 1), c(1/2*1/2, (1-1/2)*(1-1/2)), 1)
compute.bayes(c(0.75, 1-0.52), c(0.3, 1-0.3), 1)

bernoulli.L <- function(p, x1) {
  return(p^x1*(1-p)^(1-x1))
}

bernoulli.L <- function(p, xs) {
  return(p^sum(xs)*(1-p)^(length(xs)-sum(xs)))
}

uniform.L <- function(p, x1) {
  return(ifelse((x1 >= p) & (x1 <= p+1), p+1-x1, 0))
}

plt.likelihood <- function(L, p_values, x1) {
  plot(p_values, L(p_values, x1), type='l')
}

x1 = 5
plt.likelihood(uniform.L, seq(3,7,0.01), x1)

plt.likelihood(bernoulli.L, seq(0,1,0.01), 1)

plt.likelihood(bernoulli.L, seq(0,1,0.01), c(1,0,1,0))
plt.likelihood(bernoulli.L, seq(0,1,0.01), c(1,0,1,0,1,1))

pnorm(70, 80, 10, lower.tail = TRUE)
pnorm((70 - 80) / 10, lower.tail = TRUE)

qnorm(0.95)

qnorm(0.95, 1100, 75, lower.tail = TRUE)

qnorm(0.95, 1100, 75/10, lower.tail = TRUE)
m <- replicate(10000, {
  x <- rnorm(100, 1100, 75)
  mean(x)
})
hist(m)
quantile(m, 0.95)

p <- pnorm(90, 80, 10, lower.tail=FALSE)
sum(dbinom(4:5, 5, p))
pbinom(3, 5, p, lower.tail = FALSE)

sum(dbinom(4:5, 5, 1/2))

pnorm(16, 15, 10/10, lower.tail = TRUE) - pnorm(14, 15, 10/10, lower.tail = TRUE)

v <- replicate(1000, {
  x <- runif(100)
  var(x)
})
mean(v)
1/12


m <- replicate(10000, {
  x <- rnorm(100)
  mean(x)
})
q1 <- quantile(m, 0.95)

m <- replicate(10000, {
  x <- rnorm(10)
  mean(x)
})
q2 <- quantile(m, 0.95)

q1
q2
q1 / q2
sqrt(10) / 10

x <- runif(1000) #rnorm(1000) #rexp(1000)
a <- 5
b <- 2
y <- a^2*x + b
qqplot(x,y)

quantile(x)
quantile(y)
quantile(y) / (a^2*quantile(x) + b)


x <- rnorm(100, 10, 2)
bx <- replicate(1000, {
  mean(sample(x, 100, replace=TRUE))
})
hist(bx)
mean(x)
mean(bx)

c(1100 + qt(0.025, 9-1)*30/sqrt(9), 1100 - qt(0.025, 9-1)*30/sqrt(9))
c(1100 + qnorm(0.025)*30/sqrt(9), 1100 - qnorm(0.025)*30/sqrt(9))

-2
for (s in seq(0,3,0.1)) {
  print(c(s, qt(0.025, 9-1, lower.tail=FALSE)*s/sqrt(9)))
}

Sp <- sqrt(((10-1)*0.60+(10-1)*0.68) / (10+10-2))
5 - 3 + c(-1,1)*qt(0.975, 10+10-2)*Sp*sqrt(1/10+1/10)


x <- c(1,3)
bx <- replicate(1000, {
  mean(sample(x, 2, replace=TRUE))
})
hist(bx)
table(bx) / length(bx)

x <- 4
n <- 10
a <- 10
b <- 10

(x + a) / (n + a + b)

bx <- replicate(10000, {
  x <- rlnorm(100, 5, 1)
  exp(sum(log(x))/100)
})
mean(bx)
exp(5)

bx <- replicate(10000, {
  x <- rlnorm(100, 5, 1)
  mean(x)
})
mean(bx)
exp(5+1/2)