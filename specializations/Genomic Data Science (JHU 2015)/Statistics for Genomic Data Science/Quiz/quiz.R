setwd("C:/courses/Coursera/Current/Statistics for Genomic Data Science/Quiz")

# Quiz 1

#Q3
library(Biobase)
library(GenomicRanges)
data(sample.ExpressionSet, package = "Biobase")
se = makeSummarizedExperimentFromExpressionSet(sample.ExpressionSet)
?SummarizedExperiment

#Q5
con =url("http://bowtie-bio.sourceforge.net/recount/ExpressionSets/bottomly_eset.RData")
load(file=con)
close(con)
bot = bottomly.eset
pdata_bot=pData(bot)

#library(plotrix)
#pie3D(pdata_bot$num.tech.reps,labels=pdata_bm$tissue.type)

con =url("http://bowtie-bio.sourceforge.net/recount/ExpressionSets/bodymap_eset.RData")
load(file=con)
close(con)
bm = bodymap.eset
pdata_bm=pData(bm)

#Q6
con =url("http://bowtie-bio.sourceforge.net/recount/ExpressionSets/bodymap_eset.RData")
load(file=con)
close(con)
bm = bodymap.eset
pdata_bm=pData(bm)

library(plotrix)
pie3D(pdata_bm$num.tech.reps,labels=pdata_bm$tissue.type)

#Q7
con =url("http://bowtie-bio.sourceforge.net/recount/ExpressionSets/bodymap_eset.RData")
load(file=con)
close(con)
bm = bodymap.eset
edata = exprs(bm)

row_sums = rowSums(edata)
index = which(rank(-row_sums) < 500 )
heatmap(edata[index,],Rowv=NA,Colv=NA)

#Q8
con =url("http://bowtie-bio.sourceforge.net/recount/ExpressionSets/bodymap_eset.RData")
load(file=con)
close(con)
bm = bodymap.eset
pdata = pData(bm)
edata = exprs(bm)

library(limma)
#mm=log2(edata[,1]+1)-log2(edata[,2]+1)
#aa=log2(edata[,1]+1)+log2(edata[,2]+1)
#plot(aa,mm)
#MA <- new("MAList")
#MA$M <- edata[,1] 
#MA$A <- log2(pdata[,2] +1)
#plotMA(DESeqDataSetFromMatrix(edata[,1:2], pdata[1:2,],design=~ tissue.type))
#source("https://bioconductor.org/biocLite.R")
#biocLite("DESeq2")
dds <- DESeqDataSetFromMatrix(edata[,1:2], pdata[1:2,], design=~)
#plot(log2( 1+counts(dds, normalized=TRUE)[, 1:2] ), col="#00000020", pch=20, cex=0.3 )
library(DESeq2)
plot(assay(rlog(dds)))


#Q9
con =url("http://bowtie-bio.sourceforge.net/recount/ExpressionSets/montpick_eset.RData")
load(file=con)
close(con)
mp = montpick.eset
pdata=pData(mp)
edata=as.data.frame(exprs(mp))
fdata = fData(mp)
library(rafalib)
myplclust(hclust(dist(t(edata))))
myplclust(hclust(dist(t(edata[rowMeans(edata) < 100,]))))
myplclust(hclust(dist(t(log2 (edata+1)))))


#Q10
con =url("http://bowtie-bio.sourceforge.net/recount/ExpressionSets/montpick_eset.RData")
load(file=con)
close(con)
mp = montpick.eset
pdata=pData(mp)
edata=as.data.frame(exprs(mp))
fdata = fData(mp)
set.seed(1235)
cl1 <- kmeans(t(edata), 2)
cl2 <- kmeans(t(log2(edata+1)), 2)
cl1$clus
cl2$clus
table(pdata$num.tech.reps)
sum(cl1$clus == pdata$num.tech.reps)
hc <- hclust(dist(t(edata)))
cl3 <- cutree(hc, k = 2)
sum(cl3 == pdata$num.tech.reps)


#####
MA Plot
####
library(limma)
MA <- new("MAList")
MA$A <- runif(300,4,16)
MA$M <- rt(300,df=3)
status <- rep("Gene",300)
status[1:3] <- "M=0"
MA$M[1:3] <- 0
status[4:6] <- "M=3"
MA$M[4:6] <- 3
status[7:9] <- "M=-3"
MA$M[7:9] <- -3
plotMA(MA,main="MA-Plot with Simulated Data",status=status,values=c("M=0","M=3","M=-3"),col=c("blue","red","green"))


