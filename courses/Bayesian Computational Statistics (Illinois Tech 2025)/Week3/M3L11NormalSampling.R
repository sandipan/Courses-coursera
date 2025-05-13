# Load necessary library
library(MASS)

# Set seed for reproducibility
set.seed(123)

# Generate some data
n <- 100  # Number of data points
mu_true <- 5  # True mean
sigma2_true <- 4  # True variance
y <- rnorm(n, mean = mu_true, sd = sqrt(sigma2_true))

# Define the normal model with noninformative priors
# Priors: p(mu, sigma2) ∝ 1/sigma2

# Compute posterior distribution parameters
y_bar <- mean(y)  # Sample mean
S2 <- var(y)  # Sample variance

# Posterior parameters
mu_post <- y_bar
sigma2_post <- S2 * (n - 1) / rchisq(1, df = n - 1)

# Number of samples to draw from the posterior predictive distribution
n_samples <- 1000

# Draw from the joint posterior distribution of (mu, sigma2)
mu_samples <- numeric(n_samples)
sigma2_samples <- numeric(n_samples)
for (i in 1:n_samples) {
  sigma2_samples[i] <- S2 * (n - 1) / rchisq(1, df = n - 1)
  mu_samples[i] <- rnorm(1, mean = y_bar, sd = sqrt(sigma2_samples[i] / n))
}

# Draw from the posterior predictive distribution
y_tilde <- numeric(n_samples)
for (i in 1:n_samples) {
  y_tilde[i] <- rnorm(1, mean = mu_samples[i], sd = sqrt(sigma2_samples[i]))
}

# Plot the posterior predictive distribution
hist(y_tilde, breaks = 30, main = "Posterior Predictive Distribution", xlab = "y_tilde", col = "skyblue", border = "white")
abline(v = mu_true, col = "red", lwd = 2, lty = 2)
legend("topright", legend = "True Mean", col = "red", lwd = 2, lty = 2)
