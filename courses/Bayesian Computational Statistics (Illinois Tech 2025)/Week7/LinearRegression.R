# Load necessary libraries
library(readr)
library(dplyr)
library(MASS)  # For mvrnorm function
library(ggplot2)
library(Matrix)

# URLs for the datasets
radon_url <- "https://raw.githubusercontent.com/pymc-devs/pymc-examples/main/examples/data/srrs2.dat"
city_url <- "https://raw.githubusercontent.com/pymc-devs/pymc-examples/main/examples/data/cty.dat"

# Read the datasets
radon_df <- read_csv(radon_url)
city_df <- read_csv(city_url)

# Filter the radon data to include only the relevant counties
radon_mn <- radon_df %>%
  filter(state == "MN", county %in% c("BLUE EARTH", "CLAY", "GOODHUE"))

# Create county indicators based on the inspected values
radon_mn <- radon_mn %>%
  mutate(
    BlueEarth = ifelse(county == "BLUE EARTH", 1, 0),
    Clay = ifelse(county == "CLAY", 1, 0),
    Goodhue = ifelse(county == "GOODHUE", 1, 0)
  )

radon_mn <- radon_mn %>%
  mutate(log_radon = log(activity))

# Define the matrix X and vector y
y <- matrix(radon_mn$log_radon, ncol = 1)

# Define the matrix X with 4 columns
X <- cbind(radon_mn$BlueEarth, radon_mn$Clay, radon_mn$Goodhue, radon_mn$floor)

# Ensure X is a matrix
X <- as.matrix(X)

# Compute A = (X^T X)^{-1}
XtX <- t(X) %*% X
A <- solve(XtX)

# Compute beta_hat = A X^T y
beta_hat <- A %*% t(X) %*% y

# Compute S_squared = (y - X beta_hat)^T(y - X beta_hat) * (1 / (n - p))
n <- nrow(X)
p <- ncol(X)
y_hat <- X %*% beta_hat
residuals <- y - y_hat
S_squared <- t(residuals) %*% residuals * (1 / (n - p))

# Function to draw from scaled inverse chi-squared distribution
draw_scaled_inv_chi_sq <- function(df, scale) {
  return(df * scale / rchisq(1, df))
}

# Collect 1000 samples
set.seed(3)  # For reproducibility
num_samples <- 1000
beta_draw_samples <- matrix(NA, nrow = num_samples, ncol = p)

for (i in 1:num_samples) {
  s_draw <- draw_scaled_inv_chi_sq(n - p, S_squared)
  beta_draw <- mvrnorm(1, mu = beta_hat, Sigma = Diagonal(n=p,x=s_draw) %*% A)
  beta_draw_samples[i, ] <- beta_draw
}

# Convert beta_draw_samples to a data frame for plotting
beta_draw_df <- data.frame(beta_draw_samples)
colnames(beta_draw_df) <- c("Blue Earth", "Clay", "Goodhue", "First Floor")

# Compute means and standard errors
means <- apply(beta_draw_samples, 2, mean)
ses <- apply(beta_draw_samples, 2, sd) / sqrt(num_samples)

# Print means and SEs
print("Means:")
print(means)
print("Standard Errors:")
print(ses)

# Plot histograms for each dimension of beta_draw and add mean and SE in legend
par(mfrow = c(2, 2))
for (i in 1:p) {
  hist(beta_draw_samples[, i], main = paste("Beta Draw:", colnames(beta_draw_df)[i]), xlab = "Value", col = "lightblue")
  abline(v = means[i], col = "red", lwd = 2)
  legend("topright", legend = c(paste("Mean:", round(means[i], 2)), paste("SE:", round(ses[i], 2))), col = c("red", "blue"), lty = 1, lwd = 2)
}
par(mfrow = c(1, 1))  # Reset layout

# Generate posterior predictive distribution for the case of X1=1, X2=0, X3=0, X4=0
new_X <- matrix(c(1, 0, 0, 1), ncol = 1)

# Draw posterior predictive samples
posterior_predictive_samples <- beta_draw_samples %*% new_X

# Plot the posterior predictive distribution
hist(posterior_predictive_samples, main = "Posterior Predictive Distribution: Blue Earth, First Floor", xlab = "Predicted log Radon", col = "lightblue")
abline(v = mean(posterior_predictive_samples), col = "red", lwd = 2)
legend("topright", legend = c(paste("Mean:", round(mean(posterior_predictive_samples), 2)), paste("SE:", round(sd(posterior_predictive_samples) / sqrt(num_samples), 2))), col = c("red", "blue"), lty = 1, lwd = 2)