# Quiz 2

# Q1
con =url("http://bowtie-bio.sourceforge.net/recount/ExpressionSets/montpick_eset.RData")
load(file=con)
close(con)
mp = montpick.eset
pdata=pData(mp)
edata=as.data.frame(exprs(mp))
fdata = fData(mp)

#Do no transformations?
svd1 = svd(edata)
(svd1$d^2)[1]/sum(svd1$d^2)

#log2(data + 1) transform?
svd1 = svd(log2(edata + 1))
(svd1$d^2)[1]/sum(svd1$d^2)

#log2(data + 1) transform and subtract row means?
edata_centered = log2(edata + 1) - rowMeans(log2(edata + 1))
svd1 = svd(edata_centered)
#names(svd1)
(svd1$d^2)[1]/sum(svd1$d^2)

plot(svd1$d,ylab="Singular value",col=2)
plot(svd1$d^2/sum(svd1$d^2),ylab="Percent Variance Explained",col=2)
par(mfrow=c(1,2))
plot(svd1$v[,1],col=2,ylab="1st PC")
plot(svd1$v[,2],col=2,ylab="2nd PC")

#Q2
con =url("http://bowtie-bio.sourceforge.net/recount/ExpressionSets/montpick_eset.RData")
load(file=con)
close(con)
mp = montpick.eset
pdata=pData(mp)
edata=as.data.frame(exprs(mp))
fdata = fData(mp)

log_edata <- log2(edata + 1)
edata_centered = log_edata  - rowMeans(log_edata)
set.seed(333)
cl <- kmeans(t(edata_centered), 2)
svd1 <- svd(edata_centered)
cor(svd1$v[,1], cl$cluster)

# Q3
con =url("http://bowtie-bio.sourceforge.net/recount/ExpressionSets/bodymap_eset.RData")
load(file=con)
close(con)
bm = bodymap.eset
edata = exprs(bm)
pdata_bm=pData(bm)
counts <- edata[1,]
m <- lm(counts ~ as.factor(pdata_bm$num.tech.reps))
plot(counts ~ as.factor(pdata_bm$num.tech.reps))
hist(pdata_bm$num.tech.reps)

# Q4
con =url("http://bowtie-bio.sourceforge.net/recount/ExpressionSets/bodymap_eset.RData")
load(file=con)
close(con)
bm = bodymap.eset
edata = exprs(bm)
pdata_bm=pData(bm)
counts <- edata[1,]
m <- lm(counts ~ pdata_bm$age + pdata_bm$gender)
summary(m)

# Q5
con =url("http://bowtie-bio.sourceforge.net/recount/ExpressionSets/montpick_eset.RData")
load(file=con)
close(con)
mp = montpick.eset
pdata=pData(mp)
edata=as.data.frame(exprs(mp))
fdata = fData(mp)
#data <- cbind.data.frame(t(edata), pdata$population)
m <- lm.fit(model.matrix(~pdata$population), t(edata))
summary(m)
dim(m$coefficients)
dim(m$residuals)
dim(m$effects)
m$effects[,1]

# Q6
con =url("http://bowtie-bio.sourceforge.net/recount/ExpressionSets/montpick_eset.RData")
load(file=con)
close(con)
mp = montpick.eset
pdata=pData(mp)
edata=as.data.frame(exprs(mp))
fdata = fData(mp)
log_edata <- log2(edata + 1)
m <- lm.fit(model.matrix(~pdata$population), t(log_edata))
summary(m)
m$coefficients[,1]
dim(m$effects)
m$effects[,1]

# Q7
con =url("http://bowtie-bio.sourceforge.net/recount/ExpressionSets/bodymap_eset.RData")
load(file=con)
close(con)
bm = bodymap.eset
edata = exprs(bm)
pdata_bm = pData(bm)
edata <- edata[,-which(is.na(pdata_bm$age))]
pdata <- pdata_bm[!is.na(pdata_bm$age),]
fit <- lm.fit(model.matrix(~pdata$age), t(edata))
library(limma)
fit_limma <- lmFit(edata, model.matrix(~pdata$age))
fit$coefficients[,1000]
fit_limma$coefficients[1000,]
par(mfrow=c(4,4))
for (i in 1:16) {
  plot(fit$residuals[i,],col=2)
}
par(mfrow=c(4,4))
for (i in 1:16) {
  plot(fit$fitted.values[i,],col=2)
  abline(h=pdata$age[i],col=3)
}

