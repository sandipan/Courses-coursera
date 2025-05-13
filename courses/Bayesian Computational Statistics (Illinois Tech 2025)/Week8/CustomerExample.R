# Load necessary libraries
library(MCMCpack)  # For rdirichlet function and rinvchisq function

# Simulate data
set.seed(123)
n <- 300
lambda_true <- 0.4
mu_online_true <- 45
mu_physical_true <- 100
sigma_online_true <- 20
sigma_physical_true <- 15

z_true <- rbinom(n, 1, lambda_true)
y <- rnorm(n, mean = mu_online_true, sd = sigma_online_true) * (z_true == 1) + rnorm(n, mean = mu_physical_true, sd = sigma_physical_true) * (z_true == 0)

# Initialize parameters
lambda <- 0.5
mu_online <- mean(y)
mu_physical <- mean(y)
sigma_online_sq <- var(y)
sigma_physical_sq <- var(y)

# Set priors
alpha_1 <- 2
alpha_2 <- 2
mu0_online <- 50
mu0_physical <- 50
sigma0_online_sq <- 25^2
sigma0_physical_sq <- 25^2
nu0_online <- 2  # Prior degrees of freedom for sigma_online_sq
nu0_physical <- 2  # Prior degrees of freedom for sigma_physical_sq

# Gibbs sampling parameters
iterations <- 1000
burn_in <- 500

# Storage for samples
lambda_samples <- numeric(iterations)
mu_online_samples <- numeric(iterations)
mu_physical_samples <- numeric(iterations)
sigma_online_sq_samples <- numeric(iterations)
sigma_physical_sq_samples <- numeric(iterations)

# Gibbs sampling loop
for (iter in 1:iterations) {
  # Update z
  z_probs <- lambda * dnorm(y, mean = mu_online, sd = sqrt(sigma_online_sq)) /
    (lambda * dnorm(y, mean = mu_online, sd = sqrt(sigma_online_sq)) + (1 - lambda) * dnorm(y, mean = mu_physical, sd = sqrt(sigma_physical_sq)))
  z <- rbinom(n, 1, z_probs)
  
  # Update lambda
  alpha_lambda_post <- alpha_1 + sum(z)
  beta_lambda_post <- alpha_2 + n - sum(z)
  lambda <- rbeta(1, alpha_lambda_post, beta_lambda_post)
  
  # Update mu_online
  n_online <- sum(z)
  y_online_mean <- mean(y[z == 1])
  mu_online_post_mean <- (mu0_online / sigma0_online_sq + n_online * y_online_mean / sigma_online_sq) / (1 / sigma0_online_sq + n_online / sigma_online_sq)
  mu_online_post_sd <- sqrt(1 / (1 / sigma0_online_sq + n_online / sigma_online_sq))
  mu_online <- rnorm(1, mean = mu_online_post_mean, sd = mu_online_post_sd)
  
  # Update mu_physical
  n_physical <- n - n_online
  y_physical_mean <- mean(y[z == 0])
  mu_physical_post_mean <- (mu0_physical / sigma0_physical_sq + n_physical * y_physical_mean / sigma_physical_sq) / (1 / sigma0_physical_sq + n_physical / sigma_physical_sq)
  mu_physical_post_sd <- sqrt(1 / (1 / sigma0_physical_sq + n_physical / sigma_physical_sq))
  mu_physical <- rnorm(1, mean = mu_physical_post_mean, sd = mu_physical_post_sd)
  
  # Update sigma_online_sq using scaled inverse chi-squared distribution
  nu_online_post <- nu0_online + n_online
  sigma_online_sq_post <- (nu0_online * sigma0_online_sq + sum((y[z == 1] - mu_online)^2)) / nu_online_post
  sigma_online_sq <- rinvchisq(1, nu_online_post, sigma_online_sq_post)
  
  # Update sigma_physical_sq using scaled inverse chi-squared distribution
  nu_physical_post <- nu0_physical + n_physical
  sigma_physical_sq_post <- (nu0_physical * sigma0_physical_sq + sum((y[z == 0] - mu_physical)^2)) / nu_physical_post
  sigma_physical_sq <- rinvchisq(1, nu_physical_post, sigma_physical_sq_post)
  
  # Store samples
  lambda_samples[iter] <- lambda
  mu_online_samples[iter] <- mu_online
  mu_physical_samples[iter] <- mu_physical
  sigma_online_sq_samples[iter] <- sigma_online_sq
  sigma_physical_sq_samples[iter] <- sigma_physical_sq
}

