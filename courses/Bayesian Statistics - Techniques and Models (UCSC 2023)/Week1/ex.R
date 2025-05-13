T <- matrix(c(0,1,0.3,0.7), nrow=2, byrow=TRUE)
S <- matrix(c(1,0), nrow=1)
for (i in 2:4) {
  print(i)
  S <- S %*% T
  print(S)
}

p <- 0.7
(1-p) + p*p

S <- matrix(c(1,0), nrow=1)
for (i in 1:100) {
  S <- S %*% T
}
print(S)
# compute the left-eigenvectors, eigen() computes the right ones, need to transpose T
state.vec <- matrix(Re(eigen(t(T))$vectors[, 1]), nrow=1) 
state.vec <- state.vec / sum(state.vec) #/ norm(state.vec, type='F') # normalize
state.vec

T1 <- matrix(rep(state.vec,2), nrow=2, byrow=TRUE)
S %*% T %*% T %*% T 