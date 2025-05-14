#phi((12-x)/(4/sqrt(100))) > qnorm(0.975))
#x < 12-(4/sqrt(100))*qnorm(0.975)
12-(4/sqrt(100))*qnorm(0.95)
pnorm((12-11.3)/(4/sqrt(100)), lower.tail=FALSE)

x <- c(140,138,150,148,135)
y <- c(138,136,148,146,133)
t.test(x, y, paired = FALSE, alternative = 'two.sided')
t.test(x, y, paired = TRUE, alternative = 'two.sided', var.equal = TRUE)
t.test(x-y, mu=0, alternative = 'two.sided')

sd(x)
sd(y)
diff <- x-y
2*pt(abs(mean(diff) / (sd(diff) / sqrt(100))), df=5-1, lower.tail = FALSE)

new <- c(0.929,-1.745,1.677,0.701,0.128)
old <- c(2.223,-2.513,1.204,1.938,2.533)
t.test(new, old, paired = TRUE, alternative = 'less')
t.test(new-old, mu=0, alternative = 'less')
diff <- new - old
exp(mean(diff) + c(-1,1)*qt(0.975, df=5-1)*(sd(diff) / sqrt(5)))

compute.power <- function(mu_a_mu, sigma, n, alpha) {
  return(pnorm(qnorm(1-alpha) - (mu_a_mu/(sigma/sqrt(n))), lower.tail = FALSE))
}


compute.power(2, 4, 16, 0.05)
compute.power(2, 4, 16, 0.025) # two-sided

compute.nsamples <- function(alpha, beta, ES) {  # ES = abs(mu_a - mu_0) / sigma
  return(((qnorm(1-alpha)+qnorm(beta))/ES)**2)
}

compute.nsamples(0.05, 0.9, 0.01/0.04)
#compute.nsamples(0.025, 0.90, 0.01/0.04)
#(4*(qnorm(0.95) + qnorm(0.9) - 1))**2

pnorm(qnorm(0.975) - 2/(12/sqrt(288)), lower.tail = FALSE)
2*pnorm(abs(qnorm(0.975) - 2/(12/sqrt(288))), lower.tail = FALSE)

Sp <- sqrt(((9-1)*1.5^2+(9-1)*1.8^2) / (9+9-2))
2*pt((3-(-1))/(Sp*sqrt(1/9+1/9)), df=9+9-2, lower.tail = FALSE)

ts <- (3/4-1/2) / sqrt((1/2*1/2)/4)
2*pnorm(ts, lower.tail = FALSE)

pbinom(2, 4, .5, lower.tail = FALSE) # one-sided
2*pbinom(2, 4, .5, lower.tail = FALSE) # 2-sided
binom.test(3, 4, .5, alternative = 'two.sided')

p1 <- 0.70
p2 <- 0.15
OR <- (70*85) / (15*30)
pnorm(log(p1/p2)/sqrt((1-p1)/(p1*100)+(1-p2)/(p2*100)), lower.tail = FALSE)
pnorm(log(OR)/sqrt(1/70+1/30+1/85+1/15), lower.tail = FALSE)
pnorm((p1-p2)/sqrt(p1*(1-p1)/100 + p2*(1-p2)/100), lower.tail = FALSE)

p1 <- 0.7
p2 <- 0.15
p <- (70 + 15) / (100 + 100)
ts <- (p1 - p2)/sqrt(p * (1 - p) * 2/100)
ts
pnorm(ts, lower.tail = FALSE)

p1 <- 45 / (45+21)
p2 <- 15 / (15+52)
n1 <- 45+21
n2 <- 15+52
SE_logRR <- sqrt((1-p1)/p1/n1 + (1-p2)/p2/n2)
SE_logRR

OR <- (45*52) / (15*21)
SE_logODDs <- sqrt(1/45+1/52+1/15+1/21)
SE_logODDs

n1 <- 100
n2 <- 200
a1 <- 2
b1 <- 2
a2 <- 2
b2 <- 2
x1 <- 60
x2 <- 110
p1 <- rbeta(10000, a1+x1, n1+b1-x1)
p2 <- rbeta(10000, a2+x2, n2+b2-x2)
hist(p1-p2)
mean(p1-p2)

