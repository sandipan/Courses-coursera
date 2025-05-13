# Week 1

# monte carlo intgration
set.seed(32)
m = 10000 #100
a = 2
b = 1 / 3
theta <- rgamma(m, shape=a, rate=b)
hist(theta, freq=FALSE)
curve(dgamma(x, shape=a, rate=b), col='blue', add=TRUE)
sum(theta) / m
mean(theta)
a/b

var(theta)
a/b^2

ind = theta < 5
head(ind)
mean(ind)
pgamma(q=5, shape=a, rate=b)
quantile(theta, prob=0.9)
qgamma(p=0.9, shape=a, rate=b)

se = sd(theta) / sqrt(m)
2*se

mean(theta) - 2*se
mean(theta) + 2*se

se = sd(ind) / sqrt(m)
2*se

mean(ind) - 2*se
mean(ind) + 2*se

# hierarchical model

m = 1e5
y = numeric(m)
phi = numeric(m)
for (i in 1:m) {
  phi[i] <- rbeta(1, shape1=2.0, shape2=2.0)
  y[i] <- rbinom(1, size=10, prob=phi[i])
}

# vectorized
phi <- rbeta(m, shape1=2.0, shape2=2.0)
y <- rbinom(m, size=10, prob=phi)

table(y) / m
plot(table(y) / m) # marginal is beta-binomial but conditional is binomial
mean(y)


# markov chain

# discrete random walk

set.seed(34)

n = 100
x = numeric(n)

for (i in 2:n) {
  x[i] = rnorm(1, mean=x[i-1], sd=1.0)
}

plot.ts(x)

Q = matrix(c(0.0, 0.5, 0.0, 0.0, 0.5,
             0.5, 0.0, 0.5, 0.0, 0.0,
             0.0, 0.5, 0.0, 0.5, 0.0,
             0.0, 0.0, 0.5, 0.0, 0.5,
             0.5, 0.0, 0.0, 0.5, 0.0), 
           nrow=5, byrow=TRUE)

Q %*% Q # Matrix multiplication in R. This is Q^2.
(Q %*% Q)[1,3]
Q5 = Q %*% Q %*% Q %*% Q %*% Q # h=5 steps in the future
round(Q5, 3)
Q10 = Q %*% Q %*% Q %*% Q %*% Q %*% Q %*% Q %*% Q %*% Q %*% Q # h=10 steps in the future
round(Q10, 3)
Q30 = Q
for (i in 2:30) {
  Q30 = Q30 %*% Q
}
round(Q30, 3) # h=30 steps in the future
c(0.2, 0.2, 0.2, 0.2, 0.2) %*% Q
n = 5000
x = numeric(n)
x[1] = 1 # fix the state as 1 for time 1
for (i in 2:n) {
  x[i] = sample.int(5, size=1, prob=Q[x[i-1],]) # draw the next state from the intergers 1 to 5 with probabilities from the transition matrix Q, based on the previous value of X.
}
table(x) / n

# continuous random walk
set.seed(38)

n = 1500
x = numeric(n)
phi = -0.6

for (i in 2:n) {
  x[i] = rnorm(1, mean=phi*x[i-1], sd=1.0)
}

plot.ts(x)

hist(x, freq=FALSE)
curve(dnorm(x, mean=0.0, sd=sqrt(1.0/(1.0-phi^2))), col="red", add=TRUE)
legend("topright", legend="theoretical stationary\ndistribution", col="red", lty=1, bty="n")

# Week 2

# Metropolis-Hastings
lg <- function(mu, n, ybar) {
  mu2 <- mu^2
  n*(ybar*mu-mu2/2.0)-log(1.0+mu2)
}

mh <- function(n, ybar, n_iter, mu_init, cand_sd) {
  mu_out <- numeric(n_iter)
  accept <- 0
  mu_now <- mu_init
  lg_now <- lg(mu=mu_now, n=n, ybar=ybar)
  
  for (i in 1:n_iter) {
    
    mu_cand <- rnorm(1, mean=mu_now, sd=cand_sd)
    
    lg_cand <- lg(mu=mu_cand, n=n, y=ybar)
    lalpha <- lg_cand - lg_now
    alpha <- exp(lalpha)
    
    u = runif(1)
    if (u < alpha) {
      mu_now <- mu_cand
      accept <- accept + 1
      lg_now <- lg_cand
    }
    
    mu_out[i] <- mu_now
  }
  
  list(mu=mu_out, accept=accept / n_iter)
  
}

