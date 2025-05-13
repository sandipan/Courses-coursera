compute.posterior.coin <- function(prior, n, h, likelihood=likelihood.coin, p=1/2) {
  return (likelihood(n, h, p)*prior / 
            (likelihood(n, h, p)*prior + integrate(function(p) choose(n, h)*p^h*(1-p)^(n-h), 0, 1)$value*(1-prior)))
}

likelihood.coin <- function(n, h, p=1/2) {
  return (choose(n, h)*p^h*(1-p)^(n-h))
}

# P(H0|HHH) = P(HHH | H0)P(H0) / P(HHH) = P(HHH | H0)P(H0) / (P(HHH | H0)P(H0) + P(HHH | HA)P(HA))
#n <- 3
#p0 <- 1/2
#(1/2)^n * p0 / ((1/2)^n*p0 + integrate(function(p) p^n, 0, 1)$value*(1-p0))
compute.posterior.coin(1/2, 3, 0)

# P(H0|HHHHH) = P(HHHHH | H0)P(H0) / P(HHHHH) = P(HHHHH | H0)P(H0) / (P(HHHHH | H0)P(H0) + P(HHHHH | HA)P(HA))
#n <- 5
#p0 <- 0.66
#(1/2)^n * p0 / ((1/2)^n*p0 + integrate(function(p) p^n, 0, 1)$value*(1-p0))
compute.posterior.coin(0.66, 5, 0)

# P(H+1|+0.5) = P(+0.5|H1)P(H+1) / (P(+0.5|H1)P(H+1) + P(+0.5|H-1)P(H-1))
exp(-(0.5-1)^2/2)/sqrt(2*pi)*0.5 / (exp(-(0.5-1)^2/2)/sqrt(2*pi)*0.5 + exp(-(0.5+1)^2/2)/sqrt(2*pi)*0.5)

p0 <- 0.99
for (n in 1:20) {
  print(c(n, compute.posterior.coin(p0, n, n, p=1/6)))
}

#p0 <- 0.99
#for (n in 1:20) {
#  p0 <- compute.posterior.coin(p0, n, n)
#  print(c(n, p0))
#}

compute.posterior <- function(tpr, fpr, prior) {
  return (tpr*prior / (tpr*prior + fpr*(1-prior)))
}

# P(+|D) = 0.95, P(+|~D) = 0.1
# P(D|+) = P(+|D)P(D) / P(+)
p0 <- 0.01
for(n in 1:10) {
  p0 <- 0.95*p0 / (0.95*p0 + 0.1*(1-p0)) 
  print(c(n, p0))
}

p0 <- 0.01
for(n in 1:2) {
  p0 <- 0.95*p0 / (0.95*p0 + 0.1*(1-p0)) 
  print(c(n, p0))
}

# P(A|R) = P(R|A)P(A) / P(R)
l <- 0.25 #0.5 #0 #0.35
u <- 0.75 #1 #0.25 #0.65
pA <- 0.5
(u-l)*pA / ((u-l)*pA + integrate(function(x) 2*x, l, u)$value*(1-pA))

# P(+|P) = 0.99, P(+|~P) = 0.01
#p0 <- 0.99
# P(P|+) = P(+|P)p0 / (P(+|P)p0 + P(+|~P)(1-p0))
0.99*p0 / (0.99*p0 + 0.01*(1-p0))
compute.posterior(0.99, 0.1, 0.99)

compute.posterior.coin(1/2, 3, 0)

# P(+|D) = 0.95, P(+|~D) = 0.1
# P(D|+) = P(+|D)P(D) / P(+)
#p0 <- 0.99
#0.95*p0 / (0.95*p0 + 0.01*(1-p0))
compute.posterior(0.95, 0.01, 0.99)

# P(~F) = 0.5, P(D|~F) = 0.005, P(D|F) = 1, P(~F|DDDD) = P(DDDD|~F)P(~F) / P(DDDD)

(0.005)^4*0.5 / ((0.005)^4*0.5 + 1*0.5)


# P(A|S) = P(S|A)P(A) / P(S)
p0 <- 0.5

p0 <- 0.99
for (n in 1:10) {
  print(c(n, compute.posterior.coin(p0, n, n)))
}


n <- 4
p0 <- 0.99
compute.posterior.coin(p0, n, n)

n <- 4
p0 <- 0.5
compute.posterior.coin(p0, n, n)

