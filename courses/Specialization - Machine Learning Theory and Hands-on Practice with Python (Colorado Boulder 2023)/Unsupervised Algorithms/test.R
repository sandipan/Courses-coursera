3/sqrt(6)/sqrt(5)
A <- rbind(c(1,3),c(2,6),c(4,12),c(3,9))
eigen(t(A) %*% A)
eigen(A %*% t(A))