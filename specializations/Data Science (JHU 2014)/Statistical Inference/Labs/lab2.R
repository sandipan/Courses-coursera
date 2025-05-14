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
