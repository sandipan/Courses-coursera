# Load necessary libraries
library(coda)  # for effectiveSize function
library(ggplot2)

# Define target distribution: Beta distribution with alpha = 2, beta = 5
alpha <- 2
beta <- 5
target_density <- function(x) {
  if (x < 0 || x > 1) return(0)
  return(dbeta(x, shape1 = alpha, shape2 = beta))
}

# Define asymmetric proposal distribution: Chi-squared distribution centered at current point
proposal_distribution <- function(x) {
  return(rchisq(1, df = 2) + x - 1)  # Adjusting to center around the current point
}

# Metropolis-Hastings algorithm
metropolis_hastings <- function(num_samples, initial_value) {
  samples <- numeric(num_samples)
  samples[1] <- initial_value
  
  for (t in 2:num_samples) {
    current_x <- samples[t-1]
    proposed_x <- proposal_distribution(current_x)
    
    # Ensure proposed_x is within the bounds of the Beta distribution
    if (proposed_x < 0 || proposed_x > 1) {
      samples[t] <- current_x  # Reject the proposal if out of bounds
    } else {
      # Calculate the proposal density
      proposal_density_current_to_proposed <- dchisq(proposed_x - current_x + 1, df = 2)
      proposal_density_proposed_to_current <- dchisq(current_x - proposed_x + 1, df = 2)
      
      acceptance_ratio <- (target_density(proposed_x) * proposal_density_proposed_to_current) / 
        (target_density(current_x) * proposal_density_current_to_proposed)
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
burn_in <- 0
initial_value <- 0.5

# Run the Metropolis-Hastings algorithm
set.seed(123)
samples <- metropolis_hastings(num_samples, initial_value)
samples <- samples[(burn_in + 1):num_samples]

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

# Plot the density of the samples and the target distribution
hist(samples, breaks = 30, probability = TRUE, col = "skyblue", border = "black",
     xlab = "Value", ylab = "Density", main = "Histogram and Density Plot of Samples from Metropolis-Hastings Algorithm")
lines(density(samples), col = "blue", lwd = 2)
curve(dbeta(x, shape1 = alpha, shape2 = beta), add = TRUE, col = "red", lwd = 2)
legend("topright", legend = c("Sample Density", "True Beta Density"), col = c("blue", "red"), lwd = 2)