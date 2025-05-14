compute_slope_intercept <- function(s) {
  return (list(m = (s$y2 - s$y1) / (s$x2 - s$x1), 
               c = (s$y1*s$x2 - s$y2*s$x1) / (s$x2 - s$x1)))
  #return (c((s$y2 - s$y1) / (s$x2 - s$x1), (s$y1*s$x2 - s$y2*s$x1) / (s$x2 - s$x1)))
}

check_intersection <- function(s1, s2) {
  res <- compute_slope_intercept(s1)
  m1 <- res$m
  c1 <- res$c
  res <- compute_slope_intercept(s2)
  m2 <- res$m
  c2 <- res$c
  if (m1 == m2) return (list(intersect=F, p = NULL))
  if (max(c(s1$x1, s1$x2)) < min(c(s2$x1, s2$x2))) return (list(intersect=F, p = NULL))
  if (max(c(s2$x1, s2$x2)) < min(c(s1$x1, s1$x2))) return (list(intersect=F, p = NULL))
  if (max(c(s1$y1, s1$y2)) < min(c(s2$y1, s2$y2))) return (list(intersect=F, p = NULL))
  if (max(c(s2$y1, s2$y2)) < min(c(s1$y1, s1$y2))) return (list(intersect=F, p = NULL))
  return (list(intersect = T, 
               p = c((c2 - c1) / (m1 - m2), (m1*c2 - m2*c1) / (m1 - m2))))
}


find_intersection <- function(s1, s2) {
  res <- check_intersection(s1, s2)
  #ifelse(res$intersect, res$p, c(NULL, NULL))
  if (res$intersect) {
    return (res$p)
  } 
  return (NULL)
}

df <- as.data.frame(matrix(c(1, 1, 8, 10,
                                2, 7, 10, 3,
                                4, 8, 5, 2,
                                6, 4, 7, 9), nrow=4, byrow=T))
names(df) <- c('x1', 'y1', 'x2', 'y2')
df
n <- nrow(df)
for (i in 1:(n-1)) {
  for (j in (i+1):n) {
    print(find_intersection(df[i,], df[j,]))
  }
}

print(find_intersection(df[1,], df[3,]))
print(find_intersection(df[2,], df[3,]))
print(find_intersection(df[2,], df[4,]))
print(find_intersection(df[1,], df[2,]))
print(find_intersection(df[3,], df[4,]))
print(find_intersection(df[1,], df[4,]))


df2 <- df
df2$id <- as.factor(1:nrow(df))
library(ggplot2)
ggplot(df2) + geom_segment(aes(x = x1, y = y1, xend = x2, yend = y2, col=id))

read.file <- function(path) {
  lines <- readLines(path)
  mn <- as.integer(unlist(strsplit(lines[1], ' ')))
  n <- mn[1]
  m <- mn[2]
  x <- c()
  y <- c()
  for (i in 2:(n+1)) {
    xy <- as.integer(unlist(strsplit(lines[i], ' ')))
    x <- c(x, xy[2])
    y <- c(y, xy[3])
  }
  df <- NULL
  for (i in (n+2):(n+m+1)) {
    tri <- as.integer(unlist(strsplit(lines[i], ' ')))
    df <- rbind(df, data.frame(p1=tri[1]+1, p2=tri[2]+1, p3=tri[3]+1))
  }
  return(list(x=x, y=y, tri=df))
}

plot.triangles <- function(tri, x, y, toff=5) {
  seg.df <- NULL
  for (i in 1:nrow(tri)) {
    p1 <- tri[i,]$p1
    p2 <- tri[i,]$p2
    p3 <- tri[i,]$p3
    seg.df <- rbind(seg.df, data.frame(id=p1, x1=x[p1], y1=y[p1], x2=x[p2], y2=y[p2]))
    seg.df <- rbind(seg.df, data.frame(id=p2, x1=x[p2], y1=y[p2], x2=x[p3], y2=y[p3]))
    seg.df <- rbind(seg.df, data.frame(id=p3, x1=x[p3], y1=y[p3], x2=x[p1], y2=y[p1]))
  }
  head(seg.df)
  print(ggplot(seg.df) + geom_segment(aes(x = x1, y = y1, xend = x2, yend = y2)) + 
                   geom_point(aes(x1, y1)) + geom_text(aes(x1+toff, y1+toff, label=id-1)) + 
                   xlab('x') + ylab('y') + 
                   theme_bw())
}

