setwd("E:/Academics/Coursera/R Programming")

set.seed(1)
rpois(5, 2)

set.seed(10)
x <- rbinom(10, 10, 0.5)
e <- rnorm(10, 0, 20)
y <- 0.5 + 2 * x + e

library(datasets)
n <- 1000
y <- rnorm(n)
x1 <- rnorm(n)
x2 <- rnorm(n)
Rprof(filename="Rprof.out")
fit <- lm(y ~ x1 + x2)
Rprof(NULL)
summaryRprof(filename="Rprof.out")

