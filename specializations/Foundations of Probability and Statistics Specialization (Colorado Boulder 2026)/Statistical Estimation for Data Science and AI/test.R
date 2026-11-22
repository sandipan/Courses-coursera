E <- function(f, p) {
  return (sum(f*p))
}

x <- c(20, 21.5, 26.8)
f <- c()
for (i in x) {
  f <- c(f, 20*i + 100)
}
p <- c(0.1, 0.7, 0.2)
E(f, p)

150*0.03
sqrt(150*0.03*0.97)

exp(-3)

mean(replicate(1000,
          {
            x <- rexp(1000, 0.014)
            mean(x > mean(x) + 2*sd(x))
          }))

x <- c(2781, 2900, 3013, 2856, 2888)
xbar <- mean(x)
s <- sd(x)
n <- length(x)
t95 <- qt(0.975, n-1)
c(xbar - t95*s/sqrt(n), xbar + t95*s/sqrt(n))

xbar <- 83.14
s <- 2.73
n <- 138
t90 <- qt(0.95, n-1)
c(xbar - t90*s/sqrt(n), xbar + t90*s/sqrt(n))

xbar <- 23.7
s <- sqrt(25.1)
#n <- 12
#t80 <- qt(0.9, n-1)
#c(xbar - t80*s/sqrt(n), xbar + t80*s/sqrt(n))
c(xbar - qnorm(0.9)*s/sqrt(n), xbar + qnorm(0.9)*s/sqrt(n))

(2*qnorm(0.975)*3/2.7)^2
#(2*qt(0.975, 20-1)*3/2.7)^2
#(2*qt(0.975, 21-1)*3/2.7)^2
#(2*qt(0.975, 22-1)*3/2.7)^2

# same known pop variances, normal distribution
n1 <- 10
x1bar <- 2.7
n2 <- 12
x2bar <- 3.2
s2 <- 0.8
z95 <- qnorm(0.95)
#t95 <- qt(0.95, n1+n2-2)
sf <- sqrt(s2*(1/n1+1/n2))
xbar <- x1bar-x2bar
c(xbar-z95*sf, xbar+z95*sf)
#c(xbar-t95*sf, xbar+t95*sf)

# same unknown pop variance, different known sample variances
n1 <- 10
x1bar <- 2.7
s12 <- 0.73
n2 <- 12
x2bar <- 3.2
s22 <- 0.80
sp2 <- ((n1-1)*s12 + (n2-1)*s22)/(n1+n2-2)
t95 <- qt(0.95, n1+n2-2)
sf <- sqrt(sp2*(1/n1+1/n2))
xbar <- x1bar-x2bar
c(xbar-t95*sf, xbar+t95*sf)

# different unknown pop variance, different known sample variances
n1 <- 138
x1bar <- 18.17
s12 <- 1.78
n2 <- 110
x2bar <- 21.66
s22 <- 3.21
df <- (s12/n1+s22/n2)^2 / ((s12/n1)^2/(n1-1) + (s22/n2)^2/(n2-1))
t975 <- qt(0.975, df)
sf <- sqrt(s12/n1+s22/n2)
xbar <- x1bar-x2bar
c(xbar-t975*sf, xbar+t975*sf)

n <- 250
p <- 112/250
c(p - qnorm(0.975)*sqrt(p*(1-p)/n), p + qnorm(0.975)*sqrt(p*(1-p)/n))

nA <- 150
pA <- 78/150
nB <- 150
pB <- 92/150
p <- pB - pA
s <- sqrt(pB*(1-pB)/nB + pA*(1-pA)/nA)
c(p - qnorm(0.975)*s, p + qnorm(0.975)*s)

x <- c(9.2229,8.3665,8.797058,10.2195,6.5629)
n <- length(x)
s <- sd(x)
c((n-1)*s^2/qchisq(0.96,n-1), (n-1)*s^2/qchisq(0.04,n-1))
#c((n-1)*s^2/qchisq(0.95,n-1), (n-1)*s^2/qchisq(0.05,n-1))
#c((n-1)*s^2/qchisq(0.975,n-1), (n-1)*s^2/qchisq(0.025,n-1))
