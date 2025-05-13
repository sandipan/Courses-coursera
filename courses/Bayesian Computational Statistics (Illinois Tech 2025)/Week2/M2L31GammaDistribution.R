# Load necessary library
library(ggplot2)

# Parameters for the Gamma distribution
alpha <- 3.0
beta <- 5.0

# Generate a sequence of x values
x <- seq(0, 3, length.out = 1000)

# Compute the density of the Gamma distribution
y <- dgamma(x, shape = alpha, rate = beta)

# Create a data frame for plotting
df <- data.frame(x = x, y = y)

# Calculate the mean of the Gamma distribution
mean_value <- alpha / beta

# Plot the Gamma distribution
ggplot(df, aes(x = x, y = y)) +
  geom_line(color = 'blue', size = 1) +
  geom_vline(xintercept = mean_value, color = 'red', linetype = "dashed", linewidth = 1) +
  labs(title = 'Gamma Distribution with Mean', x = 'x', y = 'Density') +
  annotate("text", x = mean_value + 0.5, y = max(y) / 2, label = paste("Mean =", round(mean_value, 2)), color = "red") +
  theme_minimal()



# Notes on running this: 

# Make sure ggplot2 is installed. Within the console, run: 
# install.packages("ggplot2")

# To run the entire script, click the Source button at the 
# top right of the script editor or use the shortcut 
# Ctrl+Shift+Enter (Windows/Linux) or Cmd+Shift+Enter (Mac).
# The plot will appear in the plots pane 
