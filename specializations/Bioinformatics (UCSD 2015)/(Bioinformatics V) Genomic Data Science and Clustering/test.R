# maxdistance
#data <- matrix(c(2, 6, 4, 9, 5, 7, 6, 5, 8, 3), ncol=2, byrow=T)
#centers <- matrix(c(4, 5, 7, 4), ncol=2, byrow=T)
data <- matrix(c(2, 8, 2, 5, 6, 9, 7, 5, 5, 2), ncol=2, byrow=T)
centers <- matrix(c(3, 5, 5, 4), ncol=2, byrow=T)
maxdistance <- 0
for (i in 1:nrow(data)) {
  ds <- c()
  for (j in 1:nrow(centers)) {
    ds <- c(ds, sqrt(sum((data[i,] - centers[j,])^2)))
  }
  #print(ds)
  #print(which.min(ds))
  #print(min(ds))
  maxdistance <- max(maxdistance, min(ds))
}
print(maxdistance)

#distortion
data <- matrix(c(2, 6, 4, 9, 5, 7, 6, 5, 8, 3), ncol=2, byrow=T)
centers <- matrix(c(4, 5, 7, 4), ncol=2, byrow=T)
#data <- matrix(c(2, 8, 2, 5, 6, 9, 7, 5, 5, 2), ncol=2, byrow=T)
#centers <- matrix(c(3, 5, 5, 4), ncol=2, byrow=T)
distortion <- 0
for (i in 1:nrow(data)) {
  ds <- c()
  for (j in 1:nrow(centers)) {
    ds <- c(ds, sum((data[i,] - centers[j,])^2))
  }
  #print(ds)
  #print(which.min(ds))
  distortion <- distortion + min(ds)
}
distortion <- distortion / nrow(data)
print(distortion)
