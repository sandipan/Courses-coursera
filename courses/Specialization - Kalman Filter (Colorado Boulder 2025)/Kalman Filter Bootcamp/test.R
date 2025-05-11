integrate(Vectorize(function(x) x), 1, 2)
integrate(Vectorize(function(x) x^2/12), -6, 6)
integrate(Vectorize(function(x) x/12), -6, 6)
integrate(Vectorize(function(x) x^2/6), -3, 3)
integrate(Vectorize(function(x) x/2), 0, 2)

n <- 2
x <- c(0,1)
xbar <- c(1,0)
S <- matrix(c(2,0,0,1),nrow=2)
1/((2*pi)^(n/2)*sqrt(det(S)))*exp(-0.5*t(x-xbar)%*%solve(S)%*%(x-xbar))

Ad <- 0.9 #0.5 
Bd <- 0.2 #0.1
Sx0 <- 2 #1
Sw <- 1 #0.5
x0 <- -1 #1
u0 <- 5 #10
x1 <- Ad*x0 + Bd*u0
x1
Sx1 <- Ad*Sx0*t(Ad) + Sw
Sx1

Sx <- c(Sx0)
for (i in 1:1000) {
  Sx0 <- Ad*Sx0*t(Ad) + Sw
  Sx <- c(Sx, Sx0)
}
plot(1:length(Sx), Sx, pch=19)
Sx


A <- -0.2 #-0.1
B <- 0.5 #0.2
Bw <- 1
Sx0 <- 2 #1
Sw <- 1 #2
x0 <- 10 #1
u0 <- 2
x0dot <- A*x0 + B*u0
x0dot
Sx0dot <- 2*A*Sx0 + Bw^2*Sw
Sx0dot
Sx <- -Bw^2*Sw/(2*A)
Sx

library(expm)
A <- -0.2 #-0.1
B <- 0.5 #0.1
C <- 3
D <- 0
Bw <- 1
Sw <- 1 #0.5
Sv <- 0.02 #0.01
dt <- 0.1
Ad <- t(expm(t(A)*dt))
Ad
#c22 <- t(Ad)
#c11 <- exp(-A*dt)
Z = matrix(c(-A, Bw*Sw*t(Bw), 0*A, t(A)), nrow=2, byrow=TRUE)
CC = expm(Z*dt)
c11 = CC[1,1] 
c12 = CC[1,2]
c21 = CC[2,1]
c22 = CC[2,2]

Sigw <- t(c22)*c12
Sigw
Sigv <- Sv / dt
Sigv