1.
# sum(mu.sqrt(w)-x.sqrt(w))^2
# sum(mu.w1-y)^2, w1=sqrt(w), y=x.w1
# mu = solve(t(w1)%*%w1)%*%(t(w1)%*%y)
x <- c(0.18, -1.54, 0.42, 0.95)
w <- c(2, 1, 3, 1)
w1 <- sqrt(w)
y <- x*w1
solve(t(w1) %*% w1) %*% (t(w1) %*% y)

2.
# through mean
x <- c(0.8, 0.47, 0.51, 0.73, 0.36, 0.58, 0.57, 0.85, 0.44, 0.42)
y <- c(1.39, 0.72, 1.55, 0.48, 1.19, -1.59, 1.23, -0.65, 1.49, 0.05)
x1 <- cbind(rep(1, length(x)), x)
y1 <- as.matrix(y)
solve(t(x1) %*% x1) %*% (t(x1) %*% y1)
lm(y~x)
# through origin
# y = 0 + r * (s_y / s_x) * (x - 0)
# slope = cor(x, y) * sd(y) / sd(x)
lm(y~0+x)

3.
data(mtcars) 
lm(mpg ~ wt, data=mtcars)

4.
# s_x = 0.5*s_y 
# r = cor(x,y) = 0.5
# (y - ybar) / s_y = r * (x - xbar) / s_x
# y = ybar + r * (s_y / s_x) * (x - xbar)
r <- 0.5
s_y_by_s_x <- 1 / 0.5
slope <- r * s_y_by_s_x

5. 
#(s2 - 0) / 1 = r * (s1 - 0) / 1
s2 = 0.4 * 1.5

6.
x <- c(8.58, 10.46, 9.01, 9.64, 8.86)
scale(x)
mean(scale(x))
sd(scale(x))

7.
x <- c(0.8, 0.47, 0.51, 0.73, 0.36, 0.58, 0.57, 0.85, 0.44, 0.42)
y <- c(1.39, 0.72, 1.55, 0.48, 1.19, -1.59, 1.23, -0.65, 1.49, 0.05)
lm(y~x)

8.
# (y - 0) / s_y = r * (x - 0) / s_x
# y = r * (s_y / s_x) * x
# intercept = 0

9.
x <- c(0.8, 0.47, 0.51, 0.73, 0.36, 0.58, 0.57, 0.85, 0.44, 0.42)
# sum(mu*1-x)^2
ones <- rep(1, length(x))
mu <- solve(t(ones)%*%ones)%*%(t(ones)%*%x)
mu
mean(x)

10.
# beta1 = r * (s_y / s_x)
# gamma1 = r * (s_x / s_y)
# beta1 / gamma1 = v_y / v_x