y <- c(1.2, 1.4, -0.5, 0.3, 0.9, 2.3, 1.0, 0.1, 1.3, 1.9)
ybar <- mean(y)
n <- length(y)
hist(y, freq=FALSE, xlim=c(-1,3))
points(y, rep(0, n))
points(ybar, 0, pch=19)
curve(dt(x, df=1), lty=2, add=TRUE)
## posterior sampling
set.seed(43)
post = mh(n=n, ybar=ybar, n_iter=1e3, mu_init=0, cand_sd=3)
str(post)

library(coda)
traceplot(as.mcmc(post$mu))

post = mh(n=n, ybar=ybar, n_iter=1e3, mu_init=0, cand_sd=0.01)
str(post)

library(coda)
traceplot(as.mcmc(post$mu))

post = mh(n=n, ybar=ybar, n_iter=1e3, mu_init=0, cand_sd=0.9)
str(post)

library(coda)
traceplot(as.mcmc(post$mu))

post = mh(n=n, ybar=ybar, n_iter=1e3, mu_init=30, cand_sd=0.9)
str(post)

library(coda)
traceplot(as.mcmc(post$mu))

post$mu_keep <- post$mu[-(1:100)]
plot(density(post$mu_keep), xlim=c(-1,3))
curve(dt(x, df=1), lty=2, add=TRUE)
points(ybar, 0, pch=19)


## JAGS
library(rjags)

mod_string = "model {
  for (i in 1:n) {
    y[i] ~ dnorm(mu, 1.0/sig2)
  }
  mu ~ dt(0.0, 1.0/1.0, 1)
  sig2 = 1.0
}"

set.seed(50)
y <- c(1.2, 1.4, -0.5, 0.3, 0.9, 2.3, 1.0, 0.1, 1.3, 1.9)
ybar <- mean(y)
n <- length(y)
data_jags <- list(y=y, n=n)
params <- c('mu')
inits <- function() {
  inits <- list("mu"=0.0)
}

mod = jags.model(textConnection(mod_string), data=data_jags, inits=inits)

update(mod, 500)

mod_sim = coda.samples(model=mod, variable.names = params, n.iter=1000)

library(coda)
plot(mod_sim)
summary(mod_sim)

## Gibbs Sampling

library(coda)



library("rjags")

mod_string = " model {
  for (i in 1:n) {
    y[i] ~ dnorm(mu, 1.0/sig2)
  }
  mu ~ dt(0.0, 1.0/1.0, 1.0) # location, inverse scale, degrees of freedom
  sig2 = 1.0
} "

set.seed(50)
y = c(1.2, 1.4, -0.5, 0.3, 0.9, 2.3, 1.0, 0.1, 1.3, 1.9)
n = length(y)

data_jags = list(y=y, n=n)
params = c("mu")

inits = function() {
  inits = list("mu"=0.0)
} # optional (and fixed)

mod = jags.model(textConnection(mod_string), data=data_jags, inits=inits)

update(mod, 500) # burn-in

mod_sim = coda.samples(model=mod,
                       variable.names=params,
                       n.iter=1000)

summary(mod_sim)
library("coda")
plot(mod_sim)



update_mu = function(n, ybar, sig2, mu_0, sig2_0) {
  sig2_1 = 1.0 / (n / sig2 + 1.0 / sig2_0)
  mu_1 = sig2_1 * (n * ybar / sig2 + mu_0 / sig2_0)
  rnorm(n=1, mean=mu_1, sd=sqrt(sig2_1))
}

update_sig2 = function(n, y, mu, nu_0, beta_0) {
  nu_1 = nu_0 + n / 2.0
  sumsq = sum( (y - mu)^2 ) # vectorized
  beta_1 = beta_0 + sumsq / 2.0
  out_gamma = rgamma(n=1, shape=nu_1, rate=beta_1) # rate for gamma is shape for inv-gamma
  1.0 / out_gamma # reciprocal of a gamma random variable is distributed inv-gamma
}

gibbs = function(y, n_iter, init, prior) {
  ybar = mean(y)
  n = length(y)
  
  ## initialize
  mu_out = numeric(n_iter)
  sig2_out = numeric(n_iter)
  
  mu_now = init$mu
  
  ## Gibbs sampler
  for (i in 1:n_iter) {
    sig2_now = update_sig2(n=n, y=y, mu=mu_now, nu_0=prior$nu_0, beta_0=prior$beta_0)
    mu_now = update_mu(n=n, ybar=ybar, sig2=sig2_now, mu_0=prior$mu_0, sig2_0=prior$sig2_0)
    
    sig2_out[i] = sig2_now
    mu_out[i] = mu_now
  }
  
  cbind(mu=mu_out, sig2=sig2_out)
}

