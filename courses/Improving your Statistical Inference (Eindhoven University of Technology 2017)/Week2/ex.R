# Calculate Likelihood Ratio

#Calculate the likelihood ratio----
n<-100 #set total trials
x<-64 #set successes
H0 <- .5 #specify one hypothesis you want to compare with the likihood ratio
H1 <- 64/100 #specify another hypothesis you want to compare with the likihood ratio (you can use 1/20, or 0.05)
dbinom(x,n,H0)/dbinom(x,n,H1) #Returns the likelihood ratio of H0 over H1
dbinom(x,n,H1)/dbinom(x,n,H0) #Returns the likelihood ratio of H1 over H0

n<-280 #set total trials
x<-143 #set successes
H0 <- .5 #specify one hypothesis you want to compare with the likihood ratio
H1 <- .52 #specify another hypothesis you want to compare with the likihood ratio (you can use 1/20, or 0.05)
dbinom(x,n,H0)/dbinom(x,n,H1) #Returns the likelihood ratio of H0 over H1
dbinom(x,n,H1)/dbinom(x,n,H0) #Returns the likelihood ratio of H1 over H0

theta<- seq(0,1,len=100) #create theta variable, from 0 to 1
like <- dbinom(x,n,theta)
#png(file="LikRatio.png",width=4000,height=3000, , units = "px", res = 900)
plot(theta,like,type='l',xlab=expression(theta), ylab='Likelihood', lwd=2)
points(H0,dbinom(x,n,H0))
points(H1,dbinom(x,n,H1))
segments(H0, dbinom(x,n,H0), x/n, dbinom(x,n,H0), lty=2, lwd=2)
segments(H1, dbinom(x,n,H1), x/n, dbinom(x,n,H1), lty=2, lwd=2)
segments(x/n, dbinom(x,n,H0), x/n, dbinom(x,n,H1), lwd=2)
title(paste('Likelihood Ratio H0/H1:',round(dbinom(x,n,H0)/dbinom(x,n,H1),digits=2)," Likelihood Ratio H1/H0:",round(dbinom(x,n,H1)/dbinom(x,n,H0),digits=2)))
#dev.off()

# Copyright Daniel Lakens, 2016. 
# This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. https://creativecommons.org/licenses/by-nc-sa/4.0/

library(animation)
p <- ggplot(data.frame(x = c(0, 1)), aes(x)) 
saveGIF({
   for (i in 1:20) {
     p <- p + 
       stat_function(fun = function(x) dbeta(x, shape1=i,shape2=i), colour = i)
     print(p)  
   }
})

# Binomial Bayes Factor
H0<-0.5 #Set the point null hypothesis you want to calculate the Bayes Factor for
n<-50 #20 #set total trials
x<-20 #10 #set successes
aprior<-2 #1 #Set the alpha for the Beta distribution for the prior
bprior<-2 #1 #Set the beta for the Beta distribution for the prior

alikelihood<-x+1 #Calculate the alpha for the Beta distribution for the likelihood
blikelihood<-n-x+1 #Calculate the beta for the Beta distribution for the likelihood
aposterior<-aprior+alikelihood-1 #Calculate the alpha for the Beta distribution for the posterior
bposterior<-bprior+blikelihood-1 #Calculate the beta for the Beta distribution for the posterior

theta<-seq(0,1,0.001) #create theta range from 0 to 1
#png(file="PriorLikelihoodPosterior.png",width=3000,height=3000, res = 500)
prior <- dbeta(theta, aprior, bprior)
likelihood <- dbeta(theta, alikelihood, blikelihood)
posterior <- dbeta(theta, aposterior, bposterior)
plot(theta, posterior, ylim=c(0, 15), type = "l", lwd = 3, xlab = bquote(theta), ylab = "Density", las = 1)
lines(theta, prior, col="grey", lwd = 3)
lines(theta, likelihood, lty = 2, lwd = 3, col="dodgerblue")
BF10<-dbeta(H0, aposterior, bposterior)/dbeta(H0, aprior, bprior)
points(H0,dbeta(H0, aposterior, bposterior), pch = 19)
points(H0,dbeta(H0, aprior, bprior), pch = 19, col="grey")
segments(H0, dbeta(H0, aposterior, bposterior), H0, dbeta(H0, aprior, bprior), lty=2)
title(paste('Bayes Factor:',round(BF10,digits=2)))
#dev.off()

#© Daniel Lakens, 2016. 
# This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. https://creativecommons.org/licenses/by-nc-sa/4.0/

# Binomial Posterior Mean
n<-10 #20 #set total trials
x<-0 #10 #set successes
aprior<-10 #1 #Set the alpha for the Beta distribution for the prior
bprior<-10 #1 #Set the beta for the Beta distribution for the prior

ymax<-10 #set max y-axis

alikelihood<-x+1 #Calculate the alpha for the Beta distribution for the likelihood
blikelihood<-n-x+1 #Calculate the beta for the Beta distribution for the likelihood
aposterior<-aprior+alikelihood-1 #Calculate the alpha for the Beta distribution for the posterior
bposterior<-bprior+blikelihood-1 #Calculate the beta for the Beta distribution for the posterior

theta<-seq(0,1,0.001) #create theta range from 0 to 1
#png(file="BinomialPosteriorMean.png",width=4000,height=4000, res = 500)
prior <- dbeta(theta, aprior, bprior) #deterine prior distribution
likelihood <- dbeta(theta, alikelihood, blikelihood) #determine likelihood distribution
posterior <- dbeta(theta, aposterior, bposterior) #determine posterior distribution
plot(theta, posterior, ylim=c(0, ymax), type = "l", lwd = 3, xlab = bquote(theta), ylab = "Density", las = 1) #draw posterior distribution
lines(theta, prior, col="grey", lwd = 3) #draw prior distribution
lines(theta, likelihood, lty = 2, lwd = 3, col="dodgerblue") #draw likelihood distribution
LL<-qbeta(.025,aposterior, bposterior) #calculate lower limit credible interval
UL<-qbeta(.975,aposterior, bposterior) #calculate upper limit credible interval
abline(v = aposterior/(aposterior+bposterior)) #draw line mean
abline(v = LL, col="grey",lty=3) #draw line lower limit
abline(v = UL, col="grey",lty=3) #draw line upper limit
polygon(c(theta[theta<LL],rev(theta[theta<LL])),c(posterior[theta<LL], rep(0,sum(theta<LL))),col="lightgrey",border=NA)
polygon(c(theta[theta>UL],rev(theta[theta>UL])),c(posterior[theta>UL], rep(0,sum(theta>UL))),col="lightgrey",border=NA)
title(paste('Mean posterior:',round((aposterior/(aposterior+bposterior)),digits=5),", 95% Credible Interval:",round(LL,digits=2),";",round(UL,digits=2)))
#dev.off()

if(!require(binom)){install.packages('binom')}
library(binom)
binom.bayes(x, n, type = "central", prior.shape1 = aprior, prior.shape2 = bprior)
binom.bayes(x, n, type = "highest", prior.shape1 = aprior, prior.shape2 = bprior)

#© Daniel Lakens, 2016. 
# This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. https://creativecommons.org/licenses/by-nc-sa/4.0/