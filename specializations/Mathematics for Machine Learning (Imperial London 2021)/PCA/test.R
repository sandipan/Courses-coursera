inner.product <- function(x, y, A) {
  return(t(x)%*%A%*%y)
}

norm <- function(x, A) {
  return(sqrt(t(x)%*%A%*%x))
}

angle.in.radian <- function(x, y, A=diag(length(x))) {
  acos(inner.product(x, y, A)/(norm(x, A)*norm(y, A)))
}

projection.matrix.1d <- function(b) {
  (b%*%t(b)) / as.numeric((t(b)%*%b))
}

projection.1d <- function(x, b) {
  projection.matrix.1d(b)%*%x
}

x <- c(1,1)
y <- c(-1,1)
A <- matrix(c(2,-1,-1,4),nrow=2)
angle.in.radian(x,y,A)

x <- c(0,-1)
y <- c(1,1)
A <- matrix(c(1,-1/2,-1/2,5),nrow=2)
angle.in.radian(x,y,A)

x <- c(2,2)
y <- c(-2,-2)
A <- matrix(c(2,1,1,4),nrow=2)
angle.in.radian(x,y,A)

x <- c(1,1)
y <- c(1,-1)
A <- matrix(c(1,0,0,5),nrow=2)
angle.in.radian(x,y,A)

x <- c(1,1,1)
y <- c(2,-1,0)
A <- matrix(c(1,0,0,0,2,-1,0,-1,3),nrow=3)
angle.in.radian(x,y,A)

b <- c(1,2,2)
projection.matrix.1d(matrix(b, ncol=1))

x <- c(1,1,1)
x_ <- projection.1d(matrix(x, ncol=1), matrix(b, ncol=1))

x <- matrix(x, ncol=3)
x_ <- t(x_)
dist(x, x_)