lg = function(mu, n, ybar) {
  mu2 = mu^2
  n * (ybar * mu - mu2 / 2.0) - log(1 + mu2)
}

mh = function(n, ybar, n_iter, mu_init, cand_sd) {
  ## Random-Walk Metropolis-Hastings algorithm
  
  ## step 1, initialize
  mu_out = numeric(n_iter)
  accpt = 0
  mu_now = mu_init
  lg_now = lg(mu=mu_now, n=n, ybar=ybar)
  
  ## step 2, iterate
  for (i in 1:n_iter) {
    ## step 2a
    mu_cand = rnorm(n=1, mean=mu_now, sd=cand_sd) # draw a candidate
    
    ## step 2b
    lg_cand = lg(mu=mu_cand, n=n, ybar=ybar) # evaluate log of g with the candidate
    lalpha = lg_cand - lg_now # log of acceptance ratio
    alpha = exp(lalpha)
    
    ## step 2c
    u = runif(1) # draw a uniform variable which will be less than alpha with probability min(1, alpha)
    if (u < alpha) { # then accept the candidate
      mu_now = mu_cand
      accpt = accpt + 1 # to keep track of acceptance
      lg_now = lg_cand
    }
    
    ## collect results
    mu_out[i] = mu_now # save this iteration's value of mu
  }
  
  ## return a list of output
  list(mu=mu_out, accpt=accpt/n_iter)
}

#y = c(1.2, 1.4, -0.5, 0.3, 0.9, 2.3, 1.0, 0.1, 1.3, 1.9)
y = c(-0.2, -1.5, -5.3, 0.3, -0.8, -2.2)
ybar = mean(y)
n = length(y)
hist(y, freq=FALSE, xlim=c(-1.0, 3.0)) # histogram of the data
curve(dt(x=x, df=1), lty=2, add=TRUE) # prior for mu
points(y, rep(0,n), pch=1) # individual data points
points(ybar, 0, pch=19) # sample mean
set.seed(43) # set the random seed for reproducibility
post = mh(n=n, ybar=ybar, n_iter=1e3, mu_init=0.0, cand_sd=1.5)
post$accpt
str(post)
traceplot(as.mcmc(post$mu))
autocorr.plot(as.mcmc(post$mu))
effectiveSize(as.mcmc(post$mu)) # effective sample size of ~350
mean(post$mu[(1000-250+1):1000])

## prior
prior = list()
prior$mu_0 = 0.0 #1.0 #0.0
prior$sig2_0 = 0.5 #1.0
prior$n_0 = 2.0 # prior effective sample size for sig2
prior$s2_0 = 1.0 # prior point estimate for sig2
prior$nu_0 = prior$n_0 / 2.0 # prior parameter for inverse-gamma
prior$beta_0 = prior$n_0 * prior$s2_0 / 2.0 # prior parameter for inverse-gamma

hist(y, freq=FALSE, xlim=c(-1.0, 3.0)) # histogram of the data
curve(dnorm(x=x, mean=prior$mu_0, sd=sqrt(prior$sig2_0)), lty=2, add=TRUE) # prior for mu
points(y, rep(0,n), pch=1) # individual data points
points(ybar, 0, pch=19) # sample mean

set.seed(53)

init = list()
init$mu = 0.0

post1 = gibbs(y=y, n_iter=5*1e3, init=init, prior=prior)
head(post1)

library("coda")
plot(as.mcmc(post1))

summary(as.mcmc(post1))

coda::autocorr.plot(as.mcmc(post1$mu))


library("car")  # load the 'car' package
data("Anscombe")  # load the data set
?Anscombe  # read a description of the data
head(Anscombe)  # look at the first few lines of the data
pairs(Anscombe)  # scatter plots for each pair of variables
mod_lm = lm(education ~ ., Anscombe)
plot(mod_lm)


library("rjags")

mod_string = " model {
    for (i in 1:length(education)) {
        education[i] ~ dnorm(mu[i], prec)
        mu[i] = b0 + b[1]*income[i] + b[2]*young[i] + b[3]*urban[i]
    }
    
    b0 ~ dnorm(0.0, 1.0/1.0e6)
    for (i in 1:3) {
        b[i] ~ dnorm(0.0, 1.0/1.0e6)
    }
    
    prec ~ dgamma(1.0/2.0, 1.0*1500.0/2.0)
    	## Initial guess of variance based on overall
    	## variance of education variable. Uses low prior
    	## effective sample size. Technically, this is not
    	## a true 'prior', but it is not very informative.
    sig2 = 1.0 / prec
    sig = sqrt(sig2)
} "

