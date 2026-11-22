10/81

mean(replicate(10000, {
            s <- sample(0:2, 5, replace=TRUE)
            ns <- rep(0, 3)
            for (i in 0:2) {
              ns[i+1] = sum((s == i))
            }
            found <- as.integer((ns[1] == 2) && (ns[2] == 2) && (ns[3] == 1))
            found
          }
          ))

1-(2/3)^5
211/243

mean(replicate(10000, {
  s <- sample(0:2, 5, replace=TRUE)
  sum(s == 0) > 0
}
))

5/9
mean(replicate(10000, {
  hand <- 2:4
  s <- sample(1:6, 2, replace=TRUE)
  hand <- sort(c(hand, s))
  uhand <- unique(hand)
  ((length(hand) == 5) && (all(hand == 1:5) || all(hand == 2:6) || all(hand == c(1,2,3,4,6)))) ||
  ((length(uhand) == 4) && (all(uhand == 1:4) || all(uhand == 2:5)))
  #all(hand == 1:5) || all(hand == 2:6) || all(hand == c(1,2,3,4,6)) || (sum(unique(hand)) == 10) || (sum(unique(hand)) == 14)
}
))

8*factorial(5)/6^5
mean(replicate(10000, {
  hand <- sample(1:6, 5, replace=TRUE)
  hand <- sort(hand)
  uhand <- unique(hand)
  ((length(hand) == 5) && (all(hand == c(1,2,3,4,6)) ||  all(hand == c(1,3,4,5,6)))) ||
  ((length(uhand) == 4) && (all(uhand == 1:4) || all(uhand == 2:5) || all(uhand == 3:6)))
}
))

0.7 + 0.5 - 0.6*0.7

6*0.24^2
dbinom(2, 4, 0.6)

dbinom(1, 3, 0.6)

1 - (0.6*0.7) / (0.6*0.7 + 0.1*0.3)
(0.1*0.3) / (0.6*0.7 + 0.1*0.3)

dbinom(2, 5, 0.9)
5*0.9
5*0.9*0.1

(1-0.06)^(2-1)*0.06
dgeom(2, 0.06)
dgeom(1, 0.06)
1/0.06
(1-0.06)/0.06^2

1-(0.17+0.07+0.13-0.06-0.02-0.11+0.01)
0.17-0.06-0.11+0.01
0.07-0.06-0.02+0.01
0.13-0.11-0.02+0.01
0.06-0.01 + 0.02-0.01 + 0.11-0.01

x <- 0:3
p <- c(0.81,0.02,0.16,0.01)
sum(p*x)
sum(p*x^2) - (sum(p*x))^2
sqrt(sum(p*x^2) - (sum(p*x))^2)

choose(30,4)*(0.05)^4*(0.95)^26
dbinom(4, 30, 0.05)
0.95^3*0.05
dgeom(3, 0.05)
3*(0.05)^2*(0.95)^2
dnbinom(2,2,0.05)

cdf <- function(x) {
  #if (x - as.integer(x) == 0) {
  #  return(NA)
  #} else 
  if (x < 1) {
    return(0)
  } else if (x < 2) {
    return(1/9)
  } else if (x < 3) {
    return(3/9)
  } else if (x < 4) {
    return(4/9)
  } else if (x < 5) {
    return(6/9)
  } else if (x < 6) {
    return(7/9)
  } else {
    return(1)
  }
}

cdf <- Vectorize(cdf)
x <- seq(0,7, 0.01)
plot(x, cdf(x), xlab='x', ylab='P(X<x)', main='CDF', col='blue') #, lwd=2) #type='l',
points(1:6, cdf(0:5), col='red', lwd=5)
grid()

x <- 1:6
p <- c(1/9,2/9,1/9,2/9,1/9,2/9)
sum(p*x)

choose(15,4)*(0.4)^4*(0.6)^11
dbinom(4, 15, 0.4)

ks <- 0:4
sum(choose(15,ks)*(0.4)^ks*(0.6)^(15-ks))
pbinom(4, 15, 0.4)



qnorm(0.1, 12, 2, lower.tail = FALSE)
pnorm(12+2*1.5, 12, 2) - pnorm(12-2*1.5, 12, 2)
integrate(function(x) exp(-(x-12)^2/(2*4))/(sqrt(2*pi)*2), 12-2*1.5, 12+2*1.5)

integrate(function(x) 20/x^2, 10, 20)
integrate(function(x) 20/x^2, 10, 15)
integrate(function(x) x*20/x^2, 10, 20)
20*log(2)

x <- 0:10
sum(1/11*(x*10 - (10-x)*5))
#Ex
e = sum(x/length(x))
#E[x*10 + (10-x)*(-5)]
15*e - 50

(1-exp(-12/10))^3

cov <- function(x, y, px, py, pxy) {
  mx <- sum(x*px)
  my <- sum(y*py)
  sx <- sqrt(sum((x-mx)^2*px))
  sy <- sqrt(sum((y-my)^2*py))
  cv = 0
  for (i in x) {
    for (j in y) {
      #print(paste(i, j, pxy[[paste(i,j,sep=',')]]))
      cv = cv + (i-mx)*(j-my)*pxy[[paste(i,j,sep=',')]]
    }
  }
  rho = cv / (sx*sy)
  return(c(cv, rho))
}

x <- c(1,5)
y <- c(1, 4, 16)
px <- c(0.5, 0.5)
py <- c(0.3, 0.4, 0.3)
pxy <- list()
pxy[['1,1']] = 0.2
pxy[['5,1']] = 0.1
pxy[['1,4']] = pxy[['5,16']] = 0.25
pxy[['5,4']] = 0.15
pxy[['1,16']] = 0.05
cov(x, y, px, py, pxy)

pnorm((12.04-12)/0.2) - pnorm((11.97-12)/0.2)

pnorm(0.6, 1/2, 1/sqrt(12*30)) - pnorm(0.5, 1/2, 1/sqrt(12*30))
1-pnorm(0, 2, sqrt(5))

100^2/12