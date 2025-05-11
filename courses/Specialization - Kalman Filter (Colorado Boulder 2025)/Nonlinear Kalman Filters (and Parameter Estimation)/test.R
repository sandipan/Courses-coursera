# x_k = 3x_{k-1}^2 + 2u_{k-1} + sqrt(w_{k-1})
xk_1 <- 1
uk_1 <- -1
wk_1 <- 4
Ak_1 <- 6*xk_1
Bk_1 <- 1/(2*sqrt(wk_1))
Ak_1
Bk_1

# x_k = x_{k-1}^4/4 + u_{k-1}^3/3 + w_{k-1}^2/2
xk_1 <- 2
uk_1 <- -1
wk_1 <- 4
Bk_1 <- wk_1
Bk_1


# z_k = sqrt(x_k) + u_k + v_k
xk_ <- 16
uk <- 4
vkbar <- 0
zkbar <- sqrt(xk_) + uk + vkbar
zkbar

# z_k = x_k^2 + u_k + v_k
xk_ <- 4
uk <- 4
vkbar <- 0
zkbar <- xk_^2 + uk + vkbar
zkbar


# z_k = 3x_k^2 + 2u_k + v_k
xk <- 1
uk <- -1
vk <- -1
Sv <- 0.5
Sxk <- 1
Ck <- 6*xk
Ck
Dk <- 1
Dk
Lk <- Sxk*Ck/(Ck^2*Sxk + Dk^2*Sv)
Lk

# z_k = x_k^2 + u_k + v_k
xk <- 4
uk <- 4
vk <- 0
Sv <- 2
Sxk <- 1
Ck <- 2*xk
Ck
Dk <- 1
Lk <- Sxk*Ck/(Ck^2*Sxk + Dk^2*Sv)
Lk


m <- 50
k1 <- 4
k2 <- 60
d <- 0.25
b <- 2
dt <- 0.1
xkm <- matrix(rep(0,2), nrow=2)
xkp <- matrix(rep(0,2), nrow=2)
Ak <- matrix(c(1, dt, -k1*dt/m-3*k2*dt*xkp[1]^2/m, 1-b*dt/m), nrow=2, byrow=TRUE)
Ak
Bk <- matrix(c(0, dt/m), nrow=2)
Bk
Ck <- matrix(c(d/(d^2+xkm[1]^2), 0), nrow=2)
Ck


m <- 40
k1 <- 5
k2 <- 50
d <- 0.2
b <- 2
dt <- 0.2
xkm <- matrix(rep(0,2), nrow=2)
xkp <- matrix(rep(0,2), nrow=2)
Bk <- matrix(c(0, dt/m), nrow=2)
Bk

h <- sqrt(3)
L <- 1
am <- c((h^2-L)/h^2, .5/h^2, .5/h^2)
am
ac <- c((h^2-L)/h^2, .5/h^2, .5/h^2)
gam <- h
mx <- 1
Sx <- 1
X <- c(mx, mx+h*sqrt(Sx), mx-h*sqrt(Sx))
#Z <- X^2 + 2
Z <- X^3 + 1
mz <- sum(am*Z)
Sz <- sum(ac*(Z-mz)^2)
mz
Sz

chol(matrix(c(4,2,2,2), ncol=2))
Xxk_ <- matrix(c(0.5, 0.6,
          1.1, 0.2,
          0.7, 0.2,
          0.4, 0.7,
          1.0, 0.8), nrow=2)
am <- matrix(rep(0.2, 5), ncol=1)
xk_ <- Xxk_ %*% am
xk_
ac <- diag(0.2, 5)
Sxk_ <- (Xxk_ - c(xk_)) %*% ac %*% t(Xxk_ - c(xk_)) # recycling
Sxk_

Xxk_ <- matrix(c(0.6, 0,
                 0.3, 0.6,
                 0.8, 0.8,
                 0.9, 0.2,
                 0.4, 0.2), nrow=2)
am <- matrix(rep(0.2, 5), ncol=1)
xk_ <- Xxk_ %*% am
xk_
ac <- diag(0.2, 5)
Sxk_ <- (Xxk_ - c(xk_)) %*% ac %*% t(Xxk_ - c(xk_)) # recycling
Sxk_

h <- sqrt(3)
na <- 2 + 1 + 1
a0m <- (h*h - na) / (h*h)
a1m <- 1 / (2*h*h)
a0m
a1m