data_jags = as.list(Anscombe)


set.seed(72)
data1_jags = list(education=Anscombe$education, income=Anscombe$income, young=Anscombe$young, urban=Anscombe$urban)

params1 = c("b0", "b", "sig")

inits1 = function() {
  inits = list("b0"=rnorm(1,0.0,100.0),"b"=rnorm(3,0.0,100.0), "prec"=rgamma(1,1.0,1.0))
}

mod1 = jags.model(textConnection(mod_string), data=data1_jags, inits=inits1, n.chains=3)
update(mod1, 1000) # burn-in

mod1_sim = coda.samples(model=mod1,
                        variable.names=params1,
                        n.iter=5000)
plot(mod1_sim)
summary(mod1_sim)
mod1_csim = do.call(rbind, mod1_sim) # combine multiple chains
gelman.diag(mod1_sim)
autocorr.plot(mod1_sim)
effectiveSize(mod1_sim)
summary(mod1_sim)

dic.samples(mod1, n.iter = 1e5)


mod_string = " model {
    for (i in 1:length(education)) {
        education[i] ~ dnorm(mu[i], prec)
        mu[i] = b0 + b[1]*income[i] + b[2]*young[i]
    }
    
    b0 ~ dnorm(0.0, 1.0/1.0e6)
    for (i in 1:2) {
        b[i] ~ dnorm(0.0, 1.0/1.0e6)
    }
    
    prec ~ dgamma(1.0/2.0, 1.0*1500.0/2.0)
    	## Initial guess of variance based on overall
    	## variance of education variable. Uses low prior
    	## effective sample size. Technically, this is not
    	## a true 'prior', but it is not very informative.
    sig2 = 1.0 / prec
    sig = sqrt(sig2)
} "

data_jags = as.list(Anscombe)


set.seed(72)
data1_jags = list(education=Anscombe$education, income=Anscombe$income, young=Anscombe$young)

params1 = c("b0", "b", "sig")

inits1 = function() {
  inits = list("b0"=rnorm(1,0.0,100.0),"b"=rnorm(2,0.0,100.0), "prec"=rgamma(1,1.0,1.0))
}

mod2 = jags.model(textConnection(mod_string), data=data1_jags, inits=inits1, n.chains=3)
update(mod2, 1000) # burn-in

mod2_sim = coda.samples(model=mod2,
                        variable.names=params1,
                        n.iter=5000)

mod2_csim = do.call(rbind, mod2_sim) # combine multiple chains
gelman.diag(mod2_sim)
autocorr.plot(mod2_sim)
effectiveSize(mod2_sim)
summary(mod2_sim)

dic.samples(mod2, n.iter = 1e5)


mod_string = " model {
    for (i in 1:length(education)) {
        education[i] ~ dnorm(mu[i], prec)
        mu[i] = b0 + b[1]*income[i] + b[2]*young[i] + b[3]*income[i]*young[i]
    }
    
    b0 ~ dnorm(0.0, 1.0/1.0e6)
    for (i in 1:3) {
        b[i] ~ dnorm(0.0, 1.0/1.0e6)
    }
    
    prec ~ dgamma(1.0/2.0, 1.0*1500.0/2.0)
    	## Initial guess of variance based on overall
    	## variance of education variable. Uses low prior
    	## effective sample size. Technically, this is not
    	## a true 'prior', but it is not very informative.
    sig2 = 1.0 / prec
    sig = sqrt(sig2)
} "

data_jags = as.list(Anscombe)


set.seed(72)
data1_jags = list(education=Anscombe$education, income=Anscombe$income, young=Anscombe$young)

params1 = c("b0", "b", "sig")

inits1 = function() {
  inits = list("b0"=rnorm(1,0.0,100.0),"b"=rnorm(3,0.0,100.0), "prec"=rgamma(1,1.0,1.0))
}

mod3 = jags.model(textConnection(mod_string), data=data1_jags, inits=inits1, n.chains=3)
update(mod3, 1000) # burn-in

mod3_sim = coda.samples(model=mod3,
                        variable.names=params1,
                        n.iter=5000)

mod3_csim = do.call(rbind, mod3_sim) # combine multiple chains
gelman.diag(mod3_sim)
autocorr.plot(mod3_sim)
effectiveSize(mod3_sim)
summary(mod3_sim)

dic.samples(mod3, n.iter = 1e5)


