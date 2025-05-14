mean(replicate(1000, {
  sum(sample(1:6, 2)) >= 9 
}))
5/18

mean(replicate(1000, {
  (sample(1:6, 1))^2
}))
sum((1:6)^2*1/6)
91/6

g <- 0:3          # values of the r.v. G
r <- 0:2          # values of the r.v. R
gr <- outer(g, r) # all possible pairs of values G x R
  
f_GR <- matrix(
  c(4/84, 12/84, 4/84,
    18/84, 24/84, 3/84,
    12/84, 6/84, 0,
    1/84, 0, 0),
  ncol = 3, byrow = T)  # Joint PMF f_GR(.)

f_G <- rowSums(f_GR)    # marginal PMF f_G(.)
f_R <- colSums(f_GR)    # marginal PMF f_R(.)

E_G <- sum(f_G*g)       # E[G] = sum(f_G(g)*g)
E_R <- sum(f_R*r)       # E[R] = sum(f_R(r)*r)

E_GR <- sum(gr*f_GR)    # E[GR] = sum(f_GR(g*r)*g*r)

covar <- sum(f_GR*outer(g-E_G,r-E_R))  # E[GR] = sum(f_GR(g,r)*(g-E_G)*(r-E_r))
covar

covar <- E_GR - E_G*E_R # cov(G, R) = E[GR] - E[G]E[R]
covar

x <- 1:6
sum((x - mean(x))^2)/length(x)

(1:4)/16

mean(c(-1,0,2))
var(c(-1,0,2))

xbar <- 50
s <- 10
n <- 20
c(xbar + qt(.025, n-1)*s/sqrt(n), xbar + qt(.975, n-1)*s/sqrt(n))
c(xbar + qnorm(.025)*s/sqrt(n), xbar + qnorm(.975)*s/sqrt(n))

mean(rt(1000, 10))
sd(rt(1000, 10))

(0.95 - 1.05) / (0.12 / sqrt(40))