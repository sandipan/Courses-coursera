# Load necessary libraries
library(rstan)
library(ggplot2)

# Set seed for reproducibility
set.seed(42)

# Generate data from a true normal distribution
n <- 100  # Number of data points
true_mean <- 5
true_sd <- 2
y <- rnorm(n, mean = true_mean, sd = true_sd)

# Plot the true distribution
true_data <- data.frame(x = seq(min(y) - 1, max(y) + 1, length.out = 100))
true_data$y <- dnorm(true_data$x, mean = true_mean, sd = true_sd)

ggplot(true_data, aes(x = x, y = y)) +
  geom_line(color = "blue") +
  ggtitle("True Distribution") +
  xlab("Value") +
  ylab("Density")

# Define the Stan model
stan_model_code <- "
data {
  int<lower=0> N;       // Number of data points
  real y[N];            // Observations
}
parameters {
  real mu;              // Mean parameter
  real<lower=0> sigma;  // Standard deviation parameter
}
model {
  y ~ normal(mu, sigma);  // Likelihood
}
"

# Compile the Stan model
stan_model <- stan_model(model_code = stan_model_code)

# Fit the Stan model
fit <- sampling(stan_model, data = list(N = n, y = y), iter = 1000, chains = 4, seed = 123)
print(fit)

# Extract posterior samples
posterior_samples <- extract(fit)

# Calculate the mean of the posterior samples
mu_mean <- mean(posterior_samples$mu)
sigma_mean <- mean(posterior_samples$sigma)

# Plot the estimated distribution
estimated_data <- data.frame(x = seq(min(y) - 1, max(y) + 1, length.out = 100))
estimated_data$y <- dnorm(estimated_data$x, mean = mu_mean, sd = sigma_mean)

ggplot() +
  geom_line(data = true_data, aes(x = x, y = y), color = "blue") +
  geom_line(data = estimated_data, aes(x = x, y = y), color = "red") +
  ggtitle("True Distribution (blue) vs Estimated Distribution (red)") +
  xlab("Value") +
  ylab("Density")