(x1+a1) / (n1+a1+b1) - (x2+a2) / (n2+a2+b2)

chi.sq.test <- function(table) { # independence test
  marginal.row <- rowSums(table)
  marginal.col <- colSums(table)
  total <- sum(table)
  observed <- table
  expected <- table
  for (i in 1:nrow(table)){
    for (j in 1:ncol(table)) {
      expected[i, j] <- marginal.row[i] * marginal.col[j] / total
    }
  }
  TS = sum((observed - expected)**2 / expected)
  p.value = pchisq(TS, df=(nrow(table)-1)*(ncol(table)-1), lower.tail = FALSE)
  print(TS)
  print(p.value)
}

table <- matrix(c(44,77,56,43), nrow=2)
chi.sq.test(table)
chisq.test(table, correct=FALSE)
chisq.test(table)
           
table <- matrix(c(80,60,15,30,5,10), nrow=2)
chi.sq.test(table)
chisq.test(table, correct=FALSE)
chisq.test(table)

table <- matrix(c(43,4,8,45), nrow=2)
chi.sq.test(table)
chisq.test(table, correct=FALSE)
chisq.test(table)


compute.extreme.tables <- function(table) {
  r <- rowSums(table)
  n1_ <- r[1] 
  n2_ <- r[2]
  c <- colSums(table)
  n_1 <- c[1]
  n_2 <- c[2]
  x <- table[1,1]
  z <- n_1
  p <- choose(n1_, x) * choose(n2_, z-x) / choose(n1_+n2_, z)
  #print('current table')
  #print(table)
  #print(p)
  count <- 0
  tot_pr <- 0
  for (x in table[1,1]:n_1) {
    c11 <- x
    c21 <- n_1-x
    c12 <- n1_-x
    c22 <- n2_-n_1+x
    if (all(c(c11, c12, c21, c22) >= 0)) {
      print(matrix(c(c11,c21,c12,c22), ncol=2))
      pr <- choose(n1_, c11) * choose(n2_, n_1-c11) / choose(n1_+n2_, n_1)
      print(pr)
      tot_pr <- tot_pr + pr
      if (pr <= p) {
        print('more extreme!')
        count <- count + 1
      }
    }
  }
  print(count)
  print(tot_pr)
}

table <- matrix(c(4,2,1,3), ncol=2)
compute.extreme.tables(table)
fisher.test(table, alternative='greater')

table <- matrix(c(4,1,2,6), ncol=2)
compute.extreme.tables(table)
fisher.test(table, alternative='greater')

table <- matrix(c(3,2,1,4), ncol=2)
compute.extreme.tables(table)
fisher.test(table, alternative='greater')

chi.sq.GOF <- function(observed, expected) {
  total <- sum(observed)
  expected <- total*expected
  print(expected)
  TS = sum((observed - expected)**2 / expected)
  p.value = pchisq(TS, df=length(observed)-1, lower.tail = FALSE)
  print(TS)
  print(p.value)
}

chi.sq.GOF(c(254,235,267,244),rep(1/4,4))
chi.sq.GOF(c(140,100,50),c(0.53,0.35,0.12))
benford.prob <- c()
for (d in 1:9)
  benford.prob <- round(c(benford.prob, log10(d+1)-log10(d)), 3)
benford.prob
chi.sq.GOF(c(275,183,133,111,76,66,66,44,46),benford.prob)

chi.sq.GOF(c(46,54,49,51),rep(1/4,4))


dat <- matrix(c(65, 70, 15, 35, 30, 85), 3)
dat
colSums(dat)/sum(dat)

chi.sq.GOF(c(65,15),c(1/2,1/2))
chi.sq.GOF(c(70,30),c(1/2,1/2))
chi.sq.GOF(c(30,85),c(1/2,1/2))

compute.common.odds.ratio <- function(lst.tables) {
  num <- 0
  den <- 0
  for (i in 1:length(lst.tables)) {
     table <- lst.tables[[i]]
     x <- table[1,1]*table[2,2] 
     y <- table[1,2]*table[2,1]
     n <- sum(table)
     num <- num + x / n
     den <- den + y / n
  }
  return (num / den)
}