mod_string = " model {
    for (i in 1:length(y)) {
        y[i] ~ dnorm(mu[grp[i]], prec)
    }
    
    for (j in 1:3) {
        mu[j] ~ dnorm(0.0, 1.0/1.0e6)
    }
    
    prec ~ dgamma(5/2.0, 5*1.0/2.0)
    sig = sqrt( 1.0 / prec )
    mu3_mu1 = mu[3] - mu[1]
} "

set.seed(82)
str(PlantGrowth)
data_jags = list(y=PlantGrowth$weight, 
                 grp=as.numeric(PlantGrowth$group))

params = c("mu", "sig", "mu3_mu1")

inits = function() {
  inits = list("mu"=rnorm(3,0.0,100.0), "prec"=rgamma(1,1.0,1.0))
}

mod = jags.model(textConnection(mod_string), data=data_jags, inits=inits, n.chains=3)
update(mod, 1e3)
dic.samples(mod, n.iter = 1e5)

mod_sim = coda.samples(model=mod,
                       variable.names=params,
                       n.iter=5e3)
summary(mod_sim)
mod_csim = as.mcmc(do.call(rbind, mod_sim)) # combined chains
HPDinterval(mod_csim)
mean(mod_csim[,3] - mod_csim[,1])
HPDinterval(mod_csim[,3] - mod_csim[,1])

mod_string = " model {
    for (i in 1:length(y)) {
        y[i] ~ dnorm(mu[grp[i]], prec[grp[i]])
    }
    
    for (j in 1:3) {
        mu[j] ~ dnorm(0.0, 1.0/1.0e6)
        prec[j] ~ dgamma(5/2.0, 5*1.0/2.0)
        sig[j] = sqrt( 1.0 / prec[j])
    }
    
} "

set.seed(82)
str(PlantGrowth)
data_jags = list(y=PlantGrowth$weight, 
                 grp=as.numeric(PlantGrowth$group))

params = c("mu", "sig")

inits = function() {
  inits = list("mu"=rnorm(3,0.0,100.0), "prec"=rgamma(3,1.0,1.0))
}

mod = jags.model(textConnection(mod_string), data=data_jags, inits=inits, n.chains=3)
update(mod, 1e3)
dic.samples(mod, n.iter = 1e5)

mod_sim = coda.samples(model=mod,
                       variable.names=params,
                       n.iter=5e3)
summary(mod_sim)
#mod_csim = as.mcmc(do.call(rbind, mod_sim)) # combined chains
#plot(mod_sim)
#gelman.diag(mod_sim)
#autocorr.diag(mod_sim)
#effectiveSize(mod_sim)


mod_cm = lm(weight ~ -1 + group, data=PlantGrowth)
summary(mod_cm)


library("MASS")
data("OME")
?OME # background on the data
head(OME)

any(is.na(OME)) # check for missing values
dat = subset(OME, OME != "N/A") # manually remove OME missing values identified with "N/A"
dat$OME = factor(dat$OME)
str(dat)

plot(dat$Age, dat$Correct / dat$Trials )
plot(dat$OME, dat$Correct / dat$Trials )
plot(dat$Loud, dat$Correct / dat$Trials )
plot(dat$Noise, dat$Correct / dat$Trials )

mod_glm = glm(Correct/Trials ~ Age + OME + Loud + Noise, data=dat, weights=Trials, family="binomial")
summary(mod_glm)

plot(residuals(mod_glm, type="deviance"))
plot(fitted(mod_glm), dat$Correct/dat$Trials)

X = model.matrix(mod_glm)[,-1] # -1 removes the column of 1s for the intercept
head(X)


mod_string = " model {
	for (i in 1:length(y)) {
		y[i] ~ dbin(phi[i], n[i])
		logit(phi[i]) = b0 + b[1]*Age[i] + b[2]*OMElow[i] + b[3]*Loud[i] + b[4]*Noiseincoherent[i]
	}
	
	b0 ~ dnorm(0.0, 1.0/5.0^2)
	for (j in 1:4) {
		b[j] ~ dnorm(0.0, 1.0/4.0^2)
	}
	
} "

data_jags = as.list(as.data.frame(X))
data_jags$y = dat$Correct # this will not work if there are missing values in dat (because they would be ignored by model.matrix). Always make sure that the data are accurately pre-processed for JAGS.
data_jags$n = dat$Trials
str(data_jags) # make sure that all variables have the same number of observations (712).
params = c("b0", "b")

mod1 = jags.model(textConnection(mod_string), data=data_jags, n.chains=3)
update(mod1, 5*1e3)

mod1_sim = coda.samples(model=mod1,
                        variable.names=params,
                        n.iter=5e3)
