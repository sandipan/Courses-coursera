# Week 1

tbl <- data.frame(fs=c(203, 122), sc=c(118, 167), th=c(178, 528), cr=c(212, 673))
rownames(tbl) <- c('Survived', 'Didnot survive') 
colSums(tbl)
sum(tbl)
round(colSums(tbl) / sum(tbl),2)
rowSums(tbl)
round(rowSums(tbl) / sum(tbl),2)
round(203 / (203 + 122),2)
round((1/3)*(3/5+1/6+0),2)
#P(A|b) = P(b|A)P(A) / (P(b|A)P(A)+P(b|B)P(B)+P(b|C)P(C))
round((3/5)*(1/3) / ((3/5)*(1/3) + (1/6)*(1/3) + (0)*(1/3)),2)
round((1/6)*(1/3) / ((3/5)*(1/3) + (1/6)*(1/3) + (0)*(1/3)),2)

compute.posterior <- function(prior, likelihood) {
  return(round(prior*likelihood / sum(prior*likelihood),2))
}

prior <- rep(1/3,3)
likelihood <- c(3/5,1/6,0)
compute.posterior(prior, likelihood)

prior <- rep(1/3,3)
likelihood <- c(2/5,5/6,1)
compute.posterior(prior, likelihood)

I <- function(x, cond) {
  return(ifelse(cond, 1, 0))
}

x <- 0 #3
-5*I(x, (x>2)) + x*I(x, (x< (-1)))

E <- function(x, p) {
  return(sum(p*x))
}

x <- 0:3
p <- c(0.5,0.2,0.2,0.1)
E(p,x)

dbinom(0, 3, 0.2) # (0.8)^3
pbinom(0, 3, 0.2) # (0.8)^3
pbinom(2, 3, 0.2) # (0.8)^3

punif(0.2) - punif(-3) 
punif(3,2,6) - punif(2,2,6) 

pnorm(1) - pnorm(-1)
pnorm(1,0,sqrt(0.1)) - pnorm(-1,0,sqrt(0.1))

round(1 - pexp(1/3, 3),2)

mean(replicate(1000, {x <- rnorm(1000,1,5)
y <- rnorm(1000,-2,3)
mean(x+y)}))

5^2 + 3^2 + 2*(-5 - 1*(-2))


# Week 2
p <- 0.47
n <- 100
round(c(p - qnorm(0.975) * sqrt(p*(1-p)/n), p + qnorm(0.975) * sqrt(p*(1-p)/n)), 2)
round(1 / mean(c(2.0, 2.5, 4.1, 1.8, 4.0)),2)
mean(c(-1.2, 0.5, 0.8, -0.3))
(0.2)^5 *0.5 / ((0.2)^5 *0.5 + (0.7)^5 *0.5)
(0.7)^5 *0.5 / ((0.2)^5 *0.5 + (0.7)^5 *0.5)
#P(x=2|fair) = 6*(0.5)^4
#P(x=2|loaded head) =P(x=2|loaded tail) = 6*(0.7)^2*(0.3)^2
#P(fair|x=2) = 6*(0.5)^4*0.4 / (6*(0.5)^4*0.4 + 2*6*(0.7)^2*(0.3)^2*0.3)
qnorm(0.025)
qnorm(0.975)

pbeta(0.2, 1 + 3, 1 + 24 - 3)
#beta(1 + 0, 1 + 2 - 0) mean = 1/4 prob(H) = 1/4 prob (HH) = 1/16 
#beta(1 + 1, 1 + 3 - 1) mean = 2/5 prob(H) = 2/5
# prob(HH) = 1/4 * 2/ 5 = 1/10
# f(p|x) = (0.4)^2*0.5*I(p=0.6) + (0.6)^2*0.5*I(p=0.4) / ((0.4)^2*0.5 + (0.6)^2*0.5) = 0.3076923I(p=0.6) + 0.6923077I(p=0.4)
# f(Y2=1,Y1=1|p) = 0.3076923 * (0.6)^2 + 0.6923077 * (0.4)^2

# Week 3
pbeta(0.5, 1, 5)
x <- seq(0,1,length=100)
plot(x, dbeta(x, 1, 5), type='l')
mean(rbeta(1000,1,5))
qbeta(0.975, 8, 16, lower.tail = FALSE)
qbeta(0.975, 8, 16, lower.tail = TRUE)
pbeta(0.35, 8, 16)
plot(x, dbeta(x,2,2), type='l')
plot(x, dbeta(x,8,16), type='l')  # (2 + 6, 2 + 20 - 6)
plot(x, dbeta(x,8,21), type='l') # (8 + 0, 16 + 5 - 0)    (2 + 6, 2 + 25 - 6)
pbeta(0.35, 8, 21)

x <- seq(0,20,length=21)
plot(x, dgamma(x, 67, 6), type='l', lty=1)
lines(x, dgamma(x, 8, 1), lty=2)
lines(x, dpois(x, 8), lty=3)
67/6
qgamma(0.05, 67, 6)
qgamma(0.95, 67, 6)
lines(x, dgamma(x, 176, 16), lty=4) # (8 + 59 + 109, 1 + 5 + 10)
6.004 / 120.04
5 / (5+9)

