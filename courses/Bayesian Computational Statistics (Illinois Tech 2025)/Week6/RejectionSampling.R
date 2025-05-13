# Define the target and proposal distributions
target_density <- function(x) {
  dbeta(x, shape1 = 2, shape2 = 5)
}

proposal_density <- function(x) {
  dunif(x, min = 0, max = 1)
}

# Scaling constant M
M <- 2.5  # A constant such that target_density(x) <= M * proposal_density(x) for all x

# Rejection sampling function
rejection_sampling <- function(target_density, proposal_density, M, n_samples) {
  samples <- numeric(0)  # Initialize an empty vector for accepted samples
  while (length(samples) < n_samples) {
    x_star <- runif(1)  # Sample from the proposal distribution
    u <- runif(1)  # Sample from uniform distribution [0, 1]
    if (u <= target_density(x_star) / (M * proposal_density(x_star))) {
      samples <- c(samples, x_star)  # Accept the sample
    }
  }
  return(samples)
}

# Generate samples using rejection sampling
set.seed(1)
n_samples <- 2500
samples <- rejection_sampling(target_density, proposal_density, M, n_samples)

# Plot the results
hist(samples, probability = TRUE, breaks = 30, main = "Rejection Sampling",
     xlab = "x", ylim = c(0, 3))
curve(dbeta(x, shape1 = 2, shape2 = 5), col = "red", add = TRUE)
curve(dunif(x, min = 0, max = 1) * M, col = "blue", add = TRUE, lty = 2)
legend("topright", legend = c("Target Distribution", "Scaled Proposal Distribution"),
       col = c("red", "blue"), lty = c(1, 2))