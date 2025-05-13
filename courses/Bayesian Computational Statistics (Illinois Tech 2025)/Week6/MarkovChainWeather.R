# Load necessary library
library(ggplot2)

# Define states
states <- c("Sunny", "Rainy")

# Define transition matrix
transition_matrix <- matrix(c(0.8, 0.2, 0.4, 0.6), nrow = 2, byrow = TRUE)
colnames(transition_matrix) <- states
rownames(transition_matrix) <- states

# Number of days to simulate
num_days <- 10

# Initialize the weather on day 1
weather <- "Sunny"

# Vector to store the weather over days
weather_simulation <- character(num_days)
weather_simulation[1] <- weather

# Simulate the Markov chain
set.seed(3)  # For reproducibility
for (day in 2:num_days) {
  current_state <- which(states == weather)
  weather <- sample(states, 1, prob = transition_matrix[current_state, ])
  weather_simulation[day] <- weather
}

# Create a data frame for plotting
weather_data <- data.frame(
  Day = 1:num_days,
  Weather = factor(weather_simulation, levels = states)
)

# Print the simulated weather over days
print(weather_simulation)

# Plot the results
ggplot(weather_data, aes(x = Day, y = Weather, group = 1)) +
  geom_line(aes(color = Weather), size = 1) +
  geom_point(aes(color = Weather), size = 4) +
  scale_color_manual(values = c("Sunny" = "red", "Rainy" = "blue")) +
  labs(title = "Weather Simulation Using Markov Chain",
       x = "Day",
       y = "Weather State") +
  theme_minimal() +
  theme(panel.grid.major = element_blank(),
        panel.grid.minor = element_blank())