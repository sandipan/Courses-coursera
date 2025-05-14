#1
data(mtcars)
mtcars$cyl <- as.factor(mtcars$cyl)
m <- lm(mpg ~ wt+cyl, data = mtcars)
summary(m)
#cyl4: mpg = 33.9908 - 3.2056*wt
#cyl8: mpg = 33.9908 - 6.0709 *cyl8 - 3.2056*wt

#2
summary(lm(mpg ~ wt+cyl, data = mtcars))
summary(lm(mpg ~ cyl, data = mtcars))
#cyl8: mpg = 26.6636 - 11.5636*cyl8
#cyl8: mpg = 33.9908 - 6.0709 *cyl8 - 3.2056*wt
#cyl4: mpg = 26.6636
#cyl4: mpg = 33.9908 - 3.2056*wt

summary(lm(mpg ~ wt+cyl-1, data = mtcars))
summary(lm(mpg ~ cyl-1, data = mtcars))

#3
mwo <- lm(mpg ~ wt+cyl, data = mtcars)  # null model, has no interaction effect
mw <- lm(mpg ~ wt+cyl+wt*cyl, data = mtcars)
summary(mwo)
summary(mw)
anova(mwo, mw)
#library("epicalc")
library(lmtest)
lrtest(mw, mwo) # reject the null model mw in favour of the alternative modelreject the null model in favour of the alternative model mwo

mwo <- lm(mpg ~ wt+cyl, data = mtcars)
mw <- update(mpg ~ wt+cyl+wt*cyl, data = mtcars)
anova(mwo, mw)

#4.
lm(mpg ~ I(wt * 0.5) + factor(cyl), data = mtcars)
#lm(mpg ~ wt + factor(cyl), data = mtcars)
#cyl4: mpg = 33.991 - 6.411*I(wt*0.5) 
#cyl6: mpg = 33.991 - 6.411*I(wt*0.5) - 4.256
#cyl8: mpg = 33.991 - 6.411*I(wt*0.5) - 6.071

#5.
x <- c(0.586, 0.166, -0.042, -0.614, 11.72)
y <- c(0.549, -0.026, -0.127, -0.751, 1.344)
fit <- lm(y~x)
hatvalues(fit)
dfbetas(fit)
cooks.distance(fit)
influence.measures(fit)
library(bstats)
influential.plot(fit, type='potential')
library(car)
influencePlot(fit)
leveragePlots(fit)
av.Plots(fit)
# Cook's D plot
# identify D values > 4/(n-k-1) 
cutoff <- 4/((nrow(mtcars)-length(fit$coefficients)-2)) 
plot(fit, which=4, cook.levels=cutoff)
# Influence Plot 
influencePlot(fit,   id.method="identify", main="Influence Plot", sub="Circle size is proportial to Cook's Distance" )

#6.
hatvalues(fit)
dfbetas(fit)