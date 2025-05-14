setwd("E:/Academics/Coursera/Labs")
source("http://bit.ly/dasi_inference")
#load(url("http://www.openintro.org/stat/data/atheism.RData"))
load("atheism.RData")
names(atheism)
head(atheism)
us12 = subset(atheism, atheism$nationality == "United States" & atheism$year == "2012")
100* nrow(us12[us12$response == 'atheist',]) / nrow(us12)
inference(us12$response, est = "proportion", type = "ci", method = "theoretical", success = "atheist")
n <- 1000
p <- seq(0, 1, 0.01)
me <- 2 * sqrt(p * (1 - p)/n)
plot(me ~ p)
spain = subset(atheism, atheism$nationality == "Spain")
inference(y=spain$response, x=spain$year, est = "proportion", type = "ht", null = 0, alternative = "twosided", method = "theoretical", success = "atheist")
us = subset(atheism, atheism$nationality == "United States")
inference(y=us$response, x=us$year, est = "proportion", type = "ht", null = 0, alternative = "twosided", method = "theoretical", success = "atheist")
countries <- c("Japan","Czech Republic","France","Korea","Rep (South)","Germany","Netherlands","Austria","Iceland","Canada","Spain","Switzerland","Hong Kong","Italy","Argentina","Russian Federation","Finland","Moldova","United States","Poland","South Africa","Bosnia and Herzegovina","Ukraine","Colombia","Cameroon","India","Peru","Serbia","Bulgaria","Pakistan","Ecuador","Kenya","Turkey","Lithuania","Romania","Macedonia","Nigeria","Malaysia","Ghana","Vietnam")
unique(atheism$nationality)
#unique(countries)
sink("hyp-res.txt")
for (cn in countries) {
	print(cn)
	d <- subset(atheism, atheism$nationality == cn)
	inference(y=d$response, x=d$year, est = "proportion", type = "ht", null = 0, alternative = "twosided", method = "theoretical", success = "atheist")
}
sink()

d <- readLines("hyp-res.txt")
grep('p-value\\s+=\\s+0\\.\\d+', d, value=TRUE)

#1.96 * sqrt(p*(1-p)/n) = 0.01 =>
1.96*0.5 / 0.01