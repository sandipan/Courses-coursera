1/(1+0.05*0.999/(0.95*0.001))


post.pred.MC <- function(A, B, m, n_star){
  pred_sim <- matrix(NA, nrow=m)
  for (i in 1:m) {
    p_star <- rbeta(1, A, B)
    pred_sim[i] <- rbinom(1, n_star, p_star)
  }
  pred_sim
}

A <- 5 + 7 
B <- 5 + 3
m <- 50000
pred <- post.pred.MC(A, B, m, 1)
mean(pred)
hist(pred)

post.pred <- function(A, B, n_star, x_star){
  gamma(A+B) / (gamma(A)*gamma(B)) * choose(n_star, x_star) * gamma(A+x_star)*gamma(B+n_star-x_star)/gamma(A+B+n_star) 
}
print(post.pred(A, B, 1, 1))