# Q8
con =url("http://bowtie-bio.sourceforge.net/recount/ExpressionSets/bodymap_eset.RData")
load(file=con)
close(con)
bm = bodymap.eset
edata = exprs(bm)
pdata_bm=pData(bm)
edata <- edata[,-which(is.na(pdata_bm$age))]
pdata <- pdata_bm[!is.na(pdata$age),]
fit_limma <- lmFit(edata, model.matrix(~pdata$age + as.factor(pdata$tissue.type)))
#hist(edata[,16], breaks=2) #white_blood_cell
par(mfrow=c(4,4))
for (i in 1:16) {
  plot(fit_limma$residuals[i,],col=2)
}

# Q10
con =url("http://bowtie-bio.sourceforge.net/recount/ExpressionSets/bodymap_eset.RData")
load(file=con)
close(con)
bm = bodymap.eset
edata = exprs(bm)
pdata_bm=pData(bm)
set.seed(33353)

# subset the expression data to the samples without missing values of age first
idx<-which(is.na(pdata_bm$age))
edata<-edata[,-idx]
p<-pdata_bm[-idx,]

#  log2(data + 1) transforming the expression data, removing rows with rowMeans less than 1
dat<-log2(edata+1)
dat<-dat[which(rowMeans(dat)>=1),] # I tried this before the log2 operation and it messed up with the sva function

library(sva)
# SVA
mod = model.matrix(~ age,data=p)
mod0 = model.matrix(~ 1 ,data=p)
surrogate<-sva(dat,mod,mod0,n.sv=1)

# Results
round(cor(surrogate$sv,pdata_bm$age[-idx]),2)
round(cor(surrogate$sv,as.numeric(as.factor(pdata_bm$gender[-idx]))),2)
round(cor(surrogate$sv,as.numeric(as.factor(pdata_bm$race[-idx]))),2)


# Quiz 3
#source("https://bioconductor.org/biocLite.R")
#biocLite("snpStats")
#biocLite("broom")
library(snpStats)
library(broom)
data(for.exercise)
use <- seq(1, ncol(snps.10), 10)
sub.10 <- snps.10[,use]
snpdata = sub.10@.Data
status = subject.support$cc
dim(snpdata)
?snps.10
snpdata[,3]
length(status)
data <- as.integer(snpdata[,3])
data[data == 0] <- NA
m1 <- lm(status ~ data)
m2 <- glm(status ~ data, family=binomial)
data <- as.integer(snpdata[,10])
#data[data == 0] <- NA
m1 <- lm(status ~ data)
m2 <- glm(status ~ data, family=binomial)
table(predict(m1), status)
table(predict(m2, type='response'), status)

m2 <- glm(status ~ data, family=binomial)
table(predict(m1), status)
table(predict(m2, type='response'), status)

#m <- sapply(as.matrix(snpdata), function(x) glm(status ~ as.integer(x), family=binomial))
coeffs <- NULL
for (i in 1:(ncol(snpdata))) {
  data <- as.integer(snpdata[,i])
  data[data == 0] <- NA
  coeffs <- rbind(coeffs, zstat=summary(glm(status ~ data, family=binomial))$coefficients[2,3])
}
apply(coeffs, 2, mean)
apply(coeffs, 2, min)
apply(coeffs, 2, max)
cor(coeffs^2)
chi.squared(coeffs^2)

library(Biobase)
con =url("http://bowtie-bio.sourceforge.net/recount/ExpressionSets/montpick_eset.RData")
load(file=con)
close(con)
mp = montpick.eset
pdata=pData(mp)
edata=as.data.frame(exprs(mp))
fdata = fData(mp)
#showMethods(rowttests)
library(genefilter)
rowFtests(as.matrix(log2(edata[1,]+1)), pdata$population)
rowttests(as.matrix(log2(edata[1,]+1)), pdata$population)

con =url("http://bowtie-bio.sourceforge.net/recount/ExpressionSets/montpick_eset.RData")
load(file=con)
close(con)
mp = montpick.eset
pdata=pData(mp)
edata=as.data.frame(exprs(mp))
edata = edata[rowMeans(edata) > 100,]
fdata = fData(mp)

#source("https://bioconductor.org/biocLite.R")
#biocLite("DESeq2")
library(DESeq2)
de = DESeqDataSetFromMatrix(edata, pdata, ~ study)
glm_all_nb = DESeq(de)
result_nb = results(glm_all_nb)