mod1_csim = as.mcmc(do.call(rbind, mod1_sim))

summary(mod1_sim)
## convergence diagnostics
plot(mod1_sim, ask=TRUE)
raftery.diag(mod1_sim)

(pm_coef = colMeans(mod1_csim))
pm_Xb = pm_coef["b0"] + matrix(c(60,0,50,0), nrow=1) %*% pm_coef[1:4]
phat = 1.0 / (1.0 + exp(-pm_Xb))

pm_Xb = pm_coef["b0"] + X %*% pm_coef[1:4]
phat = 1.0 / (1.0 + exp(-pm_Xb))
(tab0.7 = table(phat > 0.7, (dat$Correct / dat$Trials) > 0.7))
sum(diag(tab0.7)) / sum(tab0.7)


library("car")
data("Anscombe")
head(Anscombe)
?Anscombe

Xc = scale(Anscombe, center=TRUE, scale=TRUE)
str(Xc)

data1_jags = as.list(data.frame(Xc))


mod1_string = " model {
    for(i in 1:length(education)) {
        education[i] ~ dnorm(mu[i], prec)
        mu[i] = beta[1]*income[i] + beta[2]*young[i] + beta[3]*urban[i]
    }
    
    for (j in 1:3) {
        beta[j] ~ ddexp(0.0, 1.0)
    }
    
    prec ~ dgamma(1/2.0, 1.0/2.0)
    sig = sqrt(1.0 / prec)
} "

set.seed(72)

params1 = c("beta", "sig")

mod1 = jags.model(textConnection(mod1_string), data=data1_jags, n.chains=3)
update(mod1, 1e3)

mod1_sim = coda.samples(model=mod1,
                        variable.names=params1,
                        n.iter=1e3)

summary(mod1_sim)
## convergence diagnostics
plot(mod1_sim)

gelman.diag(mod1_sim)
autocorr.diag(mod1_sim)
effectiveSize(mod1_sim)




mod3_string = " model {
    for( i in 1:length(y)) {
        y[i] ~ dnorm(mu[woolGrp[i], tensGrp[i]], prec[woolGrp[i], tensGrp[i]])
    }
    
    for (j in 1:max(woolGrp)) {
        for (k in 1:max(tensGrp)) {
            mu[j,k] ~ dnorm(0.0, 1.0/1.0e6)
            prec[j,k] ~ dgamma(1/2.0, 1.0/2.0)
            sig[j,k] = sqrt(1.0 / prec[j,k])
        }
    }
    
    
} "

str(warpbreaks)

data3_jags = list(y=log(warpbreaks$breaks), woolGrp=as.numeric(warpbreaks$wool), tensGrp=as.numeric(warpbreaks$tension))

params3 = c("mu", "sig")

mod3 = jags.model(textConnection(mod3_string), data=data3_jags, n.chains=3)
update(mod3, 1e3)

mod3_sim = coda.samples(model=mod3,
                        variable.names=params3,
                        n.iter=5e3)
mod3_csim = as.mcmc(do.call(rbind, mod3_sim))

plot(mod3_sim, ask=TRUE)

## convergence diagnostics
gelman.diag(mod3_sim)
autocorr.diag(mod3_sim)
effectiveSize(mod3_sim)
raftery.diag(mod3_sim)
(dic3 = dic.samples(mod3, n.iter=1e3))

exp(1.5-0.3*0.8+1.0*1.2)


library("COUNT")
data("badhealth")
mod_string = " model {
    for (i in 1:length(numvisit)) {
        numvisit[i] ~ dpois(lam[i])
        log(lam[i]) = int + b_badh*badh[i] + b_age*age[i] + b_intx*age[i]*badh[i]
    }
    
    int ~ dnorm(0.0, 1.0/1e6)
    b_badh ~ dnorm(0.0, 1.0/1e4)
    b_age ~ dnorm(0.0, 1.0/1e4)
    b_intx ~ dnorm(0.0, 1.0/1e4)
} "



set.seed(102)

data_jags = as.list(badhealth)

params = c("int", "b_badh", "b_age", "b_intx")

mod = jags.model(textConnection(mod_string), data=data_jags, n.chains=3)
update(mod, 1e3)

mod_sim = coda.samples(model=mod,
                       variable.names=params,
                       n.iter=5e3)
mod_csim = as.mcmc(do.call(rbind, mod_sim))

## convergence diagnostics
plot(mod_sim)

gelman.diag(mod_sim)
autocorr.diag(mod_sim)
autocorr.plot(mod_sim)
effectiveSize(mod_sim)

