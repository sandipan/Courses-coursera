# Install and load necessary packages
library(rstan)
library(bayesplot)
library(ggplot2)

# Bioassay data
x <- c(-0.86, -0.3, -0.05, 0.73)  # Doses
n <- c(5, 5, 5, 5)               # Number of animals exposed
y <- c(0, 1, 3, 5)               # Number of animals that survived

# Stan model for Bayesian logistic regression
stan_model <- "
data {
  int<lower=0> N;        // number of data points
  int<lower=0> y[N];     // number of successes
  int<lower=0> n[N];     // number of trials
  vector[N] x;           // doses
}
parameters {
  real beta0;            // intercept
  real beta1;            // slope
}
model {
  vector[N] p;
  
  // Priors
  beta0 ~ normal(0, 10);
  beta1 ~ normal(0, 10);
  
  // Likelihood
  for (i in 1:N)
    p[i] = inv_logit(beta0 + beta1 * x[i]);
  
  y ~ binomial(n, p);
}
"

# Data list for Stan
data_list <- list(N = length(y), y = y, n = n, x = x)

# Fit the model using Stan
fit <- stan(model_code = stan_model, data = data_list, iter = 2000, chains = 4)

# Print the results
print(fit)

# Extract the posterior samples
posterior_samples <- as.data.frame(extract(fit))

# Visualize the joint posterior distribution of the parameters
mcmc_scatter(posterior_samples, pars = c("beta0", "beta1")) +
  ggtitle("Joint Posterior Distribution of the Bioassay Parameters") +
  theme_minimal()