# Remove burn-in samples
lambda_samples <- lambda_samples[(burn_in + 1):iterations]
mu_online_samples <- mu_online_samples[(burn_in + 1):iterations]
mu_physical_samples <- mu_physical_samples[(burn_in + 1):iterations]
sigma_online_sq_samples <- sigma_online_sq_samples[(burn_in + 1):iterations]
sigma_physical_sq_samples <- sigma_physical_sq_samples[(burn_in + 1):iterations]

# Calculate means for each parameter
mean_lambda <- mean(lambda_samples)
mean_mu_online <- mean(mu_online_samples)
mean_mu_physical <- mean(mu_physical_samples)
mean_sigma_online_sq <- mean(sigma_online_sq_samples)
mean_sigma_physical_sq <- mean(sigma_physical_sq_samples)

# Plot histograms of the posterior samples with means
par(mfrow = c(2, 3))

hist(lambda_samples, main = "Posterior of lambda", xlab = "lambda", col = "lightblue")
abline(v = mean_lambda, col = "red", lwd = 2)
text(mean_lambda, par("usr")[4], labels = paste0("Mean: ", round(mean_lambda, 2)), pos = 3, col = "red")

hist(mu_online_samples, main = "Posterior of mu_online", xlab = "mu_online", col = "lightblue")
abline(v = mean_mu_online, col = "red", lwd = 2)
text(mean_mu_online, par("usr")[4], labels = paste0("Mean: ", round(mean_mu_online, 2)), pos = 3, col = "red")

hist(mu_physical_samples, main = "Posterior of mu_physical", xlab = "mu_physical", col = "lightblue")
abline(v = mean_mu_physical, col = "red", lwd = 2)
text(mean_mu_physical, par("usr")[4], labels = paste0("Mean: ", round(mean_mu_physical, 2)), pos = 3, col = "red")

hist(sigma_online_sq_samples, main = "Posterior of sigma_online^2", xlab = "sigma_online^2", col = "lightblue")
abline(v = mean_sigma_online_sq, col = "red", lwd = 2)
text(mean_sigma_online_sq, par("usr")[4], labels = paste0("Mean: ", round(mean_sigma_online_sq, 2)), pos = 3, col = "red")

hist(sigma_physical_sq_samples, main = "Posterior of sigma_physical^2", xlab = "sigma_physical^2", col = "lightblue")
abline(v = mean_sigma_physical_sq, col = "red", lwd = 2)
text(mean_sigma_physical_sq, par("usr")[4], labels = paste0("Mean: ", round(mean_sigma_physical_sq, 2)), pos = 3, col = "red")

# Print summary statistics
summary_stats <- list(
  lambda = summary(lambda_samples),
  mu_online = summary(mu_online_samples),
  mu_physical = summary(mu_physical_samples),
  sigma_online_sq = summary(sigma_online_sq_samples),
  sigma_physical_sq = summary(sigma_physical_sq_samples)
)
print(summary_stats)

# Simulate posterior predictive data
y_rep <- numeric(n)
for (i in 1:n) {
  if (z_true[i] == 1) {
    y_rep[i] <- rnorm(1, mean = mu_online, sd = sqrt(sigma_online_sq))
  } else {
    y_rep[i] <- rnorm(1, mean = mu_physical, sd = sqrt(sigma_physical_sq))
  }
}

# QQ plot
qqnorm(y)
qqline(y, col = "red")

# Scatter plot of observed vs. predicted
plot(y, y_rep, main = "Observed vs. Predicted", xlab = "Observed", ylab = "Predicted")
abline(0, 1, col = "red")