flip.edge <- function(df, rem.tr.ids, add.tr.df) {
  df <- df[-rem.tr.ids,]
  df <- rbind(df, add.tr.df)
  rownames(df) <- 1:nrow(df)
  return(df)
}

add.edge <- function(df, add.tr.df) {
  df <- rbind(df, add.tr.df)
  return(df)
}

rem.edge <- function(df, rem.tr.ids) {
  df <- df[-rem.tr.ids,]
  rownames(df) <- 1:nrow(df)
  return(df)
}

library(animation)

prob1 <- function() {
  res <- read.file('G:/courses/coursera/Past/Topics/Algorithms/Geometric Algorithms/Week2/inputTriangulation4.txt')
  res
  tri <- res$tri
  
  saveGIF({
    plot.triangles(tri, res$x, res$y)
    i <- 0
    
    #tri <- flip.edge(tri, c(7,8), data.frame(p1=c(3,4), p2=c(6,6), p3=c(8,8)))
    tri <- rem.edge(tri, c(7,8))
    plot.triangles(tri, res$x, res$y)
    tri <- add.edge(tri, data.frame(p1=c(3,4), p2=c(6,6), p3=c(8,8)))
    plot.triangles(tri, res$x, res$y)
    tri
    i <- i + 1
    
    #tri <- flip.edge(tri, c(12,6), data.frame(p1=c(3,8), p2=c(6,6), p3=c(9,9)))
    tri <- rem.edge(tri, c(12,6))
    plot.triangles(tri, res$x, res$y)
    tri <- add.edge(tri, data.frame(p1=c(3,8), p2=c(6,6), p3=c(9,9)))
    plot.triangles(tri, res$x, res$y)
    tri
    i <- i + 1
    
    #tri <- flip.edge(tri, c(11,13), data.frame(p1=c(4,4), p2=c(6,8), p3=c(9,9)))
    tri <- rem.edge(tri, c(11,13))
    plot.triangles(tri, res$x, res$y)
    tri <- add.edge(tri, data.frame(p1=c(4,4), p2=c(6,8), p3=c(9,9)))
    plot.triangles(tri, res$x, res$y)
    tri
    i <- i + 1
    
    #tri <- flip.edge(tri, c(3,13), data.frame(p1=c(1,1), p2=c(4,4), p3=c(9,8)))
    tri <- rem.edge(tri, c(3,13))
    plot.triangles(tri, res$x, res$y)
    tri <- add.edge(tri, data.frame(p1=c(1,1), p2=c(4,4), p3=c(9,8)))
    plot.triangles(tri, res$x, res$y)
    tri
    i <- i + 1
    
    #tri <- flip.edge(tri, c(12,11), data.frame(p1=c(1,1), p2=c(9,4), p3=c(6,6)))
    tri <- rem.edge(tri, c(12,11))
    plot.triangles(tri, res$x, res$y)
    tri <- add.edge(tri, data.frame(p1=c(1,1), p2=c(9,4), p3=c(6,6)))
    plot.triangles(tri, res$x, res$y)
    tri
    i <- i + 1
    
    #tri <- flip.edge(tri, c(2,1), data.frame(p1=c(1,1), p2=c(5,5), p3=c(9,10)))
    tri <- rem.edge(tri, c(2, 1))
    tri <- rbind(tri, data.frame(p1=c(5), p2=c(10), p3=c(5)))
    plot.triangles(tri, res$x, res$y)
    tri <- add.edge(tri, data.frame(p1=c(1,1), p2=c(5,5), p3=c(9,10)))
    plot.triangles(tri, res$x, res$y)
    tri
    i <- i + 1
    i
  }, interval = 0.5)  
  
}
prob1()


