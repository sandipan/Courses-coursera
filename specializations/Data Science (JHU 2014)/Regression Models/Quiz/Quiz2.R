1,2.
x <- c(0.61, 0.93, 0.83, 0.35, 0.54, 0.16, 0.91, 0.62, 0.62)
y <- c(0.67, 0.84, 0.6, 0.18, 0.85, 0.47, 1.1, 0.65, 0.36)
summary(lm(y ~ x))

3.
data(mtcars)
m <- lm(mpg ~ wt, data = mtcars)
summary(m)
predict(m, newdata=data.frame(wt=mean(mtcars$wt)), interval="confidence")

5.
predict(m, newdata=data.frame(wt=3), interval="confidence", level=0.95)
3*confint(m, 'wt', level=0.95)[1]

6.
summary(m)
confint(m, 'wt', level=0.95)
2*confint(m, 'wt', level=0.95)[1]

7.
y = (m*100)*(x/100) + c
x1 = x / 100
y = m*x + c
  = (m * 100) * x1 + c

8.
y = beta0 + beta1*X + epsilon
X1 = X + c
y = beta0 + beta1*(X1-c) + epsilon
intercept = beta0 - beta1*c

9.
m1 <- lm(mpg ~ NULL, data = mtcars)
m2 <- lm(mpg ~ wt, data = mtcars)
p1 <- predict(m1)
p2 <- predict(m2)
sum((mtcars$mpg - p2)^2) / sum((mtcars$mpg - p1)^2)

10.
sum((mtcars$mpg - p2))
sum((mtcars$mpg - p1))
