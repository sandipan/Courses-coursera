setwd('C:\\courses\\Coursera\\Current\\Data Visualization')
df <- read.csv('Week1\\gapminder.csv')
library(ggplot2)
ggplot(df, aes(incomeperperson)) +   geom_histogram(aes(y=..density..),      # Histogram with density instead of count on y-axis
                                                    binwidth=1000,
                                                    colour="black", fill="white") +
  geom_density(alpha=.2, fill="#FF6666") +  # Overlay with transparent density plot 
  scale_x_continuous(breaks=seq(0, 120000, 10000)) +
  scale_y_continuous(breaks=seq(0, 0.001, 0.00005)) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1), text = element_text(size = 20))

summary(df$incomeperperson)