# load necessary packages
library(rstan)

# Define the data
y_A <- 35
n_A <- 50
y_B <- 45
n_B <- 60

# Stan model for Bayesian comparison of two proportions
stan_model <- "
data {
  int<lower=0> y_A;       // number of successes in Group A
  int<lower=0> n_A;       // number of trials in Group A
  int<lower=0> y_B;       // number of successes in Group B
  int<lower=0> n_B;       // number of trials in Group B
}
parameters {
  real<lower=0, upper=1> p_A; // proportion in Group A
  real<lower=0, upper=1> p_B; // proportion in Group B
}
model {
  // Priors
  p_A ~ beta(1, 1);  // weakly informative prior for p_A
  p_B ~ beta(1, 1);  // weakly informative prior for p_B
  
  // Likelihood
  y_A ~ binomial(n_A, p_A);
  y_B ~ binomial(n_B, p_B);
}
"

# Data list for Stan
data_list <- list(y_A = y_A, n_A = n_A, y_B = y_B, n_B = n_B)

# Fit the model using Stan
fit <- stan(model_code = stan_model, data = data_list, iter = 2000, chains = 4)

# Print the summary of the fit
print(fit)

# Extract posterior samples
posterior_samples <- as.data.frame(extract(fit))

# Example of posterior summaries
summary(posterior_samples)

# Plot posterior distributions of p_A and p_B
par(mfrow=c(1,2))
hist(posterior_samples$p_A, main="Posterior Distribution of p_A", xlab="p_A")
hist(posterior_samples$p_B, main="Posterior Distribution of p_B", xlab="p_B")

# Previous code for Bayesian comparison of two proportions
# (Assuming fit and posterior_samples are already defined)

# Extract posterior samples
posterior_samples <- as.data.frame(extract(fit))

# Example of posterior summaries
summary(posterior_samples)

# Plot posterior distributions of p_A and p_B
par(mfrow=c(1,2))
hist(posterior_samples$p_A, main="Posterior Distribution of p_A", xlab="p_A")
hist(posterior_samples$p_B, main="Posterior Distribution of p_B", xlab="p_B")

# Bayesian Prediction: Likelihood of success in the next trial

# Number of simulations for prediction
S <- 1000

# Initialize vectors to store predictive probabilities
pred_prob_A <- numeric(S)
pred_prob_B <- numeric(S)

# Simulate new data and calculate predictive probabilities
for (s in 1:S) {
  # Sample from posterior distributions
  p_A_star <- posterior_samples$p_A[s]
  p_B_star <- posterior_samples$p_B[s]
  
  # Simulate new data points
  y_A_star <- rbinom(1, n_A, p_A_star)
  y_B_star <- rbinom(1, n_B, p_B_star)
  
  # Calculate predictive probabilities
  pred_prob_A[s] <- y_A_star / n_A
  pred_prob_B[s] <- y_B_star / n_B
}

# Summarize predictive probabilities
summary(pred_prob_A)
summary(pred_prob_B)

# Plot histograms of predictive probabilities
par(mfrow=c(1,2))
hist(pred_prob_A, main="Predictive Probabilities for Group A", xlab="Probability of Success")
hist(pred_prob_B, main="Predictive Probabilities for Group B", xlab="Probability of Success")
