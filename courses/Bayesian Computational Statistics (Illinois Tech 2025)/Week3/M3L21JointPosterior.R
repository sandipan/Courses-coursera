# Load necessary libraries
library(MASS)
library(ggplot2)

# Set seed for reproducibility
set.seed(123)

# Hypothetical data
n <- 70  # Number of measurements
y_bar <- 6.5  # Sample mean
s <- 2.4  # Sample standard deviation

# Number of samples to draw from the posterior distribution
n_samples <- 1000

# Draw samples from the joint posterior distribution of (mu, sigma2)
mu_samples <- numeric(n_samples)
sigma2_samples <- numeric(n_samples)
for (i in 1:n_samples) {
  sigma2_samples[i] <- (n - 1) * s^2 / rchisq(1, df = n - 1)
  mu_samples[i] <- rnorm(1, mean = y_bar, sd = sqrt(sigma2_samples[i] / n))
}

# Create a data frame for plotting
posterior_samples <- data.frame(mu = mu_samples, sigma2 = sigma2_samples)

# Plot the joint posterior distribution
ggplot(posterior_samples, aes(x = mu, y = sigma2)) +
  geom_point(alpha = 0.5, color = "blue") +
  labs(title = "Joint Posterior Distribution of Mu and Sigma^2",
       x = expression(mu),
       y = expression(sigma^2)) +
  theme_minimal()