## compute DIC
dic = dic.samples(mod, n.iter=1e3)


mod_string = " model {
    for (i in 1:length(numvisit)) {
        numvisit[i] ~ dpois(lam[i])
        log(lam[i]) = int + b_badh*badh[i] + b_age*age[i]
    }
    
    int ~ dnorm(0.0, 1.0/1e6)
    b_badh ~ dnorm(0.0, 1.0/1e4)
    b_age ~ dnorm(0.0, 1.0/1e4)
} "

set.seed(102)

data_jags = as.list(badhealth)

params = c("int", "b_badh", "b_age")

mod = jags.model(textConnection(mod_string), data=data_jags, n.chains=3)
update(mod, 1e3)

mod_sim = coda.samples(model=mod,
                       variable.names=params,
                       n.iter=5e3)
mod_csim = as.mcmc(do.call(rbind, mod_sim))

## convergence diagnostics
plot(mod_sim)

gelman.diag(mod_sim)
autocorr.diag(mod_sim)
autocorr.plot(mod_sim)
effectiveSize(mod_sim)

## compute DIC
dic2 = dic.samples(mod, n.iter=1e3)

ppois(21, 30)

setwd('H:/courses/Coursera/Current/Bayesian/Week4')
dat = read.csv(file="callers.csv", header=TRUE)
## set R's working directory to the same directory
## as this file, or use the full path to the file.
head(dat)
dat$calls_per_days_active <- dat$calls / dat$days_active
boxplot(dat$calls ~ dat$isgroup2)
boxplot(dat$age ~ dat$isgroup2)
boxplot(dat$calls_per_days_active ~ dat$isgroup2)
table(dat$isgroup2)

mod_string = " model {
    for (i in 1:length(calls)) {
		  calls[i] ~ dpois( days_active[i]*lam[i] )
		  log(lam[i]) = b0 + b[1]*age[i] + b[2]*isgroup2[i]
	  }
    b0 ~ dnorm(0.0, 1.0/1e2)
    for (i in 1:2) {
      b[i] ~ dnorm(0.0, 1.0/1e2) 
    }
} "

set.seed(102)

data_jags = as.list(dat[c('calls', 'age', 'isgroup2', 'days_active')])

params = c("b0", "b")

mod = jags.model(textConnection(mod_string), data=data_jags, n.chains=3)
update(mod, 1e3)

mod_sim = coda.samples(model=mod,
                       variable.names=params,
                       n.iter=5e3)
summary(mod_sim)
plot(mod_sim)

mod_csim = as.mcmc(do.call(rbind, mod_sim))

mean(mod_csim[,2] > 0)


llam_hat = mod_csim[,"b0"] + matrix(c(29, 1), ncol=2) %*% matrix(mod_csim[,1:2], nrow=2)
lam_hat = exp(llam_hat)
lam_hat <- lam_hat * 30
lam_hat[1:5]

(nsim <- length(lam_hat))
y <- rpois(n=nsim, lambda=lam_hat)
plot(table(factor(y, levels=0:18))/nsim, pch=2)
mean(y >= 3)

(pmed_coef = apply(mod_csim, 2, median))
llam_hat = pmed_coef["b0"] + as.matrix(dat[,c(4,3)]) %*% matrix(pmed_coef[1:2], nrow=2)
lam_hat = exp(llam_hat)

hist(lam_hat)

dat$pred_calls <- lam_hat * dat$days_active
boxplot(dat$pred_calls ~ dat$isgroup2)

## convergence diagnostics
plot(mod_sim)

gelman.diag(mod_sim)
autocorr.diag(mod_sim)
autocorr.plot(mod_sim)
effectiveSize(mod_sim)

## compute DIC
dic = dic.samples(mod, n.iter=1e3)

library("rjags")


dat = read.csv(file="pctgrowth.csv", header=TRUE)
head(dat)
dim(dat)
table(dat$grp)

mod_string = " model {
for (i in 1:length(y)) {
  y[i] ~ dnorm(theta[grp[i]], prec)
}

for (j in 1:max(grp)) {
  theta[j] ~ dnorm(mu[j], prec2)
  mu[j] ~ dnorm(0, 1.0/1e6)
}

prec ~ dgamma(1.0/2, 1.0*3/2)
prec2 ~ dgamma(2.0/2, 1.0*1/2)
sig = 1/sqrt(prec)
sig2 = 1/sqrt(prec2)

} "

set.seed(113)

data_jags = as.list(dat)

params = c("mu", "sig", "sig2")

mod = jags.model(textConnection(mod_string), data=data_jags, n.chains=3)
update(mod, 1e3)

