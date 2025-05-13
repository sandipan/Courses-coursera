# Install necessary packages if not already installed
if (!requireNamespace("rstan", quietly = TRUE)) install.packages("rstan")
if (!requireNamespace("ggplot2", quietly = TRUE)) install.packages("ggplot2")
if (!requireNamespace("tidyr", quietly = TRUE)) install.packages("tidyr")
if (!requireNamespace("bayesplot", quietly = TRUE)) install.packages("bayesplot")

# Load necessary libraries
library(rstan)
library(ggplot2)
library(tidyr)
library(bayesplot)

# Data
schools_data <- list(
  J = 8,  # number of schools
  y = c(28, 8, 3, 7, 1, 1, 18, 12),  # treatment effects
  sigma = c(15, 10, 16, 11, 9, 11, 10, 18)  # standard errors
)

# Stan model for normal-normal model
stan_code <- "
data {
  int<lower=0> J;  // number of schools
  real y[J];  // estimated treatment effects
  real<lower=0> sigma[J];  // standard errors of effect estimates
}
parameters {
  real mu;  // overall mean
  real<lower=0> tau;  // between-school standard deviation
  vector[J] theta;  // school effects
}
model {
  mu ~ normal(0, 5);
  tau ~ cauchy(0, 5);
  theta ~ normal(mu, tau);
  y ~ normal(theta, sigma);
}
"

# Compile the model
stan_model <- stan_model(model_code = stan_code)

# Fit the model with more iterations and higher adapt_delta
fit <- sampling(stan_model, data = schools_data, iter = 4000, chains = 4, seed = 123, control = list(adapt_delta = 0.99, max_treedepth = 15))

# Print the results
print(fit)

# Plot the results
mcmc_trace(as.array(fit))

# --- Future data from current experiments ---

# Extract the theta samples using as.matrix
theta_samples <- as.matrix(fit, pars = "theta")

# Generate predicted values for each school
set.seed(123)
predictions <- apply(theta_samples, 2, function(theta) {
  rnorm(length(theta), mean = theta, sd = schools_data$sigma)
})

# Convert predictions to data frame for ggplot
predictions_df <- as.data.frame(predictions)
colnames(predictions_df) <- paste0("School_", letters[1:8])

# Reshape data frame for ggplot
predictions_long <- gather(predictions_df, key = "School", value = "Prediction")

# Plot histograms for each school
ggplot(predictions_long, aes(x = Prediction)) +
  geom_histogram(bins = 30, fill = "blue", color = "black", alpha = 0.7) +
  facet_wrap(~ School, scales = "free") +
  theme_minimal() +
  labs(title = "Posterior Predictive Distribution for Each School",
       x = "Predicted Treatment Effect",
       y = "Frequency")

# --- Future data from a future experiment ---

# Extract the mu and tau samples using as.matrix
mu_samples <- as.matrix(fit, pars = "mu")
tau_samples <- as.matrix(fit, pars = "tau")

# Define sample size for future experiment
n_tilde <- 30

# Generate future predictions
set.seed(123)
future_predictions <- replicate(length(mu_samples), {
  mu <- sample(mu_samples, 1)
  tau <- sample(tau_samples, 1)
  theta_tilde <- rnorm(1, mean = mu, sd = tau)
  sigma_tilde <- sqrt(mean(schools_data$sigma^2) / n_tilde)
  y_tilde <- rnorm(1, mean = theta_tilde, sd = sigma_tilde)
  return(y_tilde)
})

# Convert future predictions to data frame for ggplot
future_predictions_df <- data.frame(Future_Prediction = future_predictions)

# Plot histogram of future predictions
ggplot(future_predictions_df, aes(x = Future_Prediction)) +
  geom_histogram(bins = 30, fill = "blue", color = "black", alpha = 0.7) +
  theme_minimal() +
  labs(title = "Posterior Predictive Distribution for Future Data",
       x = "Predicted Future Treatment Effect",
       y = "Frequency")

# --- Pair Plots ---

# Generate pairs plot for diagnostic purposes
pairs(fit, pars = c("mu", "tau", "theta[1]", "theta[2]", "theta[3]", 
                    "theta[4]", "theta[5]", "theta[6]", "theta[7]", 
                    "theta[8]"))

pairs(fit, pars = c("mu", "tau", "theta[1]", "theta[2]"))