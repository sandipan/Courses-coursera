load(url("http://www.openintro.org/stat/data/ames.RData"))
head(ames)
area <- ames$Gr.Liv.Area
price <- ames$SalePrice
summary(area)
hist(area)
samp0 <- sample(area, 50)
samp1 <- sample(area, 50)
samp2 <- sample(area, 100)
samp3 <- sample(area, 1000)
mean(samp1)
mean(samp2)
mean(samp3)
sample_means50 <- rep(NA, 5000)
for (i in 1:5000) {
	samp <- sample(area, 50)
	sample_means50[i] <- mean(samp)
}
hist(sample_means50)
hist(sample_means50, breaks = 25)
sample_means_small <- rep(NA, 100)
for (i in 1:100) {
	samp <- sample(area, 50)
	sample_means_small[i] <- mean(samp)
}
hist(sample_means_small)
sample_means_small
sample_means10 <- rep(NA, 5000)
sample_means100 <- rep(NA, 5000)
for (i in 1:5000) {
	samp <- sample(area, 10)
	sample_means10[i] <- mean(samp)
	samp <- sample(area, 100)
	sample_means100[i] <- mean(samp)
}
par(mfrow = c(3, 1))
xlimits = range(sample_means10)
hist(sample_means10, breaks = 20, xlim = xlimits)
hist(sample_means50, breaks = 20, xlim = xlimits)
hist(sample_means100, breaks = 20, xlim = xlimits)


population <- ames$Gr.Liv.Area
samp <- sample(population, 60)
sample_mean <- mean(samp)
se <- sd(samp)/sqrt(60)
lower <- sample_mean - 1.96 * se
upper <- sample_mean + 1.96 * se
c(lower, upper)

samp_mean <- rep(NA, 50)
samp_sd <- rep(NA, 50)
n <- 60
for(i in 1:50) {
	samp <- sample(population, n) # obtain a sample of size n = 60 from the population
	samp_mean[i] <- mean(samp) # save sample mean in ith element of samp_mean
	samp_sd[i] <- sd(samp) # save sample sd in ith element of samp_sd
}
lower <- samp_mean - 1.96 * samp_sd/sqrt(n)
upper <- samp_mean + 1.96 * samp_sd/sqrt(n)
c(lower[1], upper[1])
plot_ci(lower, upper, mean(population))



load(url("http://www.openintro.org/stat/data/kobe.RData"))
head(kobe)
kobe$basket[1:9]
kobe_streak <- calc_streak(kobe$basket)
barplot(table(kobe_streak))
hist(kobe_streak)
summary(kobe_streak)
b <- kobe$basket
n <- length(b)
nH <- length(b[b == 'H'])
n
nH
nH / n
nHH <- 0
for (i in 1:(n-1)) {
	if (b[i] == 'H' & b[i+1] == 'H') {
		nHH <- nHH + 1
	}
}
nHH
nHH / nH

outcomes <- c("heads", "tails")
sample(outcomes, size = 1, replace = TRUE)
sim_fair_coin <- sample(outcomes, size = 100, replace = TRUE)
sim_fair_coin
table(sim_fair_coin)

sim_unfair_coin <- sample(outcomes, size = 100, replace = TRUE, prob = c(0.2,0.8))
table(sim_unfair_coin)

outcomes <- c("H", "M")
sim_basket <- sample(outcomes, size = n, replace = TRUE, prob = c(0.45,0.55))
table(sim_basket)
sim_streak <- calc_streak(sim_basket)
barplot(table(sim_streak))
