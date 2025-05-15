install.packages("palmerpenguins")
library(palmerpenguins)
data(package = 'palmerpenguins')

install.packages('skimr')
library(skimr)
data('ToothGrowth')
skim_without_charts(ToothGrowth) 

penguins %>% 
  drop_na() %>% 
  group_by(species) %>%
  summarize(min_bl = min(bill_depth_mm))

penguins %>% 
  drop_na() %>%
  group_by(species) %>%
  summarize(mean_mass = mean(body_mass_g))

penguins %>% 
  drop_na() %>% 
  group_by(species) %>%
  summarize(max_fl = max(flipper_length_mm))

head(ToothGrowth)

ggplot(data = penguins) + 
  geom_point(mapping = aes(x = flipper_length_mm, y = body_mass_g)) +
  labs(title="Penguins")

ggplot(data = diamonds) +
  geom_bar(mapping = aes(x = color, fill = cut)) +
  facet_wrap(~cut)

ggplot(data = penguins) +
  geom_point(mapping = aes(x = flipper_length_mm, y = body_mass_g)) +
  geom_point(mapping = aes(x = flipper_length_mm, y = body_mass_g, shape=species))


setwd('C:/courses/coursera/Google - Data Analysis R Programmming')
bars_df <- read.csv("flavors_of_cacao.csv") # read_csv
head(bars_df)
colnames(bars_df)
glimpse(bars_df)
bars_df %>% rename(Maker =  Company...Maker.if.known.)
trimmed_bars_df <- bars_df %>% select(Rating, Cocoa.Percent, Company.Location)
trimmed_bars_df %>%  summarize(mean_Rating = mean(Rating))
trimmed_bars_df %>%  summarize(sd_Rating = sd(Rating))
best_trimmed_bars_df <- trimmed_bars_df %>% filter(Cocoa.Percent >= '70%' & Rating >= 3.5)
ggplot(data = best_trimmed_bars_df) + geom_bar(aes(x=Company.Location))
  
ggplot(data = best_trimmed_bars_df, aes(x=Company.Location)) + geom_bar()  
  
ggplot(data = best_trimmed_bars_df) +
  #geom_bar(mapping = aes(x = Company.Location)) +
  geom_bar(mapping = aes(x = Company.Location, col=Rating))

data.frame(best_trimmed_bars_df %>% group_by(Company.Location) %>% summarize(mr = mean(Rating)) %>% arrange(-mr))

ggplot(data = best_trimmed_bars_df) +
  geom_bar(mapping = aes(x = Rating)) +
  facet_wrap(~Rating)

ggplot(data = trimmed_bars_df) +
  geom_point(mapping = aes(x = Cocoa.Percent, y = Rating))
ggsave('chocolates.jpeg')