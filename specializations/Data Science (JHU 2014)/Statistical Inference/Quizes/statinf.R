data(sleep)
head(sleep)
g1 <-sleep$extra[1:10]
g2 <-sleep$extra[11:20]
difference <- g2 - g1
mn <- mean(difference)
s <- sd(difference)
n <- 10
mn + c(-1, 1) * qt(0.975, n - 1) * s/sqrt(n)
t.test(difference)$conf.int

Quiz-4
------
1. n <- 100
   xbar <- 12
   s <- 4
   # 0.05 = P((xbar - x)/(s/sqrt(n)) >= 1.645 | mu = x) => 12 - x >= (4/10)*1.645 => x <= 12 - (4/10)*1.645
2. x <- c(140, 138, 150, 148, 135)
   y <- c(132, 135, 151, 146, 130)
   t.test(x, y, paired=TRUE)
3. xbar <- 1100
   s <- 30
   n <- 9
   #(xbar - mu0) / (s/sqrt(n))
   #abs(mu0 - 1100) / 10 <= qt(0.975, n-1)
   1100 + 10*qt(0.975, n-1)
   1100 - 10*qt(0.975, n-1)
4. phat <- 0.75
   p <- 0.5
   q <- 1 - p
   n <- 4
   z <- (phat - p) / sqrt(p*q/n)
   pval <- 2*(1 - pnorm(z))
5. phat <- 10 / 1787
   p <- 0.01
   n <- 1787
   q <- 1 - p
   z <- (phat - p) / sqrt(p*q/n)
   pval <- pnorm(z)
7. x1bar <- -3
   x2bar <- 1
   n <- 9
   s_x1 <- 1.5
   s_x2 <- 1.8
   s_x1_x2 <- sqrt(0.5*(s_x1^2 + s_x2^2))
   tstat <- (x1bar - x2bar) / (s_x1_x2 * sqrt(2/n))
   tdf <- 2*n - 2
   pt(tstat, tdf)
8. power.t.test(n = 100, delta = 0.01, sd = 0.04, type = "one.sample", alt = "one.sided")$power   
9. power.t.test(n = 138, delta = 0.01, sd = 0.04, type = "one.sample", alt = "one.sided")$power   
   power.t.test(n = 139, delta = 0.01, sd = 0.04, type = "one.sample", alt = "one.sided")$power   
11. n <- 288
    x1bar <- 44
	x2bar <- 42.04
	s1 <- 12
	s2 <- 12
	zstat <- (x1bar - x2bar) / (sqrt(s1^2/n+s2^2/n))
    2*(1-pnorm(zstat))
12. m <- 10
	alpha <- 0.05
	alpha_fwer <- alpha / m

Quiz-3
------
1.	n <- 9
	mn  <- 1100
	s <- 30
    #(mn - u) / (s/sqrt(n)) -> N(0,1) 
	# P(abs(u - mn) / (s/sqrt(n)) <= 0.05) = P(-0.025 <= (u - mn) / (s/sqrt(n)) <= 0.025)
	mn + c(-1, 1) * qt(0.975, n - 1) * s/sqrt(n)
	
2.	n <- 9
	mn <- -2
	me <- c(-1, 1) * qt(0.975, n - 1) / sqrt(n)
	#me =  [-0.768668  0.768668]
	#mn + s*me = [-2 - 0.768668s, -2 + 0.768668s]
	#=> -2 + 0.768668s < 0 => s < 2 / 0.768668
	s <- 2.601904
	mn + c(-1, 1) * qt(0.975, n - 1) * s/sqrt(n)

4.  mn <- 3 - 5
	s <- sqrt(0.5*(0.60 + 0.68))
	n <- 10
	mn + c(-1, 1) * qt(0.975, 2*n - 2) * s/sqrt(n/2)
	
6.  mn <- 6 - 4
	s <- sqrt(0.5*(0.25 + 4))
	n <- 100
	ci <- mn + c(-1, 1) * qt(0.975, 2*n - 2) * s/sqrt(n/2)
	ci
	
7.  mn <- -3 -1
	s <- sqrt(0.5*(1.5^2 + 1.8^2))
	n <- 9
	ci <- mn + c(-1, 1) * qt(0.95, 2*n - 2) * s/sqrt(n/2)
	ci
	
Quiz-2
------
2. Pr(p|t)  = Pr(t|p)Pr(p) / (Pr(t|p)Pr(p) + Pr(t|~p)Pr(~p)) = 1 / (1 + Pr(t|~p)Pr(~p) / Pr(t|p)Pr(p)) =  1 / (1 + 0.48*0.7/(0.75*0.3)),           Pr(p) = 0.3, Pr(t|p) = 0.75, Pr(~t|~p) = 0.52
3. pnorm((70-80)/10)
4. (x-1100)/75=qnorm(.95) => x = 1100 + 75*qnorm(.95)
5. (x-1100)/(75/sqrt(100))=qnorm(.95) => x = 1100 + 7.5*qnorm(.95)
7. Pr(z <= (16 - 15) / (10/sqrt(100)) & z >= (14 - 15) / (10/sqrt(100))) = Pr(z >= -1 & z <= 1) = Phi(1) - Phi(-1) = pnorm(1) - pnorm(-1)
8. (xbar - .5) / (1/sqrt(1000*12)) -> N(0,1) => xbar -> .5
9. var(xbar) . n / (n-1) -> 1/12 => sd(sbar) -> sqrt((1 - 1/1000)*(1/12))

