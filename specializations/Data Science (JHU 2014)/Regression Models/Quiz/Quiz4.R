#1
library(MASS)
?shuttle
data(shuttle)
m <- glm(use ~ wind, data=shuttle, family="binomial")
summary(m)
# ln (p / (1 - p)) = -0.25131 -0.03181 * wintail
o1<-exp(predict(m, newdata=data.frame(wind=levels(shuttle$wind)[1])))
o2<-exp(predict(m, newdata=data.frame(wind=levels(shuttle$wind)[2])))
o2 / o1
#m <- glm(use ~ wind-1, data=shuttle, family=binomial)
#summary(m)
# ln (p / (1 - p)) = -0.2513 * winhead -0.2831 * wintail
# (odds(use)|windtail) / (odds(use)|windhead) = exp(-0.2831)/exp(-0.2513)

#predict(m, newdata=data.frame(wind=levels(shuttle$wind)[1]), type='response')
#predict(m, newdata=data.frame(wind=levels(shuttle$wind)[2]), type='response')

#2
m <- glm(use ~ wind+magn-1, data=shuttle, family="binomial")
summary(m)
# (odds(use)|windtail) / (odds(use)|windhead) = exp(-0.3955)/exp(-0.3635)


#3
p(auto==1) / (1-p(auto==1)) = exp(sum(wi*xi))
p(1-auto==1) / (1-p(1-auto==1)) = exp(sum(w1i*xi))
=>p(auto==0) / (1-p(auto==0)) = exp(sum(w1i*xi))
=>(1-p(auto==1)) / p(auto==1) = exp(sum(w1i*xi))
=> exp(sum(wi*xi)) = exp(-sum(w1i*xi))
=> w1i = -wi

#4
data(InsectSprays)
m <- glm(count ~ spray-1, data=InsectSprays, family="poisson")
summary(m)
exp(coef(m)['sprayA']) / exp(coef(m)['sprayB'])
#log(count|sprayA)

#5
#glm(count ~ x + offset(t), family = poisson) 
# log(count) = w0 + w1*x + w2*off(t) 
#glm(count ~ x + offset(t2), family = poisson)
#t2 <- log(10) + t
# log(count) = w01 + w11*x + w21*off(log(10)+t) 

positive_part <- function(x) {
 return((x >= 0) * x)
}

#6
x <- -5:5
y <- c(5.12, 3.93, 2.67, 1.87, 0.52, 0.08, 0.93, 2.05, 2.54, 3.87, 4.97)
#y = w0 + w1 * (0 - x)+ + w2 * (x - 0)+
x1 <- positive_part(-x)
x2 <- positive_part(x)
x1
x2
summary(lm(y ~ x1 + x2))$coef

#n <- 500; x <- seq(0, 4 * pi, length = n); y <- sin(x) + rnorm(n, sd = .3)
#knots <- seq(0, 8 * pi, length = 20);
#splineTerms <- sapply(knots, function(knot) (x > knot) * (x - knot))
#xMat <- cbind(1, x, splineTerms)
#yhat <- predict(lm(y ~ xMat - 1))
#plot(x, y, frame = FALSE, pch = 21, bg = "lightblue", cex = 2)
#lines(x, yhat, col = "red", lwd = 2)
#splineTerms <- sapply(knots, function(knot) (x > knot) * (x - knot)^2)
#xMat <- cbind(1, x, x^2, splineTerms)
#yhat <- predict(lm(y ~ xMat - 1))
#plot(x, y, frame = FALSE, pch = 21, bg = "lightblue", cex = 2)
#lines(x, yhat, col = "red", lwd = 2)
