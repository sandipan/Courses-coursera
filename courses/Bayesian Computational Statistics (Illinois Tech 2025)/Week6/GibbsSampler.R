# Load necessary library
library(MASS)  # for mvrnorm function

# Parameters
num_samples <- 1000  # Number of samples
burn_in <- 100       # Number of burn-in samples to discard
rho <- 0.8           # Correlation coefficient
sigma <- 1           # Standard deviation (both variables have the same standard deviation)

# Initialize storage for samples
samples <- matrix(NA, nrow = num_samples, ncol = 2)
colnames(samples) <- c("theta_1", "theta_2")

# Initialize starting values
samples[1, ] <- c(0, 0)

# Gibbs sampling
set.seed(123)  # For reproducibility

for (i in 2:num_samples) {
  theta_2 <- samples[i-1, 2]
  samples[i, 1] <- rnorm(1, mean = rho * theta_2, sd = sqrt(1 - rho^2))
  
  theta_1 <- samples[i, 1]
  samples[i, 2] <- rnorm(1, mean = rho * theta_1, sd = sqrt(1 - rho^2))
}

# Discard burn-in samples
samples <- samples[(burn_in + 1):num_samples, ]

# Plot the samples
plot(samples, col = rgb(0, 0, 1, 0.5), pch = 16, cex = 0.5,
     main = "Gibbs Sampling from Bivariate Normal Distribution",
     xlab = expression(theta[1]), ylab = expression(theta[2]))

# Plot histograms of the marginal distributions
par(mfrow = c(1, 2))
hist(samples[, 1], breaks = 30, main = expression(paste("Histogram of ", theta[1])), xlab = expression(theta[1]), col = "skyblue")
hist(samples[, 2], breaks = 30, main = expression(paste("Histogram of ", theta[2])), xlab = expression(theta[2]), col = "skyblue")

# Plot the density of the samples
par(mfrow = c(1, 1))
plot(density(samples[, 1]), main = "Density Plot of Samples", xlab = "Value", col = "blue", lwd = 2)
lines(density(samples[, 2]), col = "red", lwd = 2)
legend("topright", legend = c(expression(theta[1]), expression(theta[2])), col = c("blue", "red"), lwd = 2)