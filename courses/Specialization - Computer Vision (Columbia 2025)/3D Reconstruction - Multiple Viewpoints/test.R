q_r <- function(M) {
  res <- qr(M)
  return (list(q=qr.Q(res), r=qr.R(res)))
}

#q_r(matrix(c(1,0,0,0,1,0,1,1,0,0,0,1),ncol=4))
#q_r(matrix(c(0.8,-0.6,0,0.6,0.8,0,0,0,1,0,1,1),ncol=4))
#q_r(matrix(c(1,0,0,0,3,0,0,0,5,0,0,0),ncol=4))
#q_r(matrix(c(1,0,0,1,0,1,0,0,0,0,1,0),ncol=3))
q <- matrix(c(1,0,0,0,1,0,1,1,0,0,0,1),ncol=4)
r <- matrix(c(1,0,0,0,0,1,0,0,0,0,1,0,1,1,0,0),ncol=4)
q %*% r


A <- matrix(c(1,2,-.25,0,-.5,0,.75,0,0,1,.5,0,1,2,3,1),nrow=4)
b <- c(3,2,1,1)
A %*% b