table.low.age <- matrix(c(8,52,5,164), ncol=2)
table.high.age <- matrix(c(25,29,21,128), ncol=2)
lst.tables <- list()
lst.tables[[1]] <- table.low.age
lst.tables[[2]] <- table.high.age
compute.common.odds.ratio(lst.tables)
dat <- array(c(8, 52, 5, 164, 25, 29, 21, 128), c(2, 2, 2))
mantelhaen.test(dat, correct = FALSE)

S <- matrix(sample(c(-1,1), 3000, replace=TRUE), ncol = 3)
S <- S[!duplicated(S),]
for (i in 1:nrow(S)) {
  X <- S[i,] * (1:3)
  print(wilcox.test(X, exact=TRUE)$p.value)
}

S <- matrix(sample(c(-1,1), 3000, replace=TRUE), ncol = 3)
S <- S[!duplicated(S),]
for (i in 1:nrow(S)) {
  X <- S[i,] * (1:3)
  m <- mean(X)
  s <- sd(X)
  W <- sum(X)
  z <- (W-m)/s
  p.value <- ifelse(z > 0, pnorm(z, lower.tail=FALSE), pnorm(z))
  print(2*p.value)
}

p.values <- replicate(10000,
          {
            #X <- rnorm(3, 20, 100)
            #X <- sign(X)*sort(abs(X), index.return=TRUE)$ix
            s <- sample(c(-1,1), 3, replace=TRUE)
            X <- s * (1:3)
            W <- sum(X)
            TS <- (W - mean(X)) / sd(X)
            #n <- 3
            #TS <- (W - n*(n+1)/4) / sqrt(n*(n+1)*(2*n+1)/24)
            #2*pnorm(TS, lower.tail=FALSE)
            #p.value <- ifelse(TS > 0, pnorm(TS, lower.tail=FALSE), pnorm(TS))
            #2*p.value
            TS
          })
table(p.values)
hist(p.values)
min(p.values)

do.mcnemar.test <- function(table) {
  n12 <- table[1,2]
  n21 <- table[2,1]
  TS <- (n12 - n21)^2 / (n12 + n21)
  p_value <- pchisq(TS, df=1, lower.tail=FALSE)
  return(p_value)
}

do.mcnemar.test.exact <- function(table) {
  n12 <- table[1,2]
  n21 <- table[2,1]
  return(pbinom(n21, n12+n21, 0.5, lower.tail=TRUE))
}

table <- matrix(c(5,1,4,0), nrow=2)
table <- matrix(c(55,12,41,20), nrow=2)
#2 * pbinom(3, 5, 0.5, lower.tail = FALSE)
do.mcnemar.test(table)
#mcnemar.test(table, correct=TRUE)
mcnemar.test(table, correct=FALSE)
2*do.mcnemar.test.exact(table) # 2-sided

rowSums(table)
colSums(table)

compute.OR <- function(table) {
  return((table[1,1]*table[2,2]) / (table[1,2]*table[2,1]))
}

case.exposure.table <- matrix(c(243,54,189,153), nrow=2)
#case.exposure.table <- matrix(c(rowSums(table), colSums(table)), nrow=2)
compute.OR(case.exposure.table)
#(432/207) / (297/342)
(243/54) / (243/189)

p1 <- 243/(243+54)
p2 <- 189/(189+153)
p <- (243 + 189) / (297 + 342)
ts <- (p1 - p2)/sqrt(p * (1 - p) * 2/639)
ts
pnorm(ts, lower.tail = FALSE)

mcnemar.test(matrix(c(243, 189, 54, 153), 2), correct = FALSE)


for (n in 1:20)
  for (k in 1:n)
    if (binom.test(k,n)$p.value < 0.05)
      print(paste(k, n, binom.test(k,n)$p.value))

for (k in 0:5)
  print(paste(k, binom.test(k,5,p=0.9, alternative = 'less')$p.value))


expCase <- 243 + 189
unexpCase <- 54 + 153
expCtrl <- 243 + 54
unexpCtrl <- 189 + 153

## marginal odds ratio
expCase * unexpCtrl/(unexpCase * expCtrl)



#1 / 2^n
1/(2^(1:5))

0.9^5
#[1] 0.59049
0.8^5
#[1] 0.32768