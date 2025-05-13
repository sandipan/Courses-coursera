# Load necessary library
library(MASS)

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

# Calculate the posterior median and 95% credible interval for mu
mu_median <- median(mu_samples)
mu_credible_interval <- quantile(mu_samples, probs = c(0.025, 0.975))

# Plot the histogram of the posterior samples of mu
hist(mu_samples, breaks = 30, main = "Posterior Distribution of Mu", xlab = expression(mu), col = "skyblue", border = "white")
abline(v = mu_median, col = "blue", lwd = 2, lty = 2)
abline(v = mu_credible_interval, col = "red", lwd = 2, lty = 2)
legend("topright", legend = c("Posterior Median", "95% Credible Interval"), col = c("blue", "red"), lwd = 2, lty = 2)

# Print the posterior median and 95% credible interval for mu
cat("Posterior median of mu:", mu_median, "\n")
cat("95% credible interval for mu:", mu_credible_interval, "\n")
