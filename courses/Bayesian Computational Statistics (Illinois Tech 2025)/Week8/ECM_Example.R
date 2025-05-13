library(ggplot2)
set.seed(123)

# --- Create a Dataset to estimate with ECM ---

# Parameters for the true distributions
mu1 <- 0
sigma1 <- 1
n1 <- 150

mu2 <- 4
sigma2 <- 1
n2 <- 150

# Generate the synthetic data
data <- c(rnorm(n1, mean = mu1, sd = sigma1), rnorm(n2, mean = mu2, sd = sigma2))
data <- sample(data)

# Plot the synthetic data
hist(data, breaks = 30, col = 'green', main = 'Histogram of the generated data', xlab = 'Data')

# --- ECM Algorithm for the Synthetic Data ---

# Initialization
mu1_est <- min(data)
mu2_est <- max(data)
sigma1_est <- sd(data)
sigma2_est <- sd(data)
lambda1_est <- 0.5

e_step <- function(data, mu1, mu2, sigma1, sigma2, lambda1) {
  # Compute the responsibilities (posterior probabilities)
  pdf1 <- dnorm(data, mean = mu1, sd = sigma1)
  pdf2 <- dnorm(data, mean = mu2, sd = sigma2)
  gamma1 <- lambda1 * pdf1 / (lambda1 * pdf1 + (1 - lambda1) * pdf2)
  return(gamma1)
}

cm_step <- function(data, gamma1) {
  # Update mixture proportion
  lambda1_new <- mean(gamma1)
  
  # Update means
  mu1_new <- sum(gamma1 * data) / sum(gamma1)
  mu2_new <- sum((1 - gamma1) * data) / sum(1 - gamma1)
  
  # Update variances
  sigma1_new <- sqrt(sum(gamma1 * (data - mu1_new)^2) / sum(gamma1))
  sigma2_new <- sqrt(sum((1 - gamma1) * (data - mu2_new)^2) / sum(1 - gamma1))
  
  return(list(lambda1_new = lambda1_new, mu1_new = mu1_new, mu2_new = mu2_new, sigma1_new = sigma1_new, sigma2_new = sigma2_new))
}

# ECM algorithm
tolerance <- 1e-6
max_iterations <- 100

for (iteration in 1:max_iterations) {
  # E-step
  gamma1 <- e_step(data, mu1_est, mu2_est, sigma1_est, sigma2_est, lambda1_est)
  
  # CM-step
  estimates <- cm_step(data, gamma1)
  
  # Check for convergence
  if (abs(mu1_est - estimates$mu1_new) < tolerance && abs(mu2_est - estimates$mu2_new) < tolerance) {
    break
  }
  
  # Update estimates
  lambda1_est <- estimates$lambda1_new
  mu1_est <- estimates$mu1_new
  mu2_est <- estimates$mu2_new
  sigma1_est <- estimates$sigma1_new
  sigma2_est <- estimates$sigma2_new
}

cat("Estimated parameters after", iteration, "iterations:\n")
cat("Mean 1:", round(mu1_est, 2), ", Variance 1:", round(sigma1_est^2, 2), "\n")
cat("Mean 2:", round(mu2_est, 2), ", Variance 2:", round(sigma2_est^2, 2), "\n")
cat("Mixture Proportion 1:", round(lambda1_est, 2), "\n")

# Create a data frame for plotting the results
results <- data.frame(
  Parameter = c("Mean 1", "Variance 1", "Mean 2", "Variance 2", "Mixture Proportion 1"),
  Type = rep(c("Actual", "Estimated"), each = 5),
  Value = c(mu1, sigma1^2, mu2, sigma2^2, 0.5, mu1_est, sigma1_est^2, mu2_est, sigma2_est^2, lambda1_est)
)

# Plot the results
ggplot(results, aes(x = Parameter, y = Value, color = Type, shape = Type)) +
  geom_point(size = 4) +
  labs(title = "Actual vs Estimated Parameters", y = "Value") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))