# P(S) = 0.2, P(+|S) = 0.95, p(+|~S) = 0.1
# P(S|+) = P(+|S)P(S) / P(+)

# P(R|B1) = 0.7, P(R|~B1) = 0.3, P(B1) = 0.5
# P(B1|R) = P(R|B1)P(B1) / P(R)
p0 <- 0.5
for(n in 1:10) {
  p0 <- 0.7*p0 / (0.7*p0 + 0.3*(1-p0)) 
  print(c(n, p0))
}

(49+1)/(100+2)

compute.beta.bernoulli.posterior <- function(data, prior) {
  n <- data[1]
  y <- data[2]
  a <- prior[1]
  b <- prior[2]
  return (c(y+a, n-y+b))
}

compute.beta.bernoulli.posterior(c(10,3), c(2,2))

compute.gaussian.posterior <- function(n, ybar, sigma2, mu0, tao02) { # mean unknown
  tao_n2 <- 1 / (1/tao02 + n/sigma2)
  mu_n <- tao_n2*(n*ybar / sigma2 + mu0/tao02)
  return (c(mu_n, tao_n2))
}

#compute.gaussian.posterior2 <- function(n, v, v0) { # variance unknown
#  return (c(v0 + n, (v0*sigma2 + n*v) / (v0 + n))) # inverse-gamma
#}

compute.gaussian.posterior2 <- function(data, prior) { # variance unknown
  n_2 <- data[1] / 2
  v_2 <- data[2] / 2
  a <- prior[1]
  b <- prior[2]
  return (c(a + n_2, b + v_2))
}

y <- c(5.1, 4.4, 5.2, 5.3, 5.0)
n <- length(y)
ybar <- mean(y)
mu0 <- mean(y)
sigma2 <- 0.5 #var(y) * (n-1) / n
tao02 <- 1
compute.gaussian.posterior(n, ybar, sigma2, mu0, tao02)

compute.gamma.poisson.posterior <- function(data, prior) {
  n <- data[1]
  ybar <- data[2]
  a <- prior[1]
  b <- prior[2]
  return (c(a+n*ybar, b+n))
}

compute.gamma.exp.posterior <- function(data, prior) {
  n <- data[1]
  ybar <- data[2]
  a <- prior[1]
  b <- prior[2]
  return (c(a+n, b+n*ybar))
}

compute.gamma.poisson.posterior(c(2,1.5), c(3,5))

compute.beta.bernoulli.posterior(c(1000,350), c(22,36))
22 / (22 + 36)
372 / (372+686)

b = 0.7 / 0.15^2
a = b * 0.7
c(a, b)
c(a/b, a/b^2)

compute.gamma.exp.posterior(c(5,mean(1:5)), c(3,2))

compute.gaussian.posterior(5, mean(c(20.2,19.8,20.5,20.1,20.3)), 1, 20, 1)

y <- c(149,151,152,148,150,153,149,147,151,150)
n <- length(y)
v <- var(y) * (n-1)
compute.gaussian.posterior2(c(n, v), c(2,1))


library(MCMCpack)

# Define alpha parameters
alpha <- c(2, 3, 5)

# Generate 5 random samples
samples <- rdirichlet(5, alpha)
print(samples)

alpha <- c(2, 3, 5)

# Generate 5 random samples
samples <- rdirichlet(5, alpha)


sample <- rdirichlet(10000, c(601,301,301))
x <- sample[,3] # bus
n  <- length(x)
c(mean(x) - qt(0.975,n-1) * sd(x) / sqrt(n), mean(x) + qt(0.975,n-1) * sd(x) / sqrt(n))
hist(x)


samples1 <- rbeta(10000, 15+1,20-15+1)
samples2 <- rbeta(10000, 20+1,27-20+1)
hist(samples1, col='red', alpha=0.1)
hist(samples2, add=T, col='green', alpha=0.1)
hist(samples1 - samples2)


#rmultinom(n=800, size=10000, prob=rep(1/6,6))
sample1 <- rdirichlet(10000, c(320,380,100))
sample2 <- rdirichlet(10000, c(400,350,50))
hist(sample1[,1], col=scales::alpha('red',.5))
hist(sample2[,1], add=T, col=scales::alpha('green',.5))
x <- sample1[,1] - sample[,2]
hist(x)
sum(x > 0) / length(x)

sample <- rdirichlet(10000, c(601,301,301))
x <- sample[,3] # bus
n  <- length(x)
hist(x)