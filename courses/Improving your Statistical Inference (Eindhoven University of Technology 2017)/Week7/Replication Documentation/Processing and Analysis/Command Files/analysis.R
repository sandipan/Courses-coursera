# Read data

dfs <- read.csv('Satyajit_Ray.csv', check.names = FALSE)
dfa <- read.csv('Akira_Kurosawa.csv', check.names=FALSE)

# Justify the sample size

library(pwr)
p.t.two <- pwr.t.test(d=0.8,power=0.84,sig.level=0.05,type="two.sample",alternative="two.sided")
print(p.t.two)
## 
##      Two-sample t test power calculation 
## 
##               n = 29
##               d = 0.78948
##       sig.level = 0.05
##           power = 0.84
##     alternative = two.sided
## 
## NOTE: n is number in *each* group
plot(p.t.two, xlab="sample size per group")

# Specify the statistical test to conduct

# NHST two-sided t-test 
# 1. with t.test
t.test(dfs[,2], dfa[,2], alternative='two.sided', conf.level=0.9)
## 
##  Welch Two Sample t-test
## 
## data:  dfs[, 2] and dfa[, 2]
## t = 2.6853, df = 46.646, p-value = 0.01
## alternative hypothesis: true difference in means is not equal to 0
## 90 percent confidence interval:
##  0.1444567 0.6258881
## sample estimates:
## mean of x mean of y 
##  8.055172  7.670000

# 2. with formula
n1 <- length(dfs[,2])
n2 <- length(dfa[,2])
mu1 <- mean(dfs[,2])
mu2 <- mean(dfa[,2])
sd1 <- sd(dfs[,2]) 
sd2 <- sd(dfa[,2]) 
df <- n1 + n2 - 2
s.pooled <- sqrt(((n1-1)*sd1^2 + (n2-1)*sd2^2)/df)
t.stat <- (mu1 - mu2 - 0) / (s.pooled * sqrt(1/n1+1/n2))
p.value <- pt(t.stat, df, lower.tail=FALSE)
print(paste0('t.stat=', t.stat, ' df=', df, ' p.value=', p.value, 
            ' CI=(', (mu1-mu2)-qt(0.95, df)*s.pooled*sqrt(1/n1+1/n2), ',',  (mu1-mu2)+qt(0.95,df)*s.pooled*sqrt(1/n1+1/n2), ')'))
## [1] "t.stat=2.66216514176719 df=57 p.value=0.00503579567833758 CI=(0.143256766714653,0.627088060871554)"
			
d <- abs(mu1 - mu2) / s.pooled # choen's d_s
print(paste('Obeserved effect size (Cohen\'s d_s) = ', d))
## [1] "Obeserved effect size (Cohen's d_s) =  0.693268347374739"

# 90% confidence intervals around the effect size and check if it contains d=0.8
library(compute.es)
tes(t=(mu1 - mu2 - 0) / (s.pooled * sqrt(1/n1+1/n2)), n.1=n1, n.2=n2)

## Mean Differences ES: 
##  
##  d [ 95 %CI] = 0.69 [ 0.16 , 1.23 ] 
##   var(d) = 0.07 
##   p-value(d) = 0.01 
##   U3(d) = 75.59 % 
##   CLES(d) = 68.8 % 
##   Cliff's Delta = 0.38 