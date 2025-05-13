# Define the target and proposal distributions
target_density <- function(x) {
  sin(x * pi)
}

proposal_density <- function(x) {
  dunif(x, min = 0, max = 1)
}

# Define the function h(x) to estimate its expectation under the target distribution
h <- function(x) {
  return(x)
}

# Number of samples
N <- 30000

# Draw samples from the proposal distribution
set.seed(3)
samples <- runif(N, min = 0, max = 1)

# Compute the weights
weights <- target_density(samples) / proposal_density(samples)

# Normalize the weights
weights <- weights / sum(weights)

# Estimate the expectation of h(x) under the target distribution using importance sampling
expectation_estimate <- sum(h(samples) * weights)

# Print the estimated expectation
print(expectation_estimate)

# Plotting the target distribution and the weighted samples
library(ggplot2)

# Data for plotting
plot_data <- data.frame(samples = samples, weights = weights)

# Plot the weighted samples
ggplot(plot_data, aes(x = samples, y = ..density.., weight = weights)) +
  geom_histogram(breaks = seq(0, 1, by = 0.02), color = "black", fill = "blue", alpha = 0.5) +
  stat_function(fun = function(x) sin(x * pi) / integrate(function(x) sin(x * pi), 0, 1)$value, color = "red", size = 1) +
  labs(title = "Importance Sampling",
       x = expression(x),
       y = "Weighted Density") +
  theme_minimal()