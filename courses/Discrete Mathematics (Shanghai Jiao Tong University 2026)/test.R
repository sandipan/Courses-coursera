board <- matrix(rep(c(rep(0:1,4), rep(1:0,4)),4), nrow=8)
image(board, col=c('orange', 'black'))
text(0,0, 1)
library(gplots)
heatmap.2(board,
          cellnote = matrix(rep(0:1,32),nrow=8, byrow=TRUE),
          notecol="green",      # change font color of cell labels to black
          density.info="none",  # turns off density plot inside color legend
          trace="none",         # turns off trace lines inside the heat map
          col=c('black','orange'),       # use on color palette defined earlier
          dendrogram="none",
          key = FALSE,
          Rowv=NULL,
          Colv=NULL)   

compute_g <- function(n) {
  g <- rep(0, n)
  g[1] <- 0
  g[2] <- 1
  for (i in 3:n) {
    g[i] <- ifelse(i %% 2, g[i-1], g[i / 2] + i/2)
  }
  return(g)
}
compute_w <- function(n) {
  w <- rep(0, n)
  w[1] <- 1
  w[2] <- 1
  for (i in 3:n) {
    w[i] <- ifelse(i %% 2, w[i-1]+1, w[i / 2])
  }
  return(w)
}
g <- compute_g(65)
#compute_w(65)
for (x in g) {
  x <- rev(intToBits(x))
  x <- paste(as.integer(x), collapse = "")
  print(x)
}

g_func <- function(n) {
  return (ifelse(n == 1, 0, ifelse(n == 2, 1, ifelse(n %% 2, g_func(n-1), g_func(n/2) + n/2))))
}

w_func <- function(n) {
  return (ifelse(n == 1, 1, ifelse(n == 2, 1, ifelse(n %% 2, w_func(n-1)+1, w_func(n/2)))))
}

b_func <- function(n) {
  return (ifelse(n == 0, '', ifelse(n %% 2, paste0(b_func(n%/%2),'1'), paste0(b_func(n%/%2),'0'))))
}

for (n in 1:65) {
  print(paste(paste(as.integer(rev(intToBits(n))), collapse = ""), paste(as.integer(rev(intToBits(g_func(n)))), collapse = "")))
}

for (n in 1:65) {
  print(paste(paste(as.integer(rev(intToBits(n))), collapse = ""), b_func(n)))
}

for (n in 1:65) {
  print(paste(g_func(n), n-w_func(n)))
}

for (k in 0:7) {
  print(paste(b_func(1152921504606846987), b_func(k)))
}

n <- base::strtoi('10000000000000011', base = 2)
print(paste(paste(as.integer(rev(intToBits(n))), collapse = ""), paste(as.integer(rev(intToBits(g_func(n)))), collapse = "")))

d <- base::strtoi('10000000000000011', base = 2)
g <- compute_g(d)
g[d]
paste(as.integer(rev(intToBits(g[d]))), collapse = "")
#Vectorize(compute_w)(Vectorize(compute_g)(65))

n <- 20
k <- 0:20
sum(k**2*choose(n, k))
n*(n+1)*2^(n-2)


#plot(compute_g(65), compute_w(65), pch=19)

x <- seq(-10,10,0.01)
plot(x, exp(sin(x)), type='l')