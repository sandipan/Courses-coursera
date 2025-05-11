is.psd <- function(M) { #Sylvester's criterion
  n <- ncol(M)
  for (i in 1:n) {
    d <- ifelse(i == 1, M[1,1], det(M[1:i,1:i]))
    print(d)
    if (d < 0) {
      return (F)
    }
  }
  return (T)
}

is.pd <- function(M) {
  n <- ncol(M)
  for (i in 1:n) {
    d <- ifelse(i == 1, M[1,1], det(M[1:i,1:i]))
    print(d)
    if (d <= 0) {
      return (F)
    }
  }
  return (T)
}

is.pd(matrix(c(1,2,2,1),ncol=2))
is.pd(matrix(c(2,-1,0,-1,2,-1,0,-1,2),ncol=3))
is.pd(matrix(c(2,6,6,20),ncol=2))
is.pd(matrix(c(-1),ncol=1))
is.pd(matrix(c(2,6,6,18),ncol=2))

Higham.nearest.psd <- function(Sig) {
  res <- svd(Sig)
  H <- res$v*res$d*t(res$v)
  return((Sig + t(Sig) + H + t(H)) / 4)
}

Higham.nearest.psd(matrix(-1, ncol=1))


# ARE
#A*Sx + Sx*t(A) + Bw*Sw*t(Bw) - Sx*t(C)*solve(Sv)*C*Sx = 0
A <- -0.1
Bw <- 1
C <-  1
Sv <- 0.1
Sw <- 0.1
#(C^2/Sv)*Sx^2 - (2*A) * Sx - Sw*Bw^2 = 0
Sx = ((2*A) + sqrt(4*A^2 + 4*C^2*Bw^2*Sw/Sv)) / (2*C^2/Sv)
Sx
polyroot(c(-Sw*Bw^2, -2*A, C^2/Sv))
Sx <- 1
L <- Sx*C/Sv
L
L <- 1
s <- -(L*C-A)
s

zk = 0.1
Szk = 0.1
nees = zk^2/Szk
nees

Sx <- 0.1
C <- 1
Sv <- 0.1
L <- Sx*C/Sv
L

A <- -0.1
C <- 1
L <- 0.1
s <- -(L*C-A)
s

sw <- 0.2
Sv <- 0.1
dt <- 0.1

sw <- 0.1
Sv <- 0.2
dt <- 0.5

l <- sw * (dt)^2 / sqrt(Sv)
l

a <- -(1/8)*(l^2+8*l - (l+4)*sqrt(l^2+8*l))
a

b <- (1/4)*(l^2+4*l - l*sqrt(l^2+8*l))
b

44 / 20