library(limma)
edata2 = log2(as.matrix(edata) + 1)
mod = model.matrix(~ pdata$study)
fit_limma = lmFit(edata2,mod)
ebayes_limma = eBayes(fit_limma)
top_lane = topTable(ebayes_limma, coef=2,number=dim(edata)[1],sort.by="none")
str(top_lane)
cor(result_nb$stat, top_lane$t, use="complete.obs")
#summary(result_nb$stat)
#summary(top_lane$t)

A <- result_nb$stat
M <- top_lane$t
mat <- cbind(A,M)           
limma::plotMA(mat,main="MA plot")                   
abline(h=-7,col="red")

sum(result_nb$padj < 0.05, na.rm=TRUE)
sum(top_lane$adj.P.Val < 0.05, na.rm=TRUE)

1995/nrow(top_lane)


# Quiz 4
#source("https://bioconductor.org/biocLite.R")
#biocLite("goseq")
library(goseq) 
df <- supportedGenomes()
df1 <- df[df$species == 'Mouse' & df$name == 'NCBI Build 37',]

library(Biobase)
library(limma)
con =url("http://bowtie-bio.sourceforge.net/recount/ExpressionSets/bottomly_eset.RData")
load(file=con)
close(con)
bot = bottomly.eset
pdata_bot=pData(bot)
fdata_bot = featureData(bot)
edata = exprs(bot)
fdata_bot = fdata_bot[rowMeans(edata) > 5]
edata = edata[rowMeans(edata) > 5, ]

library(DESeq2)
head(pdata_bot)
de = DESeqDataSetFromMatrix(edata, pdata_bot, ~strain)
de_fit = DESeq(de)
de_results = results(de_fit)
sum(de_results$padj < 0.05)
library(limma)
edata2 = log2(as.matrix(edata) + 1)
mod = model.matrix(~ pdata_bot$strain)
fit_limma = lmFit(edata2,mod)
ebayes_limma = eBayes(fit_limma)
top_lane = topTable(ebayes_limma, coef=2,number=dim(edata)[1],sort.by="none")
str(top_lane)
sum(top_lane$adj.P.Val < 0.05)
head(top_lane[top_lane$adj.P.Val < 0.05,])

genes = as.integer(top_lane$adj.P.Val < 0.05)
names(genes)=rownames(edata2)
pwf = nullp(genes,"mm9","ensGene") #df1$AvailableGeneIDs)
#head(pwf[pwf$DEgenes == 1,])
#biocLite("org.Mm.eg.db")
GO.wall=goseq(pwf,"mm9","ensGene")
head(GO.wall)

library(Biobase)
library(limma)
con =url("http://bowtie-bio.sourceforge.net/recount/ExpressionSets/bottomly_eset.RData")
load(file=con)
close(con)
bot = bottomly.eset
pdata_bot=pData(bot)
fdata_bot = featureData(bot)
edata = exprs(bot)
fdata_bot = fdata_bot[rowMeans(edata) > 5]
edata = edata[rowMeans(edata) > 5, ]
library(goseq)
edata2 = log2(as.matrix(edata) + 1) #edata2 <- edata
mod = model.matrix(~ pdata_bot$strain)
fit_limma = lmFit(edata2,mod)
ebayes_limma = eBayes(fit_limma)
top_lane = topTable(ebayes_limma, coef=2,number=dim(edata)[1],sort.by="none")
str(top_lane)
#sum(top_lane$adj.P.Val < 0.05)
#head(top_lane[top_lane$adj.P.Val < 0.05,], 10)
genes = as.integer(top_lane$adj.P.Val < 0.05)
names(genes)=rownames(edata2)
pwf = nullp(genes,"mm9","ensGene") #df1$AvailableGeneIDs)
#head(pwf[pwf$DEgenes == 1,])
#biocLite("org.Mm.eg.db")
GO.wall=goseq(pwf,"mm9","ensGene")
cat1 <- head(GO.wall, 10)$category
#GO.MF=goseq(pwf,"mm9","ensGene",test.cats=c("GO:MF"))
#head(GO.MF,10)
genes = as.integer(top_lane$P.Value < 0.05)
names(genes)=rownames(edata2)
pwf = nullp(genes,"mm9","ensGene") #df1$AvailableGeneIDs)
GO.wall=goseq(pwf,"mm9","ensGene")
cat2 <- head(GO.wall, 10)$category
intersect(cat1, cat2)

# POW
library(rgl)
m <- 1:200
n <- 1:200
q <- 33^m - 7^n
q <- ifelse(q > 0, log(q), 0)
plot3d(m, n, q, col=q, size=2, type='s')
# POW