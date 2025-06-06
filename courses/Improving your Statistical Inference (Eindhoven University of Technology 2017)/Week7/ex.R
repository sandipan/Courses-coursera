library(pwr)

## One sample (power)
## Exercise 2.5 p. 47 from Cohen (1988)
pwr.t.test(d=0.2,n=60,sig.level=0.10,type="one.sample",alternative="two.sided")

## Paired samples (power)
## Exercise p. 50 from Cohen (1988)
d<-8/(16*sqrt(2*(1-0.6)))
pwr.t.test(d=d,n=40,sig.level=0.05,type="paired",alternative="two.sided")

## Two independent samples (power)
## Exercise 2.1 p. 40 from Cohen (1988)
d<-2/2.8
pwr.t.test(d=d,n=30,sig.level=0.05,type="two.sample",alternative="two.sided")

## Two independent samples (sample size)
## Exercise 2.10 p. 59
pwr.t.test(d=0.3,power=0.75,sig.level=0.05,type="two.sample",alternative="greater")


#NHST
mu1 <- 7.83
mu2 <- 7.78
sd1 <- 1.21
sd2 <- 1.29
n1 <- 400
n2 <- 400
df <- n1 + n2 - 2
s.pooled <- sqrt(((n1-1)*sd1^2 + (n2-1)*sd2^2)/df)
t.stat <- (mu1 - mu2 - 0) / (s.pooled * sqrt(1/n1+1/n2))
d <- abs(mu1 - mu2) / s.pooled # choen's d_s
pt(t.stat, df, lower.tail=FALSE)


#t.test()

library(compute.es)
tes(t=1.74, n.1=30, n.2=31)
tes(t=-0.98, n.1=180, n.2=190, level = 95)

## Two-sample t-test
p.t.two <- pwr.t.test(d=0.3, power=0.8, type="two.sample", alternative="two.sided")
plot(p.t.two)
plot(p.t.two, xlab="sample size per group")

?power.t.test
power.t.test( 20 , 1 , 3 , .05 , NULL , type = "one.sample" )
power.t.test( NULL , 1 , 3 , .05 , .8 , type = "one.sample" )


























# read IMDB
file <-  read.table(gzfile("ftp://ftp.fu-berlin.de/pub/misc/movies/database/temporaryaccess/directors.list.gz"))

# delete empty rows
file <- subset(file, !grepl('^\\s*$', file))

# split in two columns by one or more tabs
file <- strsplit(x = file, split = '\\t+') 

# row bind all itms and create df
df   <- data.frame(do.call(rbind, lapply(file, unlist)))
df