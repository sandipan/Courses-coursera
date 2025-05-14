library(glmnet)
setwd('C:\\courses\\Coursera\\Current\\ML for Data Analysis\\Week3\\')

df <- read.csv('gapminder.csv')
df <- df[-1]
df <- df[!is.na(df$lifeexpectancy),]

index <- which(names(df) == 'lifeexpectancy')
n <- ncol(df)

impute.with.med <- function(x){
  #x<-as.numeric(as.character(x)) #first convert each column into numeric if it is from factor
  x[is.na(x)] <- median(x, na.rm=TRUE) #convert the item with NA to median value from the column
  x #display the column
}
df <- sapply(df, impute.with.med)

X <- as.matrix(df[,-index][,1:(n-1)])
Y <- df[,index]

model <- cv.glmnet(X, Y, alpha=1) # lasso
plot(model$glmnet.fit, "norm", label=TRUE)
plot(model$glmnet.fit, "lambda", label=TRUE)
plot(model)
grid()
#coef(model)
coef(model, s="lambda.min")
#coef(model, s="lambda.1se")

par(mfrow=c(1,3))
ans1 <- cv.glmnet(X, Y, alpha=0) # ridge
plot(ans1$glmnet.fit, "lambda", label=FALSE)
text (6, 0.4, "A", cex=1.8, font=1)

ans2 <- cv.glmnet(X, Y, alpha=1) # lasso
plot(ans2$glmnet.fit, "norm", label=TRUE)
plot(ans2$glmnet.fit, "lambda", label=TRUE)
text (-0.8, 0.48, "B", cex=1.8, font=1)
plot(ans2)
grid()
coef(ans2)

ans3 <- cv.glmnet(X, Y, alpha=0.5) # elastic net 
plot(ans3$glmnet.fit, "lambda", label=FALSE)
text (0, 0.62, "C", cex=1.8, font=1)