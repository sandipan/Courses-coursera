# Load necessary libraries
library(MCMCpack)  # for rdirichlet
library(ggplot2)

# Set seed for reproducibility
set.seed(123)

# Data from the survey
n <- 1000
y1 <- 450  # Vanilla
y2 <- 300  # Chocolate
y3 <- 250  # Strawberry

# Prior Dirichlet parameters (noninformative prior)
alpha_prior <- c(1, 1, 1)

# Posterior Dirichlet parameters
alpha_posterior <- c(y1 + alpha_prior[1], y2 + alpha_prior[2], y3 + alpha_prior[3])

# Number of posterior samples
n_samples <- 1000

# Draw samples from the Dirichlet distribution
posterior_samples <- rdirichlet(n_samples, alpha_posterior)

# Compute theta[Vanilla] - theta[Chocolate] for each sample
theta_diff <- posterior_samples[,1] - posterior_samples[,2]

# Plot the histogram of theta[Vanilla] - theta[Chocolate]
ggplot(data.frame(theta_diff), aes(x = theta_diff)) +
  geom_histogram(binwidth = 0.01, fill = "skyblue", color = "white", boundary = 0) +
  labs(title = expression(paste("Posterior Distribution of ", theta[Vanilla] - theta[Chocolate])),
       x = expression(theta[Vanilla] - theta[Chocolate]),
       y = "Frequency") +
  theme_minimal()

# Calculate and print the proportion of samples where theta[Vanilla] > theta[Chocolate]
prop_theta_vanilla_greater_chocolate <- mean(theta_diff > 0)
cat("Estimated probability that Vanilla has more support than Chocolate:", prop_theta_vanilla_greater_chocolate, "\n")