prob2 <- function() {
  res <- read.file('G:/courses/coursera/Past/Topics/Algorithms/Geometric Algorithms/Week2/inputTriangulation5.txt')
  print(res)
  tri <- res$tri
  plot.triangles(tri, res$x, res$y)
  
  i <- 0
  
  tri <- flip.edge(tri, c(6,8), data.frame(p1=c(4,4), p2=c(5,1), p3=c(9,9)))
  plot.triangles(tri, res$x, res$y)
  print(tri)
  i <- i + 1
  
  tri <- flip.edge(tri, c(3,4), data.frame(p1=c(4,4), p2=c(7,10), p3=c(6,6)))
  plot.triangles(tri, res$x, res$y)
  print(tri)
  i <- i + 1

  tri <- flip.edge(tri, c(3,12), data.frame(p1=c(5,5), p2=c(7,4), p3=c(6,6)))
  plot.triangles(tri, res$x, res$y)
  print(tri)
  i <- i + 1
  
  i
}
prob2()


prob3 <- function(n=5) {
  x <- c()
  y <- c()
  for (i in 1:n) {
    x <- c(x, i)
    y <- c(y, i^2)
  }
  tri <- NULL
  #for (i in 1:(n-1)) {
  i <- 1
    for (j in (i+1):(n-1))
      tri <- rbind(tri, data.frame(p1=i, p2=j, p3=j+1))
  #}
  plot.triangles(tri, x, y, 0.25)
  
  i <- 0
  
  #tri <- flip.edge(tri, c(6,8), data.frame(p1=c(4,4), p2=c(5,1), p3=c(9,9)))
  #plot.triangles(tri, res$x, res$y)
  #print(tri)
  #i <- i + 1
  
  i
}
prob3()

find.circle <- function(x1, y1, x2, y2, x3, y3) {
  D <- matrix(c(x1, x2, x3, y1, y2, y3, 1, 1, 1), ncol=3)
  D_a <- matrix(c(-x1^2-y1^2, -x2^2-y2^2, -x3^2-y3^2, y1, y2, y3, 1, 1, 1), ncol=3)
  D_b <- matrix(c(x1, x2, x3, -x1^2-y1^2, -x2^2-y2^2, -x3^2-y3^2, 1, 1, 1), ncol=3)
  D_c <- matrix(c(x1, x2, x3, y1, y2, y3, -x1^2-y1^2, -x2^2-y2^2, -x3^2-y3^2), ncol=3)
  a <- det(D_a) / det(D)
  b <- det(D_b) / det(D)
  c <- det(D_c) / det(D)
  print(c(a,b,c))
  x0 <- -a/2
  y0 <- -b/2
  r <- sqrt(x0^2 + y0^2 - c)
  return(c(x0,y0,r))
}

x1 <- 1 
y1 <- 1 
x2 <- 2 
y2 <- 4 
x3 <- 5 
y3 <- 3

res <- find.circle(x1, y1, x2, y2, x3, y3)
x0 <- res[1]
y0 <- res[2]
r <- res[3]

plot(x0, y0, pch=19, xlim=c(x0-r,x0+r), ylim=c(y0-r,y0+r), col='brown')
for (theta in seq(0,2*pi,0.01)) {
  points(x0 + r*cos(theta), y0 + r*sin(theta), pch=19, cex=0.3)
}
points(x1, y1, pch=19, xlim=c(x0-r,x0+r), ylim=c(y0-r,y0+r), col='red')
points(x2, y2, pch=19, xlim=c(x0-r,x0+r), ylim=c(y0-r,y0+r), col='green')
points(x3, y3, pch=19, xlim=c(x0-r,x0+r), ylim=c(y0-r,y0+r), col='blue')
grid()

library(gsubfn)  # need 0.7-0 or later
test_func <- function (a, b) {
  list(s=a+b, d=a-b)
}

list[s,d] <- test_func(2, 1)