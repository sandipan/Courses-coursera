eigen(matrix(c(5.4,4.5,4.5,6.1), nrow=2))
eigen(matrix(c(28.0,4.2,4.2,16.4), nrow=2))

1000*70*pi/180

emat <- matrix(c(123, 12, 20, 33, 97, 13, 15, 7, 121), ncol=3, byrow=T)
rowSums(emat)
colSums(emat)
sum(emat)
mean(diag(emat) / rowSums(emat))  # usr acc
mean(diag(emat) / colSums(emat))  # prod acc
sum(diag(emat)) / sum(emat)