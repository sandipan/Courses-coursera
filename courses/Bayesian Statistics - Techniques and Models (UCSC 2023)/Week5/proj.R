#https://www.kaggle.com/datasets/mathchi/diabetes-data-set
setwd('H:/courses/Coursera/Current/Bayesian/Week5')

dat = read.csv(file="diabetes.csv", header=TRUE)
head(dat)
summary(dat)
dat = na.omit(dat)
dim(dat)
pairs(dat)
100*colSums(dat == 0) / nrow(dat)

library("corrplot")
Cor = cor(dat)
corrplot(Cor, type="upper", method="ellipse", tl.pos="d")
corrplot(Cor, type="lower", method="number", col="black", 
         add=TRUE, diag=FALSE, tl.pos="n", cl.pos="n")

vars <- colnames(dat)
col.means <- sapply(dat, function(x) mean(x[x!=0]))

for (var in vars[-length(vars)]) {
  dat[dat[,var] == 0, var] <- col.means[var]
}

100*colSums(dat == 0) / nrow(dat)

par(mfrow = c(3, 3))
for (var in vars[-length(vars)]) {
  boxplot(dat[,var]~dat$Outcome, ylab=var, xlab='outcome (diabetic?)')
}
par(mfrow = c(1, 1))

par(mfrow = c(3, 3))
for (var in vars) {
  hist(dat[,var], xlab=var, main='', probability=TRUE)
}
par(mfrow = c(1, 1))

dat$Pregnancies = log(dat$Pregnancies)
dat$Insulin = log(dat$Insulin)
dat$Age = log(dat$Age)
dat$DiabetesPedigreeFunction = log(dat$DiabetesPedigreeFunction)

#dat <- dat[c('log.Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'log.Insulin', 'BMI', 'log.DiabetesPedigreeFunction', 'log.Age', 'Outcome')]
#vars <- colnames(dat)


library(rjags)
mod1_string = " model {
    for (i in 1:length(Outcome)) {
        Outcome[i] ~ dbern(p[i])
        logit(p[i]) = int + b[1]*Pregnancies[i] + b[2]*Glucose[i] + b[3]*BloodPressure[i] + b[4]*SkinThickness[i] + b[5]*Insulin[i] + b[6]*BMI[i]
                          + b[7]*DiabetesPedigreeFunction[i] + b[8]*Age[i]
    }
    int ~ dnorm(0.0, 1.0/25.0)
    for (j in 1:8) {
        b[j] ~ ddexp(0.0, sqrt(2.0)) # has variance 1.0
    }
} "

set.seed(92)

data_jags = as.list(dat)

params = c("int", "b")

mod1 = jags.model(textConnection(mod1_string), data=data_jags, n.chains=3)
update(mod1, 1e3)

mod1_sim = coda.samples(model=mod1,
                        variable.names=params,
                        n.iter=5e3)
mod1_csim = as.mcmc(do.call(rbind, mod1_sim))

par(mfrow=c(4,2))
densplot(mod1_csim[,1:8]) #, xlim=c(-3.0, 3.0))
par(mfrow=c(1,1))

## convergence diagnostics
plot(mod1_sim, ask=TRUE)
summary(mod1_sim)

gelman.diag(mod1_sim)
autocorr.diag(mod1_sim)
autocorr.plot(mod1_sim)
effectiveSize(mod1_sim)

## calculate DIC
dic1 = dic.samples(mod1, n.iter=1e3)


mod2_string = " model {
    for (i in 1:length(Outcome)) {
        Outcome[i] ~ dbern(p[i])
        logit(p[i]) = int + b[1]*Pregnancies[i] + b[2]*Glucose[i] + b[3]*BloodPressure[i] + b[4]*BMI[i]
                          + b[5]*DiabetesPedigreeFunction[i] + b[6]*Age[i]
    }
    int ~ dnorm(0.0, 1.0/25.0)
    for (j in 1:6) {
        b[j] ~ dnorm(0.0, 1/25.0)
    }
} "

mod2 = jags.model(textConnection(mod2_string), data=data_jags, n.chains=3)
update(mod2, 1e3)

mod2_sim = coda.samples(model=mod2,
                        variable.names=params,
                        n.iter=5e3)
mod2_csim = as.mcmc(do.call(rbind, mod2_sim))

plot(mod2_sim, ask=TRUE)
summary(mod2_sim)

gelman.diag(mod2_sim)
autocorr.diag(mod2_sim)
autocorr.plot(mod2_sim)
effectiveSize(mod2_sim)

dic2 = dic.samples(mod2, n.iter=1e3)


(pm_coef = colMeans(mod2_csim))
pm_Xb = pm_coef["int"] + as.matrix(dat[,c(1,2,3,6,7,8)]) %*% pm_coef[1:6]
phat = 1.0 / (1.0 + exp(-pm_Xb))
head(phat)
plot(phat, jitter(dat$Outcome))

(tab0.5 = table(phat > 0.5, data_jags$Outcome))
sum(diag(tab0.5)) / sum(tab0.5)

X = scale(dat[,-length(vars)], center=TRUE, scale=TRUE)
colMeans(X)
apply(X, 2, sd)
X <- as.data.frame(X)
X$Outcome <- dat$Outcome

mod3_string = " model {
    for (i in 1:length(Outcome)) {
        Outcome[i] ~ dbern(p[i])
        logit(p[i]) = int + b[1]*Pregnancies[i] + b[2]*Glucose[i] + b[3]*BloodPressure[i] + b[4]*SkinThickness[i] + b[5]*Insulin[i] + b[6]*BMI[i]
                          + b[7]*DiabetesPedigreeFunction[i] + b[8]*Age[i]
    }
    int ~ dnorm(0.0, 1.0/25.0)
    for (j in 1:8) {
        b[j] ~ dnorm(0.0, 1/25.0)
    }
} "

mod3 = jags.model(textConnection(mod3_string), data=as.list(X), n.chains=3)
update(mod3, 1e3)

mod3_sim = coda.samples(model=mod3,
                        variable.names=params,
                        n.iter=5e3)
mod3_csim = as.mcmc(do.call(rbind, mod3_sim))

plot(mod3_sim, ask=TRUE)
summary(mod3_sim)

gelman.diag(mod3_sim)
autocorr.diag(mod3_sim)
autocorr.plot(mod3_sim)
effectiveSize(mod3_sim)

dic3 = dic.samples(mod3, n.iter=1e3)


(pm_coef = colMeans(mod3_csim))
pm_Xb = pm_coef["int"] + as.matrix(X[,1:8]) %*% pm_coef[1:8]
phat = 1.0 / (1.0 + exp(-pm_Xb))
head(phat)
plot(phat, jitter(dat$Outcome))

(tab0.5 = table(phat > 0.5, data_jags$Outcome))
sum(diag(tab0.5)) / sum(tab0.5)