a = 1 + 5
b = 20 + 12 + 15 +8 + 13.5 + 25
(a/b)
pgamma(0.1, a, b)

x <- seq(0,1,length=100)
plot(x, pgamma(x, 1,20), type='l')
lines(x, pgamma(x, 1/20, 1), col='red')
a = 1 + 8
b = 30 + sum(c(16, 8, 114, 60, 4, 23, 30, 105))
qgamma(0.95, a, b)

y <- seq(0,120,length=1000)
plot(y, b^a*a/(b + y)^(a+1), type='l')

# Week 4
n <- 5
x <- c(94.6, 95.4, 96.2, 94.9, 95.9)
xbar <- mean(x)
w <- 1
m <- 100  
sigma <- sqrt(0.25)
post.mu <- (n*xbar + w*m) / (n + w)
post.sigma <- sigma^2 / (n + w)
qnorm(0.975, post.mu, sqrt(post.sigma))
pnorm(100, post.mu, post.sigma)

a=3
b=200
z <- rgamma(n=1000, shape=a, rate=b)
x <- 1/z
mean(x)

z <- rgamma(1000, shape=16.5, rate=6022.9)
sig2 <- 1/z
mu <- rnorm(1000, mean=609.3, sd=sqrt(sig2/27.1))
quantile(x=mu, probs=c(0.025, 0.975))
muB <- mu

#a=a+n/2
a <- 3+30/2
#b=b+n???12s2+wn2(w+n)(y¯???m)2
b <- 200 + 403.1*(30-1)/2 + (622.8 - 500)^2*(0.1*30) / (2*(0.1+30))
#m'=ny¯+wmw+n
m <- (30*622.8 + 0.1*500)/(0.1+30)

z <- rgamma(n=1000, shape=a, rate=b)
x <- 1/z
muA <- rnorm(1000, mean=m, sd=sqrt(sig2/30.1))

sum( muA > muB ) / 1000

x <-  c(94.6, 95.4, 96.2, 94.9, 95.9)
xbar <- mean(x)
n <- length(x)
xbar
var(x)
m <- 0
sigma <- sqrt(0.25)
sigmam <- 10^6
w <- sigma / sigmam
(n*xbar + w*m) / (n + w)
(sigma^2) / (n + w)
x <- seq(0,1,length=100)
plot(x, dbeta(x,1/2,1/2), col='red', type='l')

setwd('C:/courses/Coursera/Current/bayesian-statistics/Week4/')
dat <- read.table('pgalpga2008.dat', col.names=c('D','A', 'FM'))
datF <- subset(dat, FM==1, select=1:2)
datM <- subset(dat, FM==2, select=1:2)
ggplot(dat, aes(x=D, y=A)) + geom_point() + facet_wrap(~FM)
m <- lm(A~D, datF)
summary(m)
predict(m, data.frame(D=260))
predict(m, data.frame(D=260), interval='predict')

dat[dat$FM==1,]$FM <- 0
dat[dat$FM==2,]$FM <- 1
head(dat)
m <- lm(A~D+FM, dat)
summary(m)
predict(m, data.frame(D=260))
predict(m, data.frame(D=260), interval='predict')
plot(fitted(m), residuals(m))

# beta
x <- seq(0,1,length=100)
plot(x, dbeta(x,10,10), col='green', type='l')
lines(x, dbeta(x,5,5), col='cyan')
lines(x, dbeta(x,2,2), col='blue')
lines(x, dbeta(x,1,1))
lines(x, dbeta(x,1/2,1/2), col='red')

x <- seq(0,1,length=100)
plot(x, dbeta(x,3,1), col='green', type='l')
lines(x, dbeta(x,4,2), col='brown')
lines(x, dbeta(x,2,1), col='cyan')
lines(x, dbeta(x,2,0), col='magenta')
lines(x, dbeta(x,1,0), col='blue')
lines(x, dbeta(x,0,0))
lines(x, dbeta(x,1,2), col='red')
lines(x, dbeta(x,1,3), col='pink')
lines(x, dbeta(x,2,4), col='yellow')

# gamma
x <- seq(0,1,length=100)
plot(x, dgamma(x,10,10), col='green', type='l')
lines(x, dgamma(x,5,5), col='cyan')
lines(x, dgamma(x,2,2), col='blue')
lines(x, dgamma(x,1,1))
lines(x, dgamma(x,1/2,1/2), col='red')

x <- seq(0,1,length=100)
plot(x, dgamma(x,1,2), col='green', type='l')
lines(x, dgamma(x,4,2), col='brown')
lines(x, dgamma(x,3,1), col='cyan')
lines(x, dgamma(x,2,0), col='magenta')
lines(x, dgamma(x,1,0), col='blue')
lines(x, dgamma(x,0,0))
lines(x, dgamma(x,2,1), col='red')
lines(x, dgamma(x,1,3), col='pink')
lines(x, dgamma(x,2,4), col='yellow')

