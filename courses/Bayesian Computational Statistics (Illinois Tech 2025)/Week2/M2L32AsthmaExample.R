# Load necessary library
library(ggplot2)

# Prior parameters
alpha_prior <- 3.0
beta_prior <- 5.0

# Likelihood parameters
lambda <- 2.0 * 1.5  # Poisson(2.0 * theta) where theta = 1.5

# Posterior parameters
alpha_post <- alpha_prior + 2.0  # adding the observed count (since lambda is 2 * theta)
beta_post <- beta_prior + 2.0  # adding the scale parameter of the Poisson (2.0)

# Generate a sequence of theta values
theta <- seq(0, 2, length.out = 1000)

# Compute the density of the Gamma prior distribution
prior <- dgamma(theta, shape = alpha_prior, rate = beta_prior)

# Compute the likelihood of the Poisson distribution
likelihood <- dpois(2.0 * theta, lambda = lambda)

# Compute the density of the Gamma posterior distribution
posterior <- dgamma(theta, shape = alpha_post, rate = beta_post)

# Calculate the means of the distributions
mean_prior <- alpha_prior / beta_prior
mean_likelihood <- lambda / 2.0
mean_posterior <- alpha_post / beta_post

# Create a data frame for plotting
df <- data.frame(theta = theta, prior = prior, likelihood = likelihood, posterior = posterior)

# Plot the distributions
ggplot(df, aes(x = theta)) +
  geom_line(aes(y = prior), color = 'blue', size = 1, linetype = "solid", label = "Prior") +
  geom_line(aes(y = posterior), color = 'red', size = 1, linetype = "dotted", label = "Posterior") +
  geom_vline(xintercept = mean_prior, color = 'blue', linetype = "solid") +
  geom_vline(xintercept = mean_likelihood, color = 'green', linetype = "dashed") +
  geom_vline(xintercept = mean_posterior, color = 'red', linetype = "dotted") +
  annotate("text", x = mean_prior + 0.1, y = 0.75, label = paste("Mean Prior =", round(mean_prior, 2)), color = "blue") +
  annotate("text", x = mean_likelihood + 0.1, y = 1, label = paste("Mean Likelihood =", round(mean_likelihood, 2)), color = "green") +
  annotate("text", x = mean_posterior + 0.1, y = 0.5, label = paste("Mean Posterior =", round(mean_posterior, 2)), color = "red") +
  labs(title = 'Prior, Likelihood, and Posterior Distributions with Means', x = expression(theta), y = 'Density') +
  theme_minimal() +
  theme(legend.position = "bottom") +
  guides(color = guide_legend("Distributions")) +
  theme(legend.title = element_blank()) +
  scale_color_manual(values = c('blue', 'green', 'red'),
                     labels = c('Prior', 'Likelihood', 'Posterior'))
