# Number of approximations 
num_approx <- 10

# Data
n <- 100
y <- 48

# Define the parameter space and the equally spaced points
theta <- seq(0, 1, length.out = num_approx)

# Define the posterior distribution function
p_theta_given_y <- function(theta, y, n) {
  return(theta^y * (1 - theta)^(n - y))
}

# Compute the unnormalized posterior at each theta value
p_values <- p_theta_given_y(theta, y, n)

# Normalize the posterior values
normalized_p_values <- p_values / sum(p_values)

# Compute the cumulative distribution function (CDF)
cdf <- cumsum(normalized_p_values)

# Function to draw a sample using the inverse CDF method
draw_sample <- function(cdf, theta) {
  U <- runif(1)  # Draw a uniform random sample
  sample_index <- which.min(abs(cdf - U))  # Find the closest CDF value to U
  return(theta[sample_index])  # Return the corresponding theta value
}

# Draw a sample from the discrete approximation
sample <- draw_sample(cdf, theta)
print(sample)

# Plotting the approximation and the sample
library(ggplot2)

plot_data <- data.frame(theta = theta, posterior = normalized_p_values)
# Generate the step plot data
step_x <- sort(c(theta - 1/(2*num_approx), theta + 1/(2*num_approx)))
step_y <- rep(normalized_p_values, each = 2)

step_plot_data <- data.frame(x = step_x, y = step_y)

ggplot() +
  geom_step(data = step_plot_data, aes(x = x, y = y), direction = "hv", color = 'blue') +
  geom_point(data = plot_data, aes(x = theta, y = posterior), color = 'blue') +
  geom_vline(xintercept = theta, linetype = "dashed", color = "red") +
  geom_point(aes(x = sample, y = 0), color = "green", size = 3) +
  geom_text(data = plot_data, aes(x = theta, y = posterior + 0.005, label = round(posterior, 4)), color = "black") +
  labs(title = "Posterior Distribution Approximation",
       x = expression(theta),
       y = expression(p(theta ~ "|" ~ y))) +
  theme_minimal()