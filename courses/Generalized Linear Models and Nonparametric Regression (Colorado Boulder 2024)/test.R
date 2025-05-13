# py -m jupyter notebook
plot(train_sim$y, predict(lm_sim), 
     xlab='actual', ylab='fitted', pch=19, main='Actual vs. Fitted (LM)', 
     cex.axis=1.9, cex.lab=1.9, cex.main=2)

2*pnorm(1.4224/1.1541, lower.tail = FALSE)

c(1.4224 - qnorm(0.975)*1.1541, 1.4224 + qnorm(0.975)*1.1541)

c(-1.2467 - qnorm(0.975)*0.6347, -1.2467 + qnorm(0.975)*0.6347)

exp(  0.0702)
exp(-5.2471+1.0839)
exp(-5.2471+0.3698+0.0702*100)

glm.compare.p.value <- function(model1, model2) {
  dev.res <- residuals(x, type = "deviance")
  #disp.est <- sum(dev.res^2)  #this is chi-sq w/ df from the model
  lr <- glm_ships$null.deviance - glm_ships$deviance
  df <- glm_ships$df.null - glm_ships$df.residual
  lr
  df
  1 - pchisq(lr, df)
  df <- df.residual(x)  #use built-in function
  print(df)
  list(dispersion = disp.est/df, p = 1 - pchisq(disp.est, df))
}
#glm.disp(glm_ships)
# Test chi_sq stat

#summary(glm_ships_null)
#c(sum((residuals(glm_ships, type = "deviance"))^2), df=df.residual(glm_ships))
#1 - pchisq(sum((residuals(glm_ships, type = "deviance"))^2), df=df.residual(glm_ships))

# poisson regression
# exp(predict(glm_ships_new, test)) == predict(glm_ships_new, test, type='response')

install.packages('ggfortify')
library(ggfortify)

#As can be seen, from the next code snippet, although the new reduced model performs slightly better on the test set, we can't reject the null hypothesis (at 5% level of significance, since p-value = 0.09) that the new hypothesis performs similary in favor of the alternative hypothesis, and conclude that (we don't have enough evidence to support that the new reduced model performs better) both models are similar in terms of performance. Hence we can choose either of the models.

#We choose the new reduced model, since its performance on the held-out test dtaaset is slightly better.
autoplot(glm_ships_new)


x <- train_marketing$youtube
y <- train_marketing$sales
testx <- test_marketing$youtube
testy <- test_marketing$sales
x
res <- ksmooth(x, y, kernel = 'normal', bandwidth = 15, x.points = testx)
res
plot(c(x, testx), c(y, testy))
lines(res$x, res$y, col='red')
length(x)
length(testx)
length(res$x)


library(ggplot2)
library(repr)
#library(reshape2)
options(repr.plot.width=15, repr.plot.height=12)

x <- train_marketing$youtube
y <- train_marketing$sales
testx <- test_marketing$youtube
testy <- test_marketing$sales

c(length(x), length(testx))

sort.data <- function(x, y) {    # sort the predictor $x$ apriori since most of the models expect ot this way during prediction
  res <- sort(x, index.return=TRUE)  # sort x and rerrange y accordingly
  testx <- res$x
  y <- y[res$ix]    
  return (list(x = x, y = y))
}

xy <- sort.data(x, y)
x <- xy$x
y <- xy$y
xy <- sort.data(testx, testy)
testx <- xy$x
testy <- xy$y   

kernel.regression <- function(x, y, testx, testy, kernel, bws) {
  plot.df <- NULL
  test.df <- NULL
  for (bw in bws) {
    res <- ksmooth(x, y, kernel = kernel, bandwidth = bw)
    train_rmse <- sqrt(sum((res$y - y)^2))
    plot.df <- rbind(plot.df, data.frame(x=res$x, fitted.y=res$y, bw=bw))
    res <- ksmooth(x, y, kernel = kernel, bandwidth = bw, n.points=len(testx), x.points = testx)
    test_rmse <- sqrt(sum((res$y - testy)^2))
    test.df <- rbind(test.df, data.frame(bw=bw, train_rmse=train_rmse, test_rmse=test_rmse))
  }
  plot.df$bw = as.factor(as.character(plot.df$bw))
  p <- ggplot(plot.df, aes(x, fitted.y)) + 
    geom_line(aes(col=bw), lwd=1.2) + geom_point(size=0.9) + 
    theme_bw() +
    theme(text=element_text(size=30)) + 
    ggtitle('Kernel Regression with Gaussian kernel & diff bandwidths')
  print(p)
  #print(p, vp=grid::viewport(width=unit(5, 'inch'), height=unit(8, 'inch')))
  return (test.df)
}

test.df <- kernel.regression(x, y, testx, testy, kernel = 'normal', bws = seq(10,90,10)) #seq(0.05,1,0.05))
ggplot(test.df, aes(bw, test_rmse)) + geom_line() + geom_point() + 
  theme_bw() + theme(text=element_text(size=30)) + 
  ggtitle('test RMSE for Kernel Regression with Gaussian kernel')
#test.df <- melt(test.df, id.vars=c('bw'), variable='split', value.name='rmse')
#ggplot(test.df, aes(bw, rmse, col=split)) + geom_line() + geom_point() + theme_bw() + theme(text=element_text(size=30))