approx.rect <- function(g, w) {
  return(sum(w*g))
}

approx.trap <- function(g, w) {
  n <- length(g)
  return(w*(g[1]+g[n])/2 + sum(w*g[2:(n-1)]))
}

library(hash)

approx.rect2 <- function(x, g) {
  Nr <- length(x) - 1
  w <- (max(x) - min(x)) / Nr
  xmin <- 0 #min(x)
  print(w)
  s <- 0
  for (i in seq(0.0,Nr-1,w)) {
    print(paste(xmin + (i+1/2)*w))
    s <- s + w*g[[paste0(xmin + (i+1/2)*w)]]
  }
  return(s)
}

approx.trap2 <- function(x, g) {
  n <- length(g)
  Nr <- length(x) - 1
  xmin <- min(x)
  xmax <- max(x)
  w <- (xmax - xmin) / Nr
  print(w)
  s <- w*(g[[xmin]] + g[[xmax]]) / 2
  for (i in 1:(Nr-1))
    print(paste0(0.0+xmin + i*w))
  s <- s + w*g[[paste0(xmin + i*w)]]
  return(s)
}

#w <- 0.5

#x <- seq(0.25, 1.75, 0.5)
#g <- hash(x, c(0.0625, 0.5625, 1.5625, 3.0625))
#approx.rect(x, g)

#x <- seq(0, 2, 0.5)
#g <- hash(x, c(0, 0.25, 1, 2.25, 4))
#approx.trap(x, g)

x <- seq(0.25, 1.75, 0.5)
g <- c(0.625, 0.5625, 1.5625, 3.0625)
w <- 0.5
approx.rect(g, w)
x <- seq(0, 2, 0.5)
g <- c(0, 0.25, 1, 2.25, 4)
approx.trap(g, w)

integrate(function(x) x^3, 0, 4)

x <- c(0.5, 1.5, 2, 2.5)
g <- c(0.125, 3.375, 15.625, 42.875)
w <- 1
approx.rect(g, w)

x <- 0:4
g <- c(0, 1, 8, 27, 64)
approx.trap(g, w)