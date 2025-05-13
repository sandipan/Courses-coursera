# Load necessary library
library(ggplot2)
library(coda)  # for effectiveSize function

# Target distribution: Beta distribution with alpha = 2, beta = 5
alpha <- 2
beta <- 5
target_density <- function(x) {
  if (x < 0 || x > 1) return(0)
  return(dbeta(x, shape1 = alpha, shape2 = beta))
}

# Proposal distribution: Normal distribution centered at current point
proposal_distribution <- function(x) {
  return(rnorm(1, mean = x, sd = 0.1))  # Standard deviation of proposal distribution can be adjusted
}

# Metropolis algorithm
metropolis <- function(num_samples, initial_value) {
  samples <- numeric(num_samples)
  samples[1] <- initial_value
  
  for (t in 2:num_samples) {
    current_x <- samples[t-1]
    proposed_x <- proposal_distribution(current_x)
    
    # Ensure proposed_x is within the bounds of the Beta distribution
    if (proposed_x < 0 || proposed_x > 1) {
      samples[t] <- current_x  # Reject the proposal if out of bounds
    } else {
      acceptance_ratio <- target_density(proposed_x) / target_density(current_x)
      acceptance_ratio <- min(1, acceptance_ratio)
      
      if (runif(1) < acceptance_ratio) {
        samples[t] <- proposed_x
      } else {
        samples[t] <- current_x
      }
    }
  }
  
  return(samples)
}

# Parameters
num_samples <- 10000
initial_value <- 0.5

# Run the Metropolis algorithm
set.seed(123)
samples <- metropolis(num_samples, initial_value)

# Plot the samples
hist(samples, breaks = 30, probability = TRUE, col = "skyblue", border = "black",
     xlab = "Value", ylab = "Density", main = "Histogram and Density Plot of Samples from Metropolis Algorithm")

# Plot the density of the samples
lines(density(samples), col = "blue", lwd = 2)

# Overlay the true Beta distribution for comparison
curve(dbeta(x, shape1 = alpha, shape2 = beta), add = TRUE, col = "red", lwd = 2)

# Add legend
legend("topright", legend = c("Sample Density", "True Beta Density"), col = c("blue", "red"), lwd = 2)

# --- for sample size discussion ---
# Convert to MCMC object for analysis
mcmc_samples <- as.mcmc(samples)

# Compute the mean of the samples
sample_mean <- mean(samples)
cat("Sample Mean:", sample_mean, "\n")

# Compute the effective sample size (ESS)
ess <- effectiveSize(mcmc_samples)
cat("Effective Sample Size (ESS):", ess, "\n")

# Compute the standard error (SE) of the mean
sample_sd <- sd(samples)
se_mean <- sample_sd / sqrt(ess)
cat("Standard Error (SE) of the Mean:", se_mean, "\n")