mod_sim = coda.samples(model=mod,
                       variable.names=params,
                       n.iter=5e3)
mod_csim = as.mcmc(do.call(rbind, mod_sim))

## convergence diagnostics
plot(mod_sim)
summary(mod_sim)

means_theta = colMeans(mod_csim)
means_theta

gelman.diag(mod_sim)
autocorr.diag(mod_sim)
autocorr.plot(mod_sim)
effectiveSize(mod_sim)

## compute DIC
dic = dic.samples(mod, n.iter=1e3)


means_anova = tapply(dat$y, INDEX=dat$grp, FUN=mean)
means_anova
## dat is the data read from pctgrowth.csv
plot(means_anova)
points(means_theta, col="red") ## where means_theta are the posterior point estimates for the industry means.


library("MASS")
data("OME")

dat = subset(OME, OME != "N/A")
dat$OME = factor(dat$OME) # relabel OME
dat$ID = as.numeric(factor(dat$ID)) # relabel ID so there are no gaps in numbers (they now go from 1 to 63)

## Original reference model and covariate matrix
mod_glm = glm(Correct/Trials ~ Age + OME + Loud + Noise, data=dat, weights=Trials, family="binomial")
X = model.matrix(mod_glm)[,-1]

## Original model (that needs to be extended)
mod_string = " model {
	for (i in 1:length(y)) {
		y[i] ~ dbin(phi[i], n[i])
		logit(phi[i]) = a[ID[i]] + b[1]*Age[i] + b[2]*OMElow[i] + b[3]*Loud[i] + b[4]*Noiseincoherent[i]
	}
	
	for (j in 1:max(ID)) {
	  a[j] ~ dnorm(mu, prec)
	}
  mu ~ dnorm(0, 1/10^2)
  prec ~ dgamma(1/2, 1/2)
	for (j in 1:4) {
		b[j] ~ dnorm(0.0, 1.0/4.0^2)
	}
	sig = 1/sqrt(prec)
} "

data_jags = as.list(as.data.frame(X))
data_jags$y = dat$Correct
data_jags$n = dat$Trials
data_jags$ID = dat$ID


set.seed(113)

params = c("a", "b", "mu", "sig")

mod = jags.model(textConnection(mod_string), data=data_jags, n.chains=3)
update(mod, 1e3)

mod_sim = coda.samples(model=mod,
                       variable.names=params,
                       n.iter=5e3)
mod_csim = as.mcmc(do.call(rbind, mod_sim))

## convergence diagnostics
plot(mod_sim)
summary(mod_sim)

gelman.diag(mod_sim)
autocorr.diag(mod_sim)
autocorr.plot(mod_sim)
effectiveSize(mod_sim)

## compute DIC
dic2 = dic.samples(mod, n.iter=1e3)



library("MASS")
data("OME")

dat = subset(OME, OME != "N/A")
dat$OME = factor(dat$OME) # relabel OME
dat$ID = as.numeric(factor(dat$ID)) # relabel ID so there are no gaps in numbers (they now go from 1 to 63)

## Original reference model and covariate matrix
mod_glm = glm(Correct/Trials ~ Age + OME + Loud + Noise, data=dat, weights=Trials, family="binomial")
X = model.matrix(mod_glm)[,-1]

## Original model (that needs to be extended)
mod_string = " model {
	for (i in 1:length(y)) {
		y[i] ~ dbin(phi[i], n[i])
		logit(phi[i]) = b0 + b[1]*Age[i] + b[2]*OMElow[i] + b[3]*Loud[i] + b[4]*Noiseincoherent[i]
	}
	
	b0 ~ dnorm(0.0, 1.0/5.0^2)
	for (j in 1:4) {
		b[j] ~ dnorm(0.0, 1.0/4.0^2)
	}
	
} "

data_jags = as.list(as.data.frame(X))
data_jags$y = dat$Correct
data_jags$n = dat$Trials

set.seed(113)

params = c("b0", "b")

mod = jags.model(textConnection(mod_string), data=data_jags, n.chains=3)
update(mod, 1e3)

mod_sim = coda.samples(model=mod,
                       variable.names=params,
                       n.iter=5e3)
mod_csim = as.mcmc(do.call(rbind, mod_sim))

## convergence diagnostics
plot(mod_sim)
summary(mod_sim)

gelman.diag(mod_sim)
autocorr.diag(mod_sim)
autocorr.plot(mod_sim)
effectiveSize(mod_sim)

## compute DIC
dic = dic.samples(mod, n.iter=1e3)

