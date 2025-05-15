library(Biobase)
library(SpikeInSubset)
library(genefilter)
library(geneplotter)
data(rma95)

tt = rowttests(rma95[-siIndex,],as.factor(pData(rma95)[,1]))
ses = tt$dm/tt$statistic ##hack to get the SEs, se=effect / (effect/se)

bitmap("figure-01.png",res=300,pointsize=20,width=12)
mypar(1,2)
plot(ses,tt$dm,xlab="Standard error estimate",ylab="M",cex=.25)
plot(ses,tt$stat,xlab="Standard error estimate",ylab="t-statistic",cex=.25)
dev.off()

bitmap("figure-02.png",res=300,pointsize=20)
mypar(1,1)
hist(tt$p.value,col=2)
dev.off()

bitmap("figure-03.png",res=300,pointsize=20)
mypar(1,1)
qqplot(qt(seq(1,length(tt$stat))/(length(tt$stat)+1),tt$df),tt$stat,xlab="Theoretical quantiles",ylab="Observed quantiles")
abline(0,1)
dev.off()


