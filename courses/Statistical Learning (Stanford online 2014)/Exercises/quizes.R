setwd("E:/Work/Academics/StanfordOnline/Exercises")

## Ch9
library(MASS)
getData <- function(m, n) {
	mu1 <- rep(0, n)
	mu2 <- rep(c(1,0), c(n/2,n/2))
	Sigma <- diag(n)
	x1 <- mvrnorm(m, mu1, Sigma)
	x2 <- mvrnorm(m, mu2, Sigma)
	x <- rbind(x1, x2)
	y <- rep(c(0,1),c(m,m))
	#x <- mvrnorm(m, mu, Sigma, empirical=TRUE)
	#mean(x)
	#var(x)
	dat <- data.frame(y=factor(y),x)
	return(dat)
}
ntrain <- 50
ntest <- 500
n <- 10
error <- c()
ntrial <- 1000
for (i in 1:ntrial) {
	#data
	train <- getData(ntrain, n)
	test <- getData(ntest, n)
	#svm
	#fit <- svm(factor(y)~., data=train)
	#fit <- svm(factor(y)~., data=train, kernel='linear')
	#p <- predict(fit, test)
	#glm
	fit <- glm(factor(y)~., data=train, family='binomial')
	p <- predict(fit, test, type='response')
	p[p > 0.5] <- 1
	p[p <= 0.5] <- 0
	#error
	error <- c(error, sum(p != test$y) / nrow(test))
}
print(error)
mean(error)
hist(error)

d <- load("10.R.RData")
x1 <- rbind(x, x.test)
dim(x1)
#head(x1)
pca.out <- prcomp(x1, scale=TRUE)
pca.out$sdev
biplot(pca.out, scale=0)
sum((pca.out$sdev[1:5])^2) / sum((pca.out$sdev)^2) 

summary(pc.cr <- princomp(x1, cor=TRUE))
loadings(pc.cr)
plot(pc.cr, type='l')
sum((pc.cr$sdev[1:5])^2) / sum((pc.cr$sdev)^2) 

C <- pca.out$rotation[,1:5]
X <- as.data.frame(as.matrix(x) %*% C)
X$y <- y
m <- lm(y ~ ., data = X)
Xtest <- as.data.frame(as.matrix(x.test) %*% C)
p <- predict(m, newdata = Xtest)
MSE <- mean((p - y.test)^2)
