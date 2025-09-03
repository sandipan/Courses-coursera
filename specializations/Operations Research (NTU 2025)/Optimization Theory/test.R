simplex.matrix.iter <- function(A, b, c, X_B) {
  X <- 1:(ncol(A))
  X_N <- setdiff(X, X_B)
  A_B <- A[,X_B]
  A_N <- A[,X_N]
  c_B <- c[X_B]
  c_N <- c[X_N]
  A_B_1 <- solve(A_B)
  #A_B_1A <- A_B_1 %*% A
  A_B_1b <- solve(A_B, b)
  c_BA_B_1 <- c_B %*% A_B_1
  c_BA_B_1A_N_c_N <- c_BA_B_1%*%A_N - c_N
  z <- c_BA_B_1 %*% b
  print('c_B, c_N')
  print(c_B)
  print(c_N)
  print('X_B, X_N')
  print(X_B)
  print(X_N)
  print('A_B, A_N')
  print(A_B)
  print(A_N)
  print('X_B solution')
  x <- rep(0, ncol(A))
  x[X_B] <- A_B_1b
  print(x)
  print('z solution')
  print(z)
  print('reduced cost')
  print(c_BA_B_1A_N_c_N)
  res <- list()
  m <- min(c_BA_B_1A_N_c_N)
  if (m < 0) {
    e_ix <- X_N[which.min(c_BA_B_1A_N_c_N)]
    A_B_1A_e <- A_B_1 %*% A[,e_ix]
    m <- Inf
    l_ix <- -1
    for (i in 1:length(A_B_1b)) {
#      if ((A_B_1A[i,e_ix] > 0) & (A_B_1b[i] / A_B_1A[i,e_ix] < m)) {
 #       m <- A_B_1b[i] / A_B_1A[i,e_ix]
       if ((A_B_1A_e[i] > 0) & (A_B_1b[i] / A_B_1A_e[i] < m)) {
         m <- A_B_1b[i] / A_B_1A_e[i]
         l_ix <- i
      }
    }
    if (l_ix < 0) {
      res$unbounded <- TRUE
      return(res)
    }
    print(A_B_1A_e)
    print(A_B_1b)
    print(A_B_1b / A_B_1A_e)
    print(paste(e_ix, X_B[l_ix]))
    X_B[l_ix] <- e_ix
    A_B[,l_ix] <- A_B[,e_ix]
    c_B[l_ix] <- c[e_ix]
    print(X_B)
  } else {
    res$opt <- TRUE
  }
  res$A_B <- B
  res$c_B <- c_B 
  res$X_B <- X_B  # vars
  res$A_B_1b <- A_B_1b # values
  res$z <- z    # objective
  print(c(c_BA_B_1A_N_c_N, c_BA_B_1))
  #print(c(c_BB_1A_c))
  res$opt <- all(c_BA_B_1A_N_c_N >= 0) #all(c(c_BB_1, c_BB_1A_c) >= 0)
  res$unbounded <- FALSE
  return(res)
}


#A <- matrix(c(1,2,0,0,2,1,3,0,5,1,-3,2), nrow=3)
#b <- matrix(c(15,18,20), ncol=1)
#c <- c(4,3,2,3)
#X_B <- 4:6
#B <- diag(length(X_B))
#c_B <- rep(0, 3)

A <- matrix(c(-1,-1,3,1,2,1), ncol=2)
#A <- matrix(c(2,2,0,-1,1,1), ncol=2)
m <- nrow(A)
n <- ncol(A)
A <- cbind(A, diag(m))
b <- matrix(c(3,8,18), ncol=1)
#b <- matrix(c(4,8,3), ncol=1)
c <- c(1,3)
#c <- c(1,0)
c <- c(c, rep(0, m))

X_B <- (n+1):(n+m)
#X_B <- c(1,4,5)

for (i in 1:4) {
  res <- simplex.matrix.iter(A, b, c, X_B)
  X_B <- res$X_B
  print(res)
}


#X_B <- 3:5
#B <- diag(length(X_B))
#c_B <- rep(0, 3)

X_B <- c(2,4,5)
B <- diag(length(X_B))
B[,1] <- A[,2]
c_B <- rep(0, 3)
c_B[1] <- c[2]

c_B %*% solve(B, A) - c
  
for (i in 1:3) {
  res <- simplex.matrix.iter(A, b, c, B, c_B, X_B)
  X_B <- res$X_B
  B <- res$B
  c_B <- res$c_B
  print(i)
  print(res$X_B)  
  print(res$B_1b) 
  print(res$z)  
  #print(X_B)
  #print(B)
  #print(c_B)
  print(res$opt)
}

#install.packages('lpSolve')
library(lpSolve)
objective.fn <- c
const.mat <- A
const.dir <- c("<=", "<=", "<=")
const.rhs <- b
lp.solution <- lp("max", objective.fn, const.mat, 
                  const.dir, const.rhs, compute.sens=TRUE)
#lp.solution$objective
lp.solution$solution
lp.solution$objval

c(-3,0,0) %*% solve(matrix(c(1,2,1,0,1,0,0,0,1), ncol=3)) %*% matrix(c(-1,-1,3,1,0,0), ncol=2)
c(-3,0,0) %*% solve(matrix(c(1,2,1,0,1,0,0,0,1), ncol=3)) %*% matrix(c(-1,-1,3,1,0,0), ncol=2) - c(-1,0)
solve(matrix(c(1,2,1,0,1,0,0,0,1), ncol=3)) %*% c(-1,-1,3)
solve(matrix(c(1,2,1,0,1,0,0,0,1), ncol=3)) %*% c(3,8,18)


cB <- c(2,3)
cN <- c(0,0,0)
AB <- matrix(c(1,1,1,2),nrow=2)
AN <- matrix(c(1,0,1,0,0,1), nrow=2)
t(cB)%*%solve(AB)%*%AN - t(cN)
cN <- c(0,0,0,0)
AN <- matrix(c(1,0,-1,-2,1,0,0,1), nrow=2)
t(cB)%*%solve(AB)%*%AN - t(cN)
b <- c(4,6,1)
AB <- matrix(c(1,1,0,1,2,1,0,0,1),nrow=3)
solve(AB)%*%b
solve(AB, b)
AN <- matrix(c(1,0,1,1,0,0,0,1,0), nrow=3)
solve(AB)%*%AN


det(matrix(c(1,0,1,0,0,1,0,1,1,0,0,1,0,1,1,0), nrow=4))
det(matrix(c(1,0,1,0,1,0,1,0,1), nrow=4))

x <- seq(-1,1,0.01)
plot(x, 2*x^3-x^2-2*x+1, type='l')

eigen(matrix(c(0,0,1,0,1,0,1,0,0),nrow=3))
eigen(matrix(c(1,2,3,2,3,1,3,1,2),nrow=3))

# SVM problem
library(rSymPy)  
x <- Var("x") # beta1
y <- Var("y") # beta2
z <- Var("z") # alpha
# simplify the Lagrangian
sympy("simplify((x**2+y**2)/2-((2*x+y)/5)*(z+4*x+2*y-1)-((-x-3*y)/5)*(z+2*x+y-1)+(((2*x+y)/5)+((-x-3*y)/5))*(z+x+3*y+1))")


