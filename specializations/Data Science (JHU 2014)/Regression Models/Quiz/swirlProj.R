setwd("C:/Users/SANDIPAN DEY/Desktop/coursera/Linear Regression")

> library(swirl)

| Hi! Type swirl() when you are ready to begin.

> swirl()

| Welcome to swirl! Please sign in. If you've been here before, use the same
| name as you did then. If you are new, call yourself something unique.

What shall I call you? Sandipan

| Thanks, Sandipan. Let's cover a couple of quick housekeeping items before we
| begin our first lesson. First off, you should know that when you see '...',
| that means you should press Enter when you are done reading and ready to
| continue.

...  <-- That's your cue to press Enter to continue

| Also, when you see 'ANSWER:', the R prompt (>), or when you are asked to
| select from a list, that means it's your turn to enter a response, then press
| Enter to continue.

Select 1, 2, or 3 and press Enter 

1: Continue.
2: Proceed.
3: Let's get going!

Selection: 1

| You can exit swirl and return to the R prompt (>) at any time by pressing the
| Esc key. If you are already at the prompt, type bye() to exit and save your
| progress. When you exit properly, you'll see a short message letting know
| you've done so.

| When you are at the R prompt (>):
| -- Typing skip() allows you to skip the current question.
| -- Typing play() lets you experiment with R on your own; swirl will ignore
| what you do...
| -- UNTIL you type nxt() which will regain swirl's attention.
| -- Typing bye() causes swirl to exit. Your progress will be saved.
| -- Typing main() returns you to swirl's main menu.
| -- Typing info() displays these options again.

| Let's get started!
  
  ...

| To begin, you must install a course. I can install a course for you from the
| internet, or I can send you to a web page
| (https://github.com/swirldev/swirl_courses) which will provide course options
| and directions for installing courses yourself. (If you are not connected to
                                                   | the internet, type 0 to exit.)

1: R Programming: The basics of programming in R
2: Regression Models: The basics of regression modeling in R
3: Don't install anything for me. I'll do it myself.

Selection: 2

| Course installed successfully!
  
## 1

library(swirl)
swirl()
plot(child ~ parent, galton)
plot(jitter(child,4) ~ parent,galton)
regrline <- lm(child ~ parent, galton)
abline(regrline, lwd=3, col='red')
summary(regrline)


| Please choose a course, or type 0 to exit swirl.

1: Regression Models
2: Take me to the swirl course repository!

Selection: 1

| Please choose a lesson, or type 0 to return to course menu.

 1: Introduction
 2: Residuals
 3: Least Squares Estimation
 4: Residual Variation
 5: Introduction to Multivariable Regression
 6: MultiVar Examples
 7: MultiVar Examples2
 8: MultiVar Examples3
 9: Residuals Diagnostics and Variation
10: Variance Inflation Factors
11: Overfitting and Underfitting
12: Binary Outcomes
13: Count Outcomes

Selection: 1

| Attemping to load lesson dependencies...

| This lesson requires the ‘UsingR’ package. Would you like me to install it
| for you now?

1: Yes
2: No

Selection: 1

| Trying to install package ‘UsingR’ now...
package ‘UsingR’ successfully unpacked and MD5 sums checked

| Package ‘UsingR’ loaded correctly!

| Package ‘MASS’ loaded correctly!


  |                                                                            
  |                                                                      |   0%

| Introduction to Regression Models. (Slides for this and other Data Science
| courses may be found at github
| https://github.com/DataScienceSpecialization/courses if you want to use them.
| They must be downloaded as a zip file and viewed locally. This lesson
| corresponds to Regression_Models/01_01_introduction.)

...


  |                                                                            
  |====                                                                  |   5%
| This is the first lesson on Regression Models. We'll begin with the concept
| of "regression toward the mean" and illustrate it with some pioneering work
| of the father of forensic science, Sir Francis Galton.

...


  |                                                                            
  |=======                                                               |  10%
| Sir Francis studied the relationship between heights of parents and their
| children. His work showed that parents who were taller than average had
| children who were also tall but closer to the average height. Similarly,
| parents who were shorter than average had children who were also shorter than
| average but less so than mom and dad. That is, they were closer to the
| average height. From one generation to the next the heights moved closer to
| the average or regressed toward the mean.

...


  |                                                                            
  |===========                                                           |  15%
| For this lesson we'll use Sir Francis's parent/child height data which we've
| taken the liberty to load for you. We've done this with the R command 'galton
| <- UsingR::galton' when you began the lesson. This is one of many datasets
| that R provides for users. So let's get started!

...


  |                                                                            
  |==============                                                        |  20%
| Here is a plot of Galton's data, a set of 928 parent/child height pairs.
| Moms' and dads' heights were averaged together (after moms' heights were
| adjusted by a factor of 1.08). In our plot we used the R function "jitter" on
| the children's heights to highlight heights that occurred most frequently.
| The dark spots in each column rise from left to right suggesting that
| children's heights do depend on their parents'. Tall parents have tall
| children and short parents have short children.

...


  |                                                                            
  |==================                                                    |  25%
| Here we add a red (45 degree) line of slope 1 and intercept 0 to the plot. If
| children tended to be the same height as their parents, we would expect the
| data to vary evenly about this line. We see this isn't the case. On the left
| half of the plot we see a concentration of heights above the line, and on the
| right half we see the concentration below the line.

...


  |                                                                            
  |=====================                                                 |  30%
| Now we've added a blue regression line to the plot. This is the line which
| has the minimum variation of the data around it. (For theory see the slides.)
| Its slope is greater than zero indicating that parents' heights do affect
| their children's. The slope is also less than 1 as would have been the case
| if children tended to be the same height as their parents.

...


  |                                                                            
  |=========================                                             |  35%
| Now's your chance to plot in R. Type "plot(child ~ parent, galton)" at the R
| prompt.

> plot(child ~ parent, galton)

| You are really on a roll!


  |                                                                            
  |============================                                          |  40%
| You'll notice that this plot looks a lot different than the original we
| displayed. Why? Many people are the same height to within measurement error,
| so points fall on top of one another. You can see that some circles appear
| darker than others. However, by using R's function "jitter" on the children's
| heights, we can spread out the data to simulate the measurement errors and
| make high frequency heights more visible.

...


  |                                                                            
  |================================                                      |  45%
| Now it's your turn to try. Just type "plot(jitter(child,4) ~ parent,galton)"
| and see the magic.

> plot(jitter(child,4) ~ parent,galton)

| Great job!


  |                                                                            
  |===================================                                   |  50%
| Now for the regression line. This is quite easy in R. The function lm (linear
| model) needs a "formula" and dataset. You can type "?formula" for more
| information, but, in simple terms, we just need to specify the dependent
| variable (children's heights) ~ the independent variable (parents' heights).

...


  |                                                                            
  |======================================                                |  55%
| So generate the regression line and store it in the variable regrline. Type
| "regrline <- lm(child ~ parent, galton)"

> regrline <- lm(child ~ parent, galton)

| Nice work!


  |                                                                            
  |==========================================                            |  60%
| Now add the regression line to the plot with "abline". Make the line wide and
| red for visibility. Type "abline(regrline, lwd=3, col='red')"

> abline(regrline, lwd=3, col='red')

| Great job!


  |                                                                            
  |==============================================                        |  65%
| The regression line will have a slope and intercept which are estimated from
| data. Estimates are not exact. Their accuracy is gauged by theoretical
| techniques and expressed in terms of "standard error." You can use
| "summary(regrline)" to examine the Galton regression line. Do this now.

> summary(regrline)

Call:
lm(formula = child ~ parent, data = galton)

Residuals:
    Min      1Q  Median      3Q     Max 
-7.8050 -1.3661  0.0487  1.6339  5.9264 

Coefficients:
            Estimate Std. Error t value Pr(>|t|)    
(Intercept) 23.94153    2.81088   8.517   <2e-16 ***
parent       0.64629    0.04114  15.711   <2e-16 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 2.239 on 926 degrees of freedom
Multiple R-squared:  0.2105,    Adjusted R-squared:  0.2096 
F-statistic: 246.8 on 1 and 926 DF,  p-value: < 2.2e-16


| Excellent job!


  |                                                                            
  |=================================================                     |  70%
| The slope of the line is the estimate of the coefficient, or muliplier, of
| "parent", the independent variable of our data (in this case, the parents'
| heights). From the output of "summary" what is the slope of the regression
| line?

1: 23.94153
2: .04114
3: .64629

Selection: 3

| Nice work!


  |                                                                            
  |====================================================                  |  75%
| What is the standard error of the slope?

1: .04114
2: 23.94153
3: .64629

Selection: 1

| You are quite good my friend!


  |                                                                            
  |========================================================              |  80%
| A coefficient will be within 2 standard errors of its estimate about 95% of
| the time. This means the slope of our regression is significantly different
| than either 0 or 1 since (.64629) +/- (2*.04114) is near neither 0 nor 1.

...


  |                                                                            
  |============================================================          |  85%
| We're now adding two blue lines to indicate the means of the children's
| heights (horizontal) and the parents' (vertical). Note that these lines and
| the regression line all intersect in a point. Pretty cool, huh? We'll talk
| more about this in a later lesson. (Something you can look forward to.)

...


  |                                                                            
  |===============================================================       |  90%
| The slope of a line shows how much of a change in the vertical direction is
| produced by a change in the horizontal direction. So, parents "1 inch" above
| the mean in height tend to have children who are only .65 inches above the
| mean. The green triangle illustrates this point. From the mean, moving a "1
| inch distance" horizontally to the right (increasing the parents' height)
| produces a ".65 inch" increase in the vertical direction (children's height).

...


  |                                                                            
  |==================================================================    |  95%
| Similarly, parents who are 1 inch below average in height have children who
| are only .65 inches below average height. The purple triangle illustrates
| this. From the mean, moving a "1 inch distance" horizontally to the left
| (decreasing the parents' height) produces a ".65 inch" decrease in the
| vertical direction (children's height).

...


  |                                                                            
  |======================================================================| 100%
| This concludes our lesson on regression toward the mean. We hope you found it
| above average!

...

| Are you currently enrolled in the Coursera course associated with this
| lesson?

1: Yes
2: No

Selection: 1

| Would you like me to notify Coursera that you've completed this lesson? If
| so, I'll need to get some more info from you.

1: Yes
2: No
3: Maybe later

Selection: 1

| The first item I need is your Course ID. For example, if the homepage for
| your Coursera course was 'https://class.coursera.org/rprog-001', then your
| course ID would be 'rprog-001' (without the quotes).

Course ID: regmods-002
Submission login (email): sandipan.dey@gmail.com
Submission password: P7N3y8jkyC

| Is the following information correct?

Course ID: regmods-002
Submission login (email): sandipan.dey@gmail.com
Submission password: P7N3y8jkyC

1: Yes, go ahead!
2: No, I need to change something.

Selection: 1

| I'll try to tell Coursera you've completed this lesson now.

| Great work!

| I've notified Coursera that you have completed regmods-002, Introduction.

| You've reached the end of this lesson! Returning to the main menu...

| Please choose a course, or type 0 to exit swirl.

1: Regression Models
2: Take me to the swirl course repository!

Selection: 1

| Please choose a lesson, or type 0 to return to course menu.

 1: Introduction
 2: Residuals
 3: Least Squares Estimation
 4: Residual Variation
 5: Introduction to Multivariable Regression
 6: MultiVar Examples
 7: MultiVar Examples2
 8: MultiVar Examples3
 9: Residuals Diagnostics and Variation
10: Variance Inflation Factors
11: Overfitting and Underfitting
12: Binary Outcomes
13: Count Outcomes

## 2

fit <- lm(child ~ parent, galton)
summary(fit)
mean(fit$residuals)
cov(fit$residuals, galton$parent)
ols.ic <- fit$coef[1]
ols.slope <- fit$coef[2]

#Here are the vectors of variations or tweaks
sltweak <- c(.01, .02, .03, -.01, -.02, -.03) #one for the slope
ictweak <- c(.1, .2, .3, -.1, -.2, -.3)  #one for the intercept
lhs <- numeric()
rhs <- numeric()
#left side of eqn is the sum of squares of residuals of the tweaked regression line
for (n in 1:6) lhs[n] <- sqe(ols.slope+sltweak[n],ols.ic+ictweak[n])
#right side of eqn is the sum of squares of original residuals + sum of squares of two tweaks
for (n in 1:6) rhs[n] <- sqe(ols.slope,ols.ic) + sum(est(sltweak[n],ictweak[n])^2)

lhs - rhs
all.equal(lhs, rhs)
varChild <- var(galton$child)
varRes <- var(fit$residuals)
varEst <- var(est(ols.slope, ols.ic))
all.equal(varChild, varRes + varEst)

efit <- lm(accel ~ mag+dist, attenu)
mean(efit$residuals)
cov(efit$residuals, attenu$mag)
cov(efit$residuals, attenu$dist)


Selection: 2


  |                                                                            
  |                                                                      |   0%

| Residuals. (Slides for this and other Data Science courses may be found at
| github https://github.com/DataScienceSpecialization/courses. If you care to
| use them, they must be downloaded as a zip file and viewed locally. This
| lesson corresponds to Regression_Models/01_02_linearRegression.)

...


  |                                                                            
  |==                                                                    |   3%
| This lesson will focus on the residuals, the distances between the actual
| children's heights and the estimates given by the regression line. Since all
| lines are characterized by two parameters, a slope and an intercept, we'll
| use the least squares criteria to provide two equations in two unknowns so we
| can solve for these parameters, the slope and intercept.

...


  |                                                                            
  |=====                                                                 |   6%
| The first equation says that the "errors" in our estimates, the residuals,
| have mean zero. In other words, the residuals are "balanced" among the data
| points; they're just as likely to be positive as negative. The second
| equation says that our residuals must be uncorrelated with our predictors,
| the parentsâ€™ height. This makes sense - if the residuals and predictors
| were correlated then you could make a better prediction and reduce the
| distances (residuals) between the actual outcomes and the predictions.

...


  |                                                                            
  |=======                                                               |  10%
| We'll demonstrate these concepts now. First regenerate the regression line
| and call it fit. Use the R function lm. Recall that by default its first
| argument is a formula such as "child ~ parent" and its second is the dataset,
| in this case galton.

> fit <- lm(child ~ parent, galton)

| Excellent job!


  |                                                                            
  |=========                                                             |  13%
| Now we'll examine fit to see its slope and intercept. The residuals we're
| interested in are stored in the 928-long vector fit$residuals. If you type
| fit$residuals you'll see a lot of numbers scroll by which isn't very useful;
| however if you type "summary(fit)" you will see a more concise display of the
| regression data. Do this now.

> summary(fit)

Call:
lm(formula = child ~ parent, data = galton)

Residuals:
    Min      1Q  Median      3Q     Max 
-7.8050 -1.3661  0.0487  1.6339  5.9264 

Coefficients:
            Estimate Std. Error t value Pr(>|t|)    
(Intercept) 23.94153    2.81088   8.517   <2e-16 ***
parent       0.64629    0.04114  15.711   <2e-16 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 2.239 on 926 degrees of freedom
Multiple R-squared:  0.2105,    Adjusted R-squared:  0.2096 
F-statistic: 246.8 on 1 and 926 DF,  p-value: < 2.2e-16


| You got it right!


  |                                                                            
  |===========                                                           |  16%
| First check the mean of fit$residuals to see if it's close to 0.

> 
> mean(fit$residuals)
[1] -2.359884e-15

| Excellent job!


  |                                                                            
  |==============                                                        |  19%
| Now check the correlation between the residuals and the predictors. Type
| "cov(fit$residuals, galton$parent)" to see if it's close to 0.

> cov(fit$residuals, galton$parent)
[1] -1.790153e-13

| Great job!


  |                                                                            
  |================                                                      |  23%
| As shown algebraically in the slides, the equations for the intercept and
| slope are found by supposing a change is made to the intercept and slope.
| Squaring out the resulting expressions produces three summations. The first
| sum is the original term squared, before the slope and intercept were
| changed. The third sum totals the squared changes themselves. For instance,
| if we had changed fitâ€™s intercept by adding 2, the third sum would be the
| total of 928 4â€™s. The middle sum is guaranteed to be zero precisely when
| the two equations (the conditions on the residuals) are satisfied.

...


  |                                                                            
  |==================                                                    |  26%
| We'll verify these claims now. We've defined for you two R functions, est and
| sqe. Both take two inputs, a slope and an intercept. The function est
| calculates a child's height (y-coordinate) using the line defined by the two
| parameters, (slope and intercept), and the parents' heights in the Galton
| data as x-coordinates.

...


  |                                                                            
  |====================                                                  |  29%
| Let "mch"" represent the mean of the galton childrens' heights and "mph"" the
| mean of the galton parents' heights. Let "ic" and "slope" represent the
| intercept and slope of the regression line respectively. As shown in the
| slides and past lessons, the point (mph,mch) lies on the regression line.
| This means

1: mch = ic + slope*mph
2: I haven't the slightest idea.
3: mph = ic + slope*mch

Selection: 1

| That's a job well done!


  |                                                                            
  |=======================                                               |  32%
| The function sqe calculates the sum of the squared residuals, the differences
| between the actual children's heights and the estimated heights specified by
| the line defined by the given parameters (slope and intercept).  R provides
| the function deviance to do exactly this using a fitted model (e.g., fit) as
| its argument. However, we provide sqe because we'll use it to test regression
| lines different from fit.

...


  |                                                                            
  |=========================                                             |  35%
| We'll see that when we vary or tweak the slope and intercept values of the
| regression line which are stored in fit$coef, the resulting squared residuals
| are approximately equal to the sum of two sums of squares - that of the
| original regression residuals and that of the tweaks themselves. More
| precisely, up to numerical error,

...


  |                                                                            
  |===========================                                           |  39%
| sqe(ols.slope+sl,ols.intercept+ic) == deviance(fit) + sum(est(sl,ic)Ë†2 )

...


  |                                                                            
  |=============================                                         |  42%
| Equivalently, sqe(ols.slope+sl,ols.intercept+ic) == sqe(ols.slope,
| ols.intercept) + sum(est(sl,ic)Ë†2 )

...


  |                                                                            
  |================================                                      |  45%
| The left side of the equation represents the squared residuals of a new line,
| the "tweaked" regression line. The terms "sl" and "ic" represent the
| variations in the slope and intercept respectively. The right side has two
| terms. The first represents the squared residuals of the original regression
| line and the second is the sum of squares of the variations themselves.

...


  |                                                                            
  |==================================                                    |  48%
| We'll demonstrate this now. First extract the intercept from fit$coef and put
| it in a variable called ols.ic . The intercept is the first element in the
| fit$coef vector, that is fit$coef[1].

> ols.ic <- fit$coef[1]

| You are really on a roll!


  |                                                                            
  |====================================                                  |  52%
| Now extract the slope from fit$coef and put it in the variable ols.slope; the
| slope is the second element in the fit$coef vector, fit$coef[2].

> ols.slope <- fit$coef[2]

| You are really on a roll!


  |                                                                            
  |======================================                                |  55%
| Now we'll show you some R code which generates the left and right sides of
| this equation.  Take a moment to look it over. We've formed two 6-long
| vectors of variations, one for the slope and one for the intercept. Then we
| have two "for" loops to generate the two sides of the equation.

...


  |                                                                            
  |=========================================                             |  58%
| Subtract the right side, the vector rhs, from the left, the vector lhs, to
| see the relationship between them. You should get a vector of very small,
| almost 0, numbers.

> rhs - lhs
[1] -1.264198e-09 -2.527486e-09 -3.801688e-09  1.261469e-09  2.522938e-09
[6]  3.767127e-09

| Almost! Try again. Or, type info() for more options.

| Type "lhs-rhs" at the R prompt.

> lhs - rhs
[1]  1.264198e-09  2.527486e-09  3.801688e-09 -1.261469e-09 -2.522938e-09
[6] -3.767127e-09

| You're the best!


  |                                                                            
  |===========================================                           |  61%
| You could also use the R function all.equal with lhs and rhs as arguments to
| test for equality. Try it now.

> all.equal(lhs, rhs)
[1] TRUE

| Excellent job!


  |                                                                            
  |=============================================                         |  65%
| Now we'll show that the variance in the children's heights is the sum of the
| variance in the OLS estimates and the variance in the OLS residuals. First
| use the R function var to calculate the variance in the children's heights
| and store it in the variable varChild.

> varChild <- var(galton$child)

| Keep up the great work!


  |                                                                            
  |===============================================                       |  68%
| Remember that we've calculated the residuals and they're stored in
| fit$residuals. Use the R function var to calculate the variance in these
| residuals now and store it in the variable varRes.

> varRes <- var(fit$residuals)

| You are really on a roll!


  |                                                                            
  |==================================================                    |  71%
| Recall that the function "est" calculates the estimates (y-coordinates) of
| values along the regression line defined by the variables "ols.slope" and
| "ols.ic". Compute the variance in the estimates and store it in the variable
| varEst.

> varEst <- var(est(ols.slope, ols.ic))

| You got it right!


  |                                                                            
  |====================================================                  |  74%
| Now use the function all.equal to compare varChild and the sum of varRes and
| varEst.

> all.equal(varChild, varRes + varEst)
[1] TRUE

| Nice work!


  |                                                                            
  |======================================================                |  77%
| Since variances are sums of squares (and hence always positive), this
| equation which we've just demonstrated,
| var(data)=var(estimate)+var(residuals), shows that the variance of the
| estimate is ALWAYS less than the variance of the data.

...


  |                                                                            
  |========================================================              |  81%
| Since var(data)=var(estimate)+var(residuals) and variances are always
| positive, the variance of residuals

1: is greater than the variance of data
2: is less than the variance of data
3: is unknown without actual data

Selection: 2

| You're the best!


  |                                                                            
  |===========================================================           |  84%
| The two properties of the residuals we've emphasized here can be applied to
| datasets which have multiple predictors. In this lesson we've loaded the
| dataset attenu which gives data for 23 earthquakes in California.
| Accelerations are estimated based on two predictors, distance and magnitude.

...


  |                                                                            
  |=============================================================         |  87%
| Generate the regression line for this data. Type efit <- lm(accel ~ mag+dist,
| attenu) at the R prompt.

> efit <- lm(accel ~ mag+dist, attenu)

| You are doing so well!


  |                                                                            
  |===============================================================       |  90%
| Verify the mean of the residuals is 0.

> all.equal(mean(efit$residuals), 0)
[1] TRUE

| Almost! Try again. Or, type info() for more options.

| Type "mean(efit$residuals)" at the R prompt.

> mean(efit$residuals)
[1] -1.785061e-18

| You are amazing!


  |                                                                            
  |=================================================================     |  94%
| Using the R function cov verify the residuals are uncorrelated with the
| magnitude predictor, attenu$mag.

> cov(efit$residuals, attenu$mag)
[1] 5.338694e-17

| You're the best!


  |                                                                            
  |====================================================================  |  97%
| Using the R function cov verify the residuals are uncorrelated with the
| distance predictor, attenu$dist.

> cov(efit$residuals, attenu$dist)
[1] 5.253433e-16

| Nice work!


  |                                                                            
  |======================================================================| 100%
| Congrats! You've finished the course on Residuals. We hope it hasn't left a
| bad taste in your mouth.

...

| Are you currently enrolled in the Coursera course associated with this
| lesson?

1: Yes
2: No

Selection: 1

| Would you like me to notify Coursera that you've completed this lesson? If
| so, I'll need to get some more info from you.

1: Yes
2: No
3: Maybe later

Selection: 1

| Is the following information correct?

Course ID: regmods-002
Submission login (email): sandipan.dey@gmail.com
Submission password: P7N3y8jkyC

1: Yes, go ahead!
2: No, I need to change something.

Selection: 1

| I'll try to tell Coursera you've completed this lesson now.

| Great work!

| I've notified Coursera that you have completed regmods-002, Residuals.

| You've reached the end of this lesson! Returning to the main menu...

| Please choose a course, or type 0 to exit swirl.

1: Regression Models
2: Take me to the swirl course repository!


## 3

myPlot <- function(beta){
  y <- galton$child - mean(galton$child)
  x <- galton$parent - mean(galton$parent)
  freqData <- as.data.frame(table(x, y))
  names(freqData) <- c("child", "parent", "freq")
  plot(
    as.numeric(as.vector(freqData$parent)), 
    as.numeric(as.vector(freqData$child)),
    pch = 21, col = "black", bg = "lightblue",
    cex = .15 * freqData$freq, 
    xlab = "parent", 
    ylab = "child"
  )
  abline(0, beta, lwd = 3)
  points(0, 0, cex = 2, pch = 19)
  mse <- mean( (y - beta * x)^2 )
  title(paste("beta = ", beta, "mse = ", round(mse, 3)))
}
#manipulate(myPlot(beta), beta = slider(0.4, .8, step = 0.02))

| What was the minimum mse?

1: 5.0
2: 44
3: .64
4: .66

Selection: 1

| Excellent job!

|===========================================                           |  61%

| Recall that you normalize data by subtracting its mean and dividing by its standard
| deviation. We've done this for the galton child and parent data for you. We've
| stored these normalized values in two vectors, gpa_nor and gch_nor, the normalized
| galton parent and child data.

...

|===============================================                       |  67%

| Use R's function "cor" to compute the correlation between these normalized data
| sets.

> cor(gpa_nor, gch_nor)
[1] 0.4587624

| You are doing so well!

|===================================================                   |  72%

| How does this correlation relate to the correlation of the unnormalized data?

1: It is the same.
2: It is bigger.
3: It is smaller.

Selection: 


| Leaving swirl now. Type swirl() to resume.

> cor(galton$parent, galton$child)
[1] 0.4587624
> cor(gpa_nor, gch_nor)
[1] 0.4587624
> swirl()

| Welcome to swirl! Please sign in. If you've been here before, use the same name as
| you did then. If you are new, call yourself something unique.

What shall I call you? Sandipan

| Would you like to continue with one of these lessons?

1: Regression Models Least Squares Estimation
2: No. Let me start something new.

Selection: 1

| Attemping to load lesson dependencies...

| Package 'UsingR' loaded correctly!



| How does this correlation relate to the correlation of the unnormalized data?

1: It is the same.
2: It is bigger.
3: It is smaller.

Selection: 1

| You nailed it! Good job!

|======================================================                |  78%

| Use R's function "lm" to generate the regression line using this normalized data.
| Store it in a variable called l_nor. Use the parents' heights as the predictors
| (independent variable) and the childrens' as the predicted (dependent). Remember,
| 'lm' needs a formula of the form dependent ~ independent. Since we've created the
| data vectors for you there's no need to provide a second "data" argument as you have
| previously.

> l_nor <- lm(gch_nor ~ gpa_nor)

| Nice work!

|==========================================================            |  83%

| What is the slope of this line?

1: The correlation of the 2 data sets
2: 1.
3: I have no idea

Selection: 


| Leaving swirl now. Type swirl() to resume.

> l_nor <- lm(gch_nor ~ gpa_nor)
> l_nor

Call:
lm(formula = gch_nor ~ gpa_nor)

Coefficients:
(Intercept)      gpa_nor  
2.990e-15    4.588e-01  

> swirl()

| Welcome to swirl! Please sign in. If you've been here before, use the same name as
| you did then. If you are new, call yourself something unique.

What shall I call you? Sandipan

| Would you like to continue with one of these lessons?

1: Regression Models Least Squares Estimation
2: No. Let me start something new.

Selection: 1

| Attemping to load lesson dependencies...

| Package 'UsingR' loaded correctly!



| What is the slope of this line?

1: I have no idea
2: 1.
3: The correlation of the 2 data sets

Selection: 3

| You are really on a roll!

|==============================================================        |  89%

| If you swapped the outcome (Y) and predictor (X) of your original (unnormalized)
| data, (for example, used childrens' heights to predict their parents), what would
| the slope of the new regression line be?

1: 1.
2: I have no idea
3: the same as the original
4: correlation(X,Y) * sd(X)/sd(Y)

Selection: 4

| That's a job well done!

|==================================================================    |  94%

| We'll close with a final display of source code from the slides. It plots the galton
| data with three regression lines, the original in red with the children as the
| outcome, a new blue line with the parents' as outcome and childrens' as predictor,
| and a black line with the slope scaled so it equals the ratio of the standard
| deviations.

...

|======================================================================| 100%

| Congrats! You've concluded this lesson on ordinary least squares which are truly
| extraordinary!

...

| Are you currently enrolled in the Coursera course associated with this lesson?

1: Yes
2: No

Selection: 1

| Would you like me to notify Coursera that you've completed this lesson? If so, I'll
| need to get some more info from you.

1: Yes
2: No
3: Maybe later

Selection: 1

| Is the following information correct?

Course ID: regmods-002
Submission login (email): sandipan.dey@gmail.com
Submission password: P7N3y8jkyC

1: Yes, go ahead!
2: No, I need to change something.

Selection: 1

| I'll try to tell Coursera you've completed this lesson now.

| Great work!

| I've notified Coursera that you have completed regmods-002,
| Least_Squares_Estimation.

| You've reached the end of this lesson! Returning to the main menu...

| Please choose a course, or type 0 to exit swirl.

1: Regression Models
2: Take me to the swirl course repository!

## 4

fit <- lm(child ~ parent, galton)
sqrt(sum(fit$residuals^2)/(n-2))
summary(fit)$sigma
sqrt(deviance(fit)/(n-2))

mu <- mean(galton$child)
sTot <- sum((galton$child - mu)^2)
sRes <- deviance(fit)
1 - sRes/sTot
summary(fit)$r.squared
cor(galton$parent, galton$child)^2

Selection: 4

| Attemping to load lesson dependencies...

| Package 'UsingR' loaded correctly!

|                                                                             |   0%

| Residual Variation. (Slides for this and other Data Science courses may be found at
| github https://github.com/DataScienceSpecialization/courses. If you care to use
| them, they must be downloaded as a zip file and viewed locally. This lesson
| corresponds to Regression_Models/01_06_residualVariation.)

...

|====                                                                         |   5%

| As shown in the slides, residuals are useful for indicating how well data points fit
| a statistical model. They "can be thought of as the outcome (Y) with the linear
| association of the predictor (X) removed. One differentiates residual variation
| (variation after removing the predictor) from systematic variation (variation
                                                                      | explained by the regression model)."

...

|=======                                                                      |  10%

| It can also be shown that, given a model, the maximum likelihood estimate of the
| variance of the random error is the average squared residual. However, since our
| linear model with one predictor requires two parameters we have only (n-2) degrees
| of freedom. Therefore, to calculate an "average" squared residual to estimate the
| variance we use the formula 1/(n-2) * (the sum of the squared residuals). If we
| divided the sum of the squared residuals by n, instead of n-2, the result would give
| a biased estimate.

...

|===========                                                                  |  14%

| To see this we'll use our favorite Galton height data. First regenerate the
| regression line and call it fit. Use the R function lm and recall that by default
| its first argument is a formula such as "child ~ parent" and its second is the
| dataset, in this case galton.

> fit <- lm(child ~ parent, galton)

| Nice work!

|===============                                                              |  19%

| First, we'll use the residuals (fit$residuals) of our model to estimate the standard
| deviation (sigma) of the error. We've already defined n for you as the number of
| points in Galton's dataset (928).

...

|==================                                                           |  24%

| Calculate the sum of the squared residuals divided by the quantity (n-2).  Then take
| the square root.

> sqrt(sum(fit$residuals^2)/(n-2))
[1] 2.238547

| Keep up the great work!

|======================                                                       |  29%

| Now look at the "sigma" portion of the summary of fit, "summary(fit)$sigma".

> summary(fit)$sigma
[1] 2.238547

| You are amazing!

|==========================                                                   |  33%

| Pretty cool, huh?

...

|=============================                                                |  38%

| Another cool thing - take the sqrt of "deviance(fit)/(n-2)" at the R prompt.

> deviance(fit)/(n-2)
[1] 5.011094

| Keep trying! Or, type info() for more options.

| Type "sqrt(deviance(fit)/(n-2))" at the R prompt.

> sqrt(deviance(fit)/(n-2))
[1] 2.238547

| You got it right!

|=================================                                            |  43%

| Another useful fact shown in the slides was

...

|=====================================                                        |  48%

| Total Variation = Residual Variation + Regression Variation

...

|========================================                                     |  52%

| Recall the beauty of the slide full of algebra which proved this fact. It had a
| bunch of Y's, some with hats and some with bars and several summations of squared
| values. The Y's with hats were the estimates provided by the model. (They were on
| the regression line.) The Y with the bar was the mean or average of the data. Which
| sum of squared term represented Total Variation?

1: Yi_hat-mean(Yi)
2: Yi-Yi_hat
3: Yi-mean(Yi)

Selection: 3

| You are quite good my friend!

|============================================                                 |  57%

| Which sum of squared term represents Residual Variation?

1: Yi-mean(Yi)
2: Yi_hat-mean(Yi)
3: Yi-Yi_hat

Selection: 3

| That's correct!

|================================================                             |  62%

| The term R^2 represents the percent of total variation described by the model, the
| regression variation (the term we didn't ask about in the preceding multiple choice
| questions). Also, since it is a percent we need a ratio or fraction of sums of
| squares. Let's do this now for our Galton data.

...

|===================================================                          |  67%

| We'll start with easy steps. Calculate the mean of the children's heights and store
| it in a variable called mu. Recall that we reference the childrens' heights with the
| expression 'galton$child' and the parents' heights with the expression
| 'galton$parent'.

> mu <- mean(galton$child)

| Nice work!

|=======================================================                      |  71%

| Recall that centering data means subtracting the mean from each data point. Now
| calculate the sum of the squares of the centered children's heights and store the
| result in a variable called sTot. This represents the Total Variation of the data.

> sTot <- sum((galton$child - mu)^2)

| You nailed it! Good job!

|===========================================================                  |  76%

| Now create the variable sRes. Use the R function deviance to calculate the sum of
| the squares of the residuals. These are the distances between the children's heights
| and the regression line. This represents the Residual Variation.

> sRes <- deviance(fit)

| You're the best!

|==============================================================               |  81%

| Finally, the ratio sRes/sTot represents the percent of total variation contributed
| by the residuals. To find the percent contributed by the model, i.e., the regression
| variation, subtract the fraction sRes/sTot from 1.  This is the value R^2.

> 1 - sRes/sTot
[1] 0.2104629

| You got it!

|==================================================================           |  86%

| For fun you can compare your result to the values shown in summary(fit)$r.squared to
| see if it looks familiar. Do this now.

> summary(fit)$r
NULL

| Not quite right, but keep trying. Or, type info() for more options.

| Type "summary(fit)$r.squared" at the R prompt.

> summary(fit)$r.squared
[1] 0.2104629

| You are quite good my friend!

|======================================================================       |  90%

| To see some real magic, compute the square of the correlation of the galton data,
| the children and parents. Use the R function cor.

> (cor(galton$child, galton$parent))^2
[1] 0.2104629

| Almost! Try again. Or, type info() for more options.

| Type "cor(galton$parent,galton$child)^2" at the R prompt.

> cor(galton$parent, galton$child)^2
[1] 0.2104629

| Keep up the great work!

|=========================================================================    |  95%

| We'll now summarize useful facts about R^2. It is the percentage of variation
| explained by the regression model. As a percentage it is between 0 and 1. It also
| equals the sample correlation squared. However, R^2 doesn't tell the whole story.

...

|=============================================================================| 100%

| Congrats! You've finished this lesson on Residual Variation.

...

| Are you currently enrolled in the Coursera course associated with this lesson?

1: Yes
2: No

Selection: 1

| Would you like me to notify Coursera that you've completed this lesson? If so, I'll
| need to get some more info from you.

1: Yes
2: No
3: Maybe later

Selection: 1

| Is the following information correct?

Course ID: regmods-002
Submission login (email): sandipan.dey@gmail.com
Submission password: P7N3y8jkyC

1: Yes, go ahead!
2: No, I need to change something.

ones <- rep(1, nrow(galton))
lm(child ~ ones + parent -1, galton)
lm(child ~ ones + parent, galton)
lm(child ~ 1, galton)
mean(galton$child)

View(trees)

fit <- lm(Volume ~ Girth + Height + Constant -1, trees)
trees2 <- eliminate("Girth", trees)
head(trees2)
fit2 <- lm(Volume ~ Height + Constant -1, trees2)
lapply(list(fit, fit2), coef)


## 5

Selection: 5
  |                                                                             |   0%

| Introduction to Multivariable Regression. (Slides for this and other Data Science
| courses may be found at github https://github.com/DataScienceSpecialization/courses.
| If you care to use them, they must be downloaded as a zip file and viewed locally.
| This lesson corresponds to Regression_Models/02_01_multivariate.)

...

|===                                                                          |   4%

| In this lesson we'll illustrate that regression in many variables amounts to a
| series of regressions in one. Using regression in one variable, we'll show how to
| eliminate any chosen regressor, thus reducing a regression in N variables, to a
| regression in N-1. Hence, if we know how to do a regression in 1 variable, we can do
| a regression in 2. Once we know how to do a regression in 2 variables, we can do a
| regression in 3, and so on. We begin with the galton data and a review of
| eliminating the intercept by subtracting the means.

...

|======                                                                       |   8%

| When we perform a regression in one variable, such as lm(child ~ parent, galton), we
| get two coefficients, a slope and an intercept. The intercept is really the
| coefficient of a special regressor which has the same value, 1, at every sample. The
| function, lm, includes this regressor by default.

...

|=========                                                                    |  12%

| We'll demonstrate by substituting an all-ones regressor of our own. This regressor
| must have the same number of samples as galton (928.) Create such an object and name
| it ones, using ones <- rep(1, nrow(galton)), or some equivalent expression.

> ones <- rep(1, nrow(galton))

| Great job!

|============                                                                 |  16%

| The galton data has already been loaded. The default intercept can be excluded by
| using -1 in the formula. Perform a regression which substitutes our regressor, ones,
| for the default using lm(child ~ ones + parent -1, galton). Since we want the result
| to print, don't assign it to a variable.

> lm(child ~ ones + parent -1, galton)

Call:
lm(formula = child ~ ones + parent - 1, data = galton)

Coefficients:
ones   parent  
23.9415   0.6463  


| Excellent job!

|===============                                                              |  20%

| The coefficient of ones is 23.9415. Now use the default, lm(child ~ parent, galton),
| to show the intercept has the same value. This time, DO NOT suppress the the
| intercept with -1.

> lm(child ~ ones + parent, galton)

Call:
lm(formula = child ~ ones + parent, data = galton)

Coefficients:
(Intercept)         ones       parent  
23.9415           NA       0.6463  


| Excellent job!

|==================                                                           |  24%

| The regression in one variable given by lm(child ~ parent, galton) really involves
| two regressors, the variable, parent, and a regressor of all ones.

1: True
2: False

Selection: 2

| Almost! Try again.

| Since it produces two coefficients, it must involve two regressors. One is a
| variable named parent, the other is the constant, 1.

1: True
2: False

Selection: 1

| Keep up the great work!

|======================                                                       |  28%

| In earlier lessons we demonstrated that the regression line given by lm(child ~
| parent, galton) goes through the point x=mean(parent), y=mean(child). We also showed
| that if we subtract the mean from each variable, the regression line goes through
| the origin, x=0, y=0, hence its intercept is zero. Thus, by subtracting the means,
| we eliminate one of the two regressors, the constant, leaving just one, parent. The
| coefficient of the remaining regressor is the slope.

...

|=========================                                                    |  32%

| Subtracting the means to eliminate the intercept is a special case of a general
| technique which is sometimes called Gaussian Elimination. As it applies here, the
| general technique is to pick one regressor and to replace all other variables by the
| residuals of their regressions against that one.

...

|============================                                                 |  36%

| Suppose, as claimed, that subtracting a variable's mean is a special case of
| replacing the variable with a residual. In this special case, it would be the
| residual of a regression against what?

1: The constant, 1
2: The outcome
3: The variable itself

Selection: 1

| Nice work!

|===============================                                              |  40%

| The mean of a variable is the coefficient of its regression against the constant, 1.
| Thus, subtracting the mean is equivalent to replacing a variable by the residual of
| its regression against 1. In an R formula, the constant regressor can be represented
| by a 1 on the right hand side. Thus, the expression, lm(child ~ 1, galton),
| regresses child against the constant, 1. Recall that in the galton data, the mean
| height of a child was 68.09 inches. Use lm(child ~ 1, galton) to compare the
| resulting coefficient (the intercept) and the mean height of 68.09. Since we want
| the result to print, don't assign it a name.

> lm(child ~ 1, galton)

Call:
lm(formula = child ~ 1, data = galton)

Coefficients:
(Intercept)  
68.09  


| That's a job well done!

|==================================                                           |  44%

| The mean of a variable is equal to its regression against the constant, 1.

1: True
2: False

Selection: 


| Leaving swirl now. Type swirl() to resume.

> mean(galton$child)
[1] 68.08847
> lm(child ~ 1, galton)

Call:
lm(formula = child ~ 1, data = galton)

Coefficients:
(Intercept)  
68.09  

> swirl()

| Welcome to swirl! Please sign in. If you've been here before, use the same name as
| you did then. If you are new, call yourself something unique.

What shall I call you? Sandipan

| Would you like to continue with one of these lessons?

1: Regression Models Introduction to Multivariable Regression
2: No. Let me start something new.

Selection: 1


| The mean of a variable is equal to its regression against the constant, 1.

1: False
2: True

Selection: 1

| Almost! Try again.

| The mean is a number which minimizes the sum of squared differences between itself
| and the variable.

1: True
2: False

Selection: 2

| That's not the answer I was looking for, but try again.

| The mean is a number which minimizes the sum of squared differences between itself
| and the variable.

1: False
2: True

Selection: 2

| You're the best!

|=====================================                                        |  48%

| To illustrate the general case we'll use the trees data from the datasets package.
| The idea is to predict the Volume of timber which a tree might produce from
| measurements of its Height and Girth. To avoid treating the intercept as a special
| case, we have added a column of 1's to the data which we shall use in its place.
| Please take a moment to inspect the data using either View(trees) or head(trees).

> View(trees)

| You are amazing!

|========================================                                     |  52%

| A file of relevant code has been copied to your working directory and sourced. The
| file, elimination.R, should have appeared in your editor. If not, please open it
| manually.

...

|===========================================                                  |  56%

| The general technique is to pick one predictor and to replace all other variables by
| the residuals of their regressions against that one. The function, regressOneOnOne,
| in eliminate.R performs the first step of this process. Given the name of a
| predictor and one other variable, other, it returns the residual of other when
| regressed against predictor. In its first line, labeled Point A, it creates a
| formula. Suppose that predictor were 'Girth' and other were 'Volume'. What formula
| would it create?

1: Girth ~ Volume - 1
2: Volume ~ Girth
3: Volume ~ Girth - 1

Selection: 3

| That's correct!

|==============================================                               |  60%

| The remaining function, eliminate, applies regressOneOnOne to all variables except a
| given predictor and collects the residuals in a data frame. We'll first show that
| when we eliminate one regressor from the data, a regression on the remaining will
| produce their correct coefficients. (Of course, the coefficient of the eliminated
| regressor will be missing, but more about that later.)

...

|=================================================                            |  64%

| For reference, create a model based on all three regressors, Girth, Height, and
| Constant, and assign the result to a variable named fit. Use an expression such as
| fit <- lm(Volume ~ Girth + Height + Constant -1, trees). Don't forget the -1.

> fit <- lm(Volume ~ Girth + Height + Constant -1, trees)

| Great job!

|====================================================                         |  68%

| Now let's eliminate Girth from the data set. Call the reduced data set trees2 to
| indicate it has only 2 regressors. Use the expression trees2 <- eliminate("Girth",
| trees).

> trees2 <- eliminate("Girth", trees)

| You got it!

|=======================================================                      |  72%

| Use head(trees2) or View(trees2) to inspect the reduced data set.

> head(trees2)
Constant   Height     Volume
1 0.4057735 24.38809  -9.793826
2 0.3842954 17.73947 -10.520109
3 0.3699767 14.64038 -11.104298
4 0.2482677 14.29818  -9.019900
5 0.2339490 22.19910  -7.104089
6 0.2267896 23.64956  -6.446183

| You're the best!

|===========================================================                  |  76%

| Why, in trees2, is the Constant column not constant?

1: There must be some mistake
2: Computational precision was insufficient.
3: The constant, 1, has been replaced by its residual when regressed against Girth.

Selection: 3

| Keep up the great work!

|==============================================================               |  80%

| Now create a model, called fit2, using the reduced data set. Use an expression such
| as fit2 <- lm(Volume ~ Height + Constant -1, trees2). Don't forget to use -1 in the
| formula.

> fit2 <- lm(Volume ~ Height + Constant -1, trees2)

| You nailed it! Good job!

|=================================================================            |  84%

| Use the expression lapply(list(fit, fit2), coef) to print coefficients of fit and
| fit2 for comparison.

> lapply(list(fit, fit2), coef)
[[1]]
Girth      Height    Constant 
4.7081605   0.3392512 -57.9876589 

[[2]]
Height    Constant 
0.3392512 -57.9876589 


| You got it!

|====================================================================         |  88%

| The coefficient of the eliminated variable is missing, of course. One way to get it
| would be to go back to the original data, trees, eliminate a different regressor,
| such as Height, and do another 2 variable regession, as above. There are much more
| efficient ways, but efficiency is not the point of this demonstration. We have shown
| how to reduce a regression in 3 variables to a regression in 2. We can go further
| and eliminate another variable, reducing a regression in 2 variables to a regression
| in 1.

...

|=======================================================================      |  92%

| Here is the final step. We have used eliminate("Height", trees2) to reduce the data
| to the outcome, Volume, and the Constant regressor. We have regressed Volume on
| Constant, and printed the coefficient as shown in the command above the answer. As
| you can see, the coefficient of Constant agrees with previous values.


Call:
lm(formula = Volume ~ Constant - 1, data = eliminate("Height", 
trees2))

Coefficients:
Constant  
-57.99  

...

|==========================================================================   |  96%

| Suppose we were given a multivariable regression problem involving an outcome and N
| regressors, where N > 1. Using only single-variable regression, how can the problem
| be reduced to a problem with only N-1 regressors?

1: Subtract the mean from the outcome and each regressor.
2: Pick any regressor and replace the outcome and all other regressors by their residuals against the chosen one.

Selection: 2

| You're the best!

|=============================================================================| 100%

| We have illustrated that regression in many variables amounts to a series of
| regressions in one. The actual algorithms used by functions such as lm are more
| efficient, but are computationally equivalent to what we have done. That is, the
| algorithms use equivalent steps but combine them more efficiently and abstractly.
| This completes the lesson.

...

| Are you currently enrolled in the Coursera course associated with this lesson?

1: Yes
2: No

Selection: 1

| Would you like me to notify Coursera that you've completed this lesson? If so, I'll
| need to get some more info from you.

1: Yes
2: No
3: Maybe later

Selection: 1

| Is the following information correct?

Course ID: regmods-002
Submission login (email): sandipan.dey@gmail.com
Submission password: P7N3y8jkyC

1: Yes, go ahead!
2: No, I need to change something.

Selection: 1

| I'll try to tell Coursera you've completed this lesson now.

| Great work!

| I've notified Coursera that you have completed regmods-002,
| Introduction_to_Multivariable_Regression.

| You've reached the end of this lesson! Returning to the main menu...

| Please choose a course, or type 0 to exit swirl.

1: Regression Models
2: Take me to the swirl course repository!


## 6

all <- lm(Fertility ~ ., data = swiss)
summary(all)
summary(lm(Fertility ~ Agriculture, swiss))
cor(swiss$Education, swiss$Examination)
cor(swiss$Agriculture, swiss$Education)
makelms()
ec <- swiss$Examination + swiss$Catholic
efit <- lm(Fertility ~ . + ec, data = swiss)
all$coefficients - efit$coefficients

Selection: 6

| Attemping to load lesson dependencies...

| Package 'UsingR' loaded correctly!

| Package 'datasets' loaded correctly!

| Package 'stats' loaded correctly!

| Package 'graphics' loaded correctly!

|                                                                             |   0%

| MultiVar_Examples. (Slides for this and other Data Science courses may be found at
| github https://github.com/DataScienceSpecialization/courses. If you care to use
| them, they must be downloaded as a zip file and viewed locally. This lesson
| corresponds to Regression_Models/02_02_multivariateExamples.)

...

|====                                                                         |   5%

| In this lesson, we'll look at some examples of regression models with more than one
| variable. We'll begin with the Swiss data which we've taken the liberty to load for
| you. This data is part of R's datasets package. It was gathered in 1888, a time of
| demographic change in Switzerland, and measured six quantities in 47 French-speaking
| provinces of Switzerland. We used the code from the slides (the R function pairs) to
| display here a 6 by 6 array of scatterplots showing pairwise relationships between
| the variables. All of the variables, except for fertility, are proportions of
| population. For example, "Examination" shows the percentage of draftees receiving
| the highest mark on an army exam, and "Education" the percentage of draftees with
| education beyond primary school.

...

|=======                                                                      |   9%

| From the plot, which is NOT one of the factors measured?

1: Fertility
2: Infant Mortality
3: Catholic
4: Obesity

Selection: 4

| Excellent job!

|==========                                                                   |  14%

| First, use the R function lm to generate the linear model "all" in which Fertility
| is the variable dependent on all the others. Use the R shorthand "." to represent
| the five independent variables in the formula passed to lm.  Remember the data is
| "swiss".

> all <- lm(Fertility ~ ., data = swiss)

| Great job!

|==============                                                               |  18%

| Now look at the summary of the linear model all.

> summary(all)

Call:
lm(formula = Fertility ~ ., data = swiss)

Residuals:
Min       1Q   Median       3Q      Max 
-15.2743  -5.2617   0.5032   4.1198  15.3213 

Coefficients:
Estimate Std. Error t value Pr(>|t|)    
(Intercept)      66.91518   10.70604   6.250 1.91e-07 ***
Agriculture      -0.17211    0.07030  -2.448  0.01873 *  
Examination      -0.25801    0.25388  -1.016  0.31546    
Education        -0.87094    0.18303  -4.758 2.43e-05 ***
Catholic          0.10412    0.03526   2.953  0.00519 ** 
Infant.Mortality  1.07705    0.38172   2.822  0.00734 ** 
---
Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

Residual standard error: 7.165 on 41 degrees of freedom
Multiple R-squared:  0.7067,  Adjusted R-squared:  0.671 
F-statistic: 19.76 on 5 and 41 DF,  p-value: 5.594e-10


| You nailed it! Good job!

|==================                                                           |  23%

| Recall that the Estimates are the coeffients of the independent variables of the
| linear model (all of which are percentages) and they reflect an estimated change in
| the dependent variable (fertility) when the corresponding independent variable
| changes. So, for every 1% increase in percent of males involved in agriculture as an
| occupation we expect a .17 decrease in fertility, holding all the other variables
| constant; for every 1% increase in Catholicism, we expect a .10 increase in
| fertility, holding all other variables constant.

...

|=====================                                                        |  27%

| The "*" at the far end of the row indicates that the influence of Agriculture on
| Fertility is significant. At what alpha level is the t-test of Agriculture
| significant?

1: 0.01
2: R doesn't say
3: 0.05
4: 0.1

Selection: 3

| Keep up the great work!

|========================                                                     |  32%

| Now generate the summary of another linear model (don't store it in a new variable)
| in which Fertility depends only on agriculture.

> m <- lm(Fertility ~ Agriculture, data = swiss)

| Almost! Try again. Or, type info() for more options.

| Type "summary(lm(Fertility ~ Agriculture, swiss))" at the R prompt.

> summary(lm(Fertility ~ Agriculture, data = swiss))

Call:
lm(formula = Fertility ~ Agriculture, data = swiss)

Residuals:
Min       1Q   Median       3Q      Max 
-25.5374  -7.8685  -0.6362   9.0464  24.4858 

Coefficients:
Estimate Std. Error t value Pr(>|t|)    
(Intercept) 60.30438    4.25126  14.185   <2e-16 ***
Agriculture  0.19420    0.07671   2.532   0.0149 *  
---
Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

Residual standard error: 11.82 on 45 degrees of freedom
Multiple R-squared:  0.1247,	Adjusted R-squared:  0.1052 
F-statistic: 6.409 on 1 and 45 DF,  p-value: 0.01492


| Almost! Try again. Or, type info() for more options.

| Type "summary(lm(Fertility ~ Agriculture, swiss))" at the R prompt.

> summary(lm(Fertility ~ Agriculture, swiss))

Call:
lm(formula = Fertility ~ Agriculture, data = swiss)

Residuals:
Min       1Q   Median       3Q      Max 
-25.5374  -7.8685  -0.6362   9.0464  24.4858 

Coefficients:
Estimate Std. Error t value Pr(>|t|)    
(Intercept) 60.30438    4.25126  14.185   <2e-16 ***
Agriculture  0.19420    0.07671   2.532   0.0149 *  
---
Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

Residual standard error: 11.82 on 45 degrees of freedom
Multiple R-squared:  0.1247,	Adjusted R-squared:  0.1052 
F-statistic: 6.409 on 1 and 45 DF,  p-value: 0.01492


| You are quite good my friend!

|============================                                                 |  36%

| What is the coefficient of agriculture in this new model?

1: 0.19420
2: *
3: 60.30438
4: 0.07671

Selection: 1

| Nice work!

|================================                                             |  41%

| The interesting point is that the sign of the Agriculture coefficient changed from
| negative (when all the variables were included in the model) to positive (when the
| model only considered Agriculture). Obviously the presence of the other factors
| affects the influence Agriculture has on Fertility.

...

|===================================                                          |  45%

| Let's consider the relationship between some of the factors. How would you expect
| level Education and performance on an Examination to be related?

1: They would be uncorrelated
2: I would not be able to guess without more information
3: They would be correlated

Selection: 3

| You are quite good my friend!

|======================================                                       |  50%

| Now check your intuition with the R command "cor". This computes the correlation
| between Examination and Education.

> cor(swiss$Education, swiss$Examination)
[1] 0.6984153

| Excellent job!

|==========================================                                   |  55%

| The correlation of .6984 shows the two are correlated. Now find the correlation
| between Agriculture and Education.

> cor(swiss$Agriculture, swiss$Education)
[1] -0.6395225

| You are amazing!

|==============================================                               |  59%

| The negative correlation (-.6395) between Agriculture and Education might be
| affecting Agriculture's influence on Fertility. I've loaded and sourced the file
| swissLMs.R in your working directory. In it is a function makelms() which generates
| a sequence of five linear models. Each model has one more independent variable than
| the preceding model, so the first has just one independent variable, Agriculture,
| and the last has all 5. I've tried loading the source code in your editor. If I
| haven't done this, open the file manually so you can look at the code.

...

|=================================================                            |  64%

| Now run the function makelms() to see how the addition of variables affects the
| coefficient of Agriculture in the models.

> makelms()
Agriculture Agriculture Agriculture Agriculture Agriculture 
0.1942017   0.1095281  -0.2030377  -0.2206455  -0.1721140 
Agriculture Agriculture Agriculture Agriculture Agriculture 
0.1942017   0.1095281  -0.2030377  -0.2206455  -0.1721140 

| You are doing so well!

|=====================================================                        |  68%

| The addition of which variable changes the sign of Agriculture's coefficient from
| positive to negative?

1: Catholic
2: Education
3: Examination
4: Infant.Mortality

Selection: 2

| That's correct!

|========================================================                     |  73%

| Now we'll show what happens when we add a variable that provides no new linear
| information to a model. Create a variable ec that is the sum of swiss$Examination
| and swiss$Catholic.

> ec <- swiss$Examination + swiss$Catholic

| That's correct!

|============================================================                 |  77%

| Now generate a new model efit with Fertility as the dependent variable and the
| remaining 5 of the original variables AND ec as the independent variables. Use the R
| shorthand ". + ec" for the righthand side of the formula.

> efit <- lm(Fertility ~ . + ec, data = swiss)

| You're the best!

|===============================================================              |  82%

| We'll see that R ignores this new term since it doesn't add any information to the
| model.

...

|==================================================================           |  86%

| Subtract the efit coefficients from the coefficients of the first model you created,
| all.

> 

> all$coefficients - efit$coefficients
(Intercept)      Agriculture      Examination        Education         Catholic 
0                0                0                0                0 
Infant.Mortality               ec 
0               NA 
Warning message:
In all$coefficients - efit$coefficients :
longer object length is not a multiple of shorter object length

| That's correct!

|======================================================================       |  91%

| Which is the coefficient of ec?

1: I haven't a clue.
2: 0
3: NA

Selection: 3

| That's a job well done!

|==========================================================================   |  95%

| This tells us that

1: R is a really cool
2: Adding ec doesn't change the model
3: Adding ec zeroes out the coefficients

Selection: 2

| Nice work!

|=============================================================================| 100%

| Congrats! You've concluded this first lesson on multivariable linear models.

...

| You've reached the end of this lesson! Returning to the main menu...

| Please choose a course, or type 0 to exit swirl.

1: Regression Models
2: Take me to the swirl course repository!

## 7
dim(InsectSprays)
head(InsectSprays, 15)
sA
summary(InsectSprays[,2])
sapply(InsectSprays, class)
fit <- lm(count~spray, data=InsectSprays)
summary(fit)$coef
est <- summary(fit)$coef[,1]
mean(sA)
est[1] + est[2]
mean(sB)
nfit <- lm(count~spray-1, data=InsectSprays)
summary(nfit)$coef
spray2 <- relevel(InsectSprays$spray, "C")
fit2 <- lm(count~spray2, data=InsectSprays)
summary(fit2)$coef
mean(sC)
(fit$coef[2] - fit$coef[3]) / 1.6011
Selection: 1

| Please choose a lesson, or type 0 to return to course menu.

1: Introduction
2: Residuals
3: Least Squares Estimation
4: Residual Variation
5: Introduction to Multivariable Regression
6: MultiVar Examples
7: MultiVar Examples2
8: MultiVar Examples3
9: Residuals Diagnostics and Variation
10: Variance Inflation Factors
11: Overfitting and Underfitting
12: Binary Outcomes
13: Count Outcomes

Selection: 7

| Attemping to load lesson dependencies...

| Package 'UsingR' loaded correctly!

| Package 'datasets' loaded correctly!

| Package 'stats' loaded correctly!

| Package 'graphics' loaded correctly!

|                                                                             |   0%

| MultiVar_Examples2. (Slides for this and other Data Science courses may be found at
| github https://github.com/DataScienceSpecialization/courses. If you care to use
| them, they must be downloaded as a zip file and viewed locally. This lesson
| corresponds to Regression_Models/02_02_multivariateExamples.)

...

|==                                                                           |   3%

| This is the second lesson in which we'll look at some regression models with more
| than one independent variable. We'll begin with the InsectSprays data which we've
| taken the liberty to load for you. This data is part of R's datasets package. It
| shows the effectiveness of different insect sprays. We've used the code from the
| slides to show you a boxplot of the data.

...

|=====                                                                        |   6%

| How many Insect Sprays are in this dataset?

> 6
[1] 6

| That's correct!

|=======                                                                      |   9%

| From the boxplot, which spray has the largest median?

ANSWER: B

| You are amazing!

|==========                                                                   |  12%

| Let's first try to get a better understanding of the dataset InsectSprays. Use the R
| function dim to find the dimensions of the data.

> dim(InsectSprays)
[1] 72  2

| That's a job well done!

|============                                                                 |  16%

| The R function dim says that InsectSprays is a 72 by 2 array. Use the R function
| head to look at the first 15 elements of InsectSprays.

> head(InsectSprays, 15)
count spray
1     10     A
2      7     A
3     20     A
4     14     A
5     14     A
6     12     A
7     10     A
8     23     A
9     17     A
10    20     A
11    14     A
12    13     A
13    11     B
14    17     B
15    21     B

| You're the best!

|==============                                                               |  19%

| So this dataset contains 72 counts, each associated with a particular different
| spray. The counts are in the first column and a letter identifying the spray in the
| second. To save you some typing we've created 6 arrays with just the count data for
| each spray. The arrays have the names sx, where x is A,B,C,D,E or F. Type one of the
| names (your choice) of these arrays to see what we're talking about.

> A
Error: object 'A' not found
> sA
[1] 10  7 20 14 14 12 10 23 17 20 14 13

| Nice work!

|=================                                                            |  22%

| As a check, run the R command summary on the second column of the dataset to see how
| many entries we have for each spray.  (Recall that the expression M[ ,2] yields the
| second column of the array M.)

> summary(InsectSprays[,2])
A  B  C  D  E  F 
12 12 12 12 12 12 

| Excellent job!

|===================                                                          |  25%

| It's not surprising that with 72 counts we'd have 12 count for each of the 6 sprays.
| In this lesson we'll consider multilevel factor levels and how we interpret linear
| models of data with more than 2 factors.

...

  |======================                                                       |  28%

| Use the R function sapply to find out the classes of the columns of the data.
> sapply(InsectSprays, class)
    count     spray 
"numeric"  "factor" 

| That's a job well done!

|========================                                                     |  31%

| The class of the second "spray" column is factor. Recall from the slides that the
| equation representing the relationship between a particular outcome and several
| factors contains binary variables, one for each factor. This data has 6 factors so
| we need 6 dummy variables. Each will indicate if a particular outcome (a count) is
| associated with a specific factor or category (insect spray).

...

|==========================                                                   |  34%

| Using R's lm function, generate the linear model in which count is the dependent
| variable and spray is the independent. Recall that in R formula has the form y ~ x,
| where y depends on the predictor x. The data set is InsectSprays. Store the model in
| the variable fit.

> fit <- lm(count~spray, data=InsectSprays)

| Nice work!

|=============================                                                |  38%

| Using R's summary function, look at the coefficients of the model. Recall that these
| can be accessed with the R construct x$coef.

> fit$coef
(Intercept)      sprayB      sprayC      sprayD      sprayE      sprayF 
14.5000000   0.8333333 -12.4166667  -9.5833333 -11.0000000   2.1666667 

| Almost! Try again. Or, type info() for more options.

| Type "summary(fit)$coef" at the R prompt.

> summary(fit$coef)
Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
-12.420 -10.650  -4.375  -2.583   1.833  14.500 

| That's not the answer I was looking for, but try again. Or, type info() for more
| options.

| Type "summary(fit)$coef" at the R prompt.

> summary(fit)$coef
Estimate Std. Error    t value     Pr(>|t|)
(Intercept)  14.5000000   1.132156 12.8074279 1.470512e-19
sprayB        0.8333333   1.601110  0.5204724 6.044761e-01
sprayC      -12.4166667   1.601110 -7.7550382 7.266893e-11
sprayD       -9.5833333   1.601110 -5.9854322 9.816910e-08
sprayE      -11.0000000   1.601110 -6.8702352 2.753922e-09
sprayF        2.1666667   1.601110  1.3532281 1.805998e-01

| Excellent job!

|===============================                                              |  41%

| Notice that R returns a 6 by 4 array. For convenience, store off the first column of
| this array, the Estimate column, in a variable called est. Remember the R construct
| for accessing the first column is x[,1].

> est <- summary(fit)$coef[,1]

| You are amazing!

|==================================                                           |  44%

| Notice that sprayA does not appear explicitly in the list of Estimates. It is there,
| however, as the first entry in the Estimate column. It is labeled as "(Intercept)".
| That is because sprayA is the first in the alphabetical list of the levels of the
| factor, and R by default uses the first level as the reference against which the
| other levels or groups are compared when doing its t-tests (shown in the third
| column).

...

|====================================                                         |  47%

| What do the Estimates of this model represent? Of course they are the coefficients
| of the binary or dummy variables associated with sprays. More importantly, the
| Intercept is the mean of the reference group, in this case sprayA, and the other
| Estimates are the distances of the other groups' means from the reference mean.
| Let's verify these claims now. First compute the mean of the sprayA counts. Remember
| the counts are all stored in the vectors named sx. Now we're interested in finding
| the mean of sA.

> mean(sA)
[1] 14.5

| You're the best!

|======================================                                       |  50%

| What do you think the mean of sprayB is?

1: 0.83333
2: 15.3333
3: I haven't a clue
4: -12.41667

Selection: 1

| Almost! Try again.

| Adding the value of the Intercept to the Estimate for sprayB yields the empirical
| mean of sprayB.

1: 15.3333
2: 0.83333
3: -12.41667
4: I haven't a clue

Selection: 1

| That's correct!

|=========================================                                    |  53%

| Verify this now by using R's mean function to compute the mean of sprayB.

> mean(sB)
[1] 15.33333

| You are doing so well!

|===========================================                                  |  56%

| Let's generate another model of this data, this time omitting the intercept. We can
| easily use R's lm function to do this by appending " - 1" to the formula, e.g.,
| count ~ spray - 1. This tells R to omit the first level. Do this now and store the
| new model in the variable nfit.

> nfit <- lm(count~spray-1, data=InsectSprays)

| That's correct!

|==============================================                               |  59%

| Now, as before, look at the coefficient portion of the summary of nfit.

> summary(nfit)$coef
Estimate Std. Error   t value     Pr(>|t|)
sprayA 14.500000   1.132156 12.807428 1.470512e-19
sprayB 15.333333   1.132156 13.543487 1.001994e-20
sprayC  2.083333   1.132156  1.840148 7.024334e-02
sprayD  4.916667   1.132156  4.342749 4.953047e-05
sprayE  3.500000   1.132156  3.091448 2.916794e-03
sprayF 16.666667   1.132156 14.721181 1.573471e-22

| You nailed it! Good job!

|================================================                             |  62%

| Notice that sprayA now appears explicitly in the list of Estimates. Also notice how
| the values of the columns have changed. The means of all the groups are now
| explicitly shown in the Estimate column. Remember that previously, with an
| intercept, sprayA was excluded, its mean was the intercept, and the values for the
| other sprays (estimates, standard errors, and t-tests) were all computed relative to
| sprayA, the reference group. Omitting the intercept clearly affected the model.

...

|===================================================                          |  66%

| What values does the Estimate column now show?

1: The variances of all 6 levels
2: I have no idea
3: The means of all 6 levels

Selection: 3

| Nice work!

|=====================================================                        |  69%

| Without an intercept (reference group) the tests are whether the expected counts
| (the groups means) are different from zero. Which spray has the least significant
| result?

1: sprayA
2: sprayF
3: sprayC
4: sprayB

Selection: 3

| That's a job well done!

|=======================================================                      |  72%

| Clearly, which level is first is important to the model. If you wanted a different
| reference group, for instance, to compare sprayB to sprayC, you could refit the
| model with a different reference group.

...

|==========================================================                   |  75%

| The R function relevel does precisely this. It re-orders the levels of a factor.
| We'll do this now. We'll call relevel with two arguments. The first is the factor,
| in this case InsectSprays$spray, and the second is the level that we want to be
| first, in this case "C". Store the result in a new variable spray2.

> spray2 <- relevel(InsectSprays$spray, "C")

| Nice work!

|============================================================                 |  78%

| Now generate a the new linear model and put the result in the variable fit2.

> fit2 <- lm(count~spray2, data=InsectSprays)

| Excellent job!

|===============================================================              |  81%

| As before, look at the coef portion of the summary of this new model fit2. See how
| sprayC is now the intercept (since it doesn't appear explicitly in the list).

> summary(fit2)$coef
Estimate Std. Error  t value     Pr(>|t|)
(Intercept)  2.083333   1.132156 1.840148 7.024334e-02
spray2A     12.416667   1.601110 7.755038 7.266893e-11
spray2B     13.250000   1.601110 8.275511 8.509776e-12
spray2D      2.833333   1.601110 1.769606 8.141205e-02
spray2E      1.416667   1.601110 0.884803 3.794750e-01
spray2F     14.583333   1.601110 9.108266 2.794343e-13

| You're the best!

|=================================================================            |  84%

| According to this new model what is the mean of spray2C?

1: 14.583333
2: 12.416667
3: The model doesn't tell me.
4: 2.083333

Selection: 4

| You got it right!

|===================================================================          |  88%

| Verify your answer with R's mean function using the array sC as the argument.

> mean(sC)
[1] 2.083333

| You're the best!

|======================================================================       |  91%

| According to this new model what is the mean of spray2A?

1: 12.416667
2: 14.50000
3: I don't have a clue
4: 14.583333

Selection: 2

| You are doing so well!

|========================================================================     |  94%

| Remember that with this model sprayC is the reference group, so the t-test
| statistics (shown in column 3 of the summary coefficients) compare the other sprays
| to sprayC. These can be computed by hand using the Estimates and standard error from
| the original model (fit) which used sprayA as the references.

...

|===========================================================================  |  97%

| The slides show the details of this but here we'll demonstrate by calculating the
| spray2B t value.  Subtract fit's sprayC coefficient (fit$coef[3]) from sprayB's
| (fit$coef[2]) and divide by the standard error which we saw was 1.6011. The result
| is spray2B's t value. Do this now.

> (fit$coef[3] - fit$coef[2]) / 1.6011
sprayC 
-8.275561 

| Nice try, but that's not exactly what I was hoping for. Try again. Or, type info()
| for more options.

| Type "(fit$coef[2]-fit$coef[3])/1.6011" at the R prompt.

> (fit$coef[2] - fit$coef[3]) / 1.6011
sprayB 
8.275561 

| You got it right!

|=============================================================================| 100%

| We glossed over some details in this lesson. For instance, counts can never be 0 so
| the assumption of normality is violated. We'll explore this issue more when we
| discuss Poisson GLMs. For now be glad that you've concluded this second lesson on
| multivariable linear models.

...

| You've reached the end of this lesson! Returning to the main menu...

| Please choose a course, or type 0 to exit swirl.

1: Regression Models
2: Take me to the swirl course repository!

Selection: 1

| Please choose a lesson, or type 0 to return to course menu.

1: Introduction
2: Residuals
3: Least Squares Estimation
4: Residual Variation
5: Introduction to Multivariable Regression
6: MultiVar Examples
7: MultiVar Examples2
8: MultiVar Examples3
9: Residuals Diagnostics and Variation
10: Variance Inflation Factors
11: Overfitting and Underfitting
12: Binary Outcomes
13: Count Outcomes

## 8

Selection: 8

| Attemping to load lesson dependencies...

| Package 'UsingR' loaded correctly!

| Package 'datasets' loaded correctly!

| Package 'stats' loaded correctly!

| Package 'graphics' loaded correctly!

|                                                                             |   0%

| MultiVar_Examples3. (Slides for this and other Data Science courses may be found at
| github https://github.com/DataScienceSpecialization/courses. If you care to use
| them, they must be downloaded as a zip file and viewed locally. This lesson
| corresponds to Regression_Models/02_02_multivariateExamples.)

...

|==                                                                           |   3%

| This is the third and final lesson in which we'll look at regression models with
| more than one independent variable or predictor. We'll begin with WHO hunger data
| which we've taken the liberty to load for you. WHO is the World Health Organization
| and this data concerns young children from around the world and rates of hunger
| among them which the organization compiled over a number of years. The original csv
| file was very large and we've subsetted just the rows which identify the gender of
| the child as either male or female. We've read the data into the data frame "hunger"
| for you, so you can easily access it.

...

|====                                                                         |   6%

| As we did in the last lesson let's first try to get a better understanding of the
| dataset. Use the R function dim to find the dimensions of hunger.

> dim(hunger)
[1] 948  13

| That's correct!

|======                                                                       |   8%

| How many samples does hunger have?

> 948
[1] 948

| Great job!

|=========                                                                    |  11%

| Now use the R function names to find out what the 13 columns of hunger represent.

> names(hunger)
[1] "X"              "Indicator"      "Data.Source"    "PUBLISH.STATES"
[5] "Year"           "WHO.region"     "Country"        "Sex"           
[9] "Display.Value"  "Numeric"        "Low"            "High"          
[13] "Comments"      

| You are really on a roll!

|===========                                                                  |  14%

| The Numeric column for a particular row tells us the percentage of children under
| age 5 who were underweight when that sample was taken. This is one of the columns
| we'll be focussing on in this lesson. It will be the outcome (dependent variable)
| for the models we generate.

...

|=============                                                                |  17%

| Let's first look at the rate of hunger and see how it's changed over time. Use the R
| function lm to generate the linear model in which the rate of hunger, Numeric,
| depends on the predictor, Year. Put the result in the variable fit.

> fit <- lm(Numeric ~ Year, hunger)

| You're the best!

|===============                                                              |  19%

| Now look at the coef portion of the summary of fit.

> summary(fit)$coef
Estimate  Std. Error   t value     Pr(>|t|)
(Intercept) 634.479660 121.1445995  5.237375 2.007699e-07
Year         -0.308397   0.0605292 -5.095012 4.209412e-07

| That's a job well done!

|=================                                                            |  22%

| What is the coefficient of hunger$Year?

1: 0.06053
2: -0.30840
3: 121.14460
4: 634.47966

Selection: 2

| That's correct!

|===================                                                          |  25%

| What does the negative Estimate of hunger$Year show?

1: I haven't a clue
2: As time goes on, the rate of hunger increases
3: As time goes on, the rate of hunger decreases

Selection: 3

| You got it!

|=====================                                                        |  28%

| What does the intercept of the model represent?

1: the number of children questioned in the survey
2: the percentage of hungry children at year 0
3: the number of hungry children at year 0

Selection: 2

| You nailed it! Good job!

|========================                                                     |  31%

| Now let's use R's subsetting capability to look at the rates of hunger for the
| different genders to see how, or even if, they differ.  Once again use the R
| function lm to generate the linear model in which the rate of hunger (Numeric) for
| female children depends on Year. Put the result in the variable lmF. You'll have to
| use the R construct x[hunger$Sex=="Female"] to pick out both the correct Numerics
| and the correct Years.

> fit <- lm(Numeric ~ Year, hunger[hunger$Sex=="Female",])

| You seem to have misspelled the model's name. I was expecting but you apparently
| typed .

| That's not the answer I was looking for, but try again. Or, type info() for more
| options.

| Type lmF <- lm(hunger$Numeric[hunger$Sex=="Female"] ~
| hunger$Year[hunger$Sex=="Female"]) at the R prompt or more simply lmF <-
| lm(Numeric[Sex=="Female"] ~ Year[Sex=="Female"],hunger)

> lmF <- lm(Numeric ~ Year, hunger[hunger$Sex=="Female",])

| That's not the answer I was looking for, but try again. Or, type info() for more
| options.

| Type lmF <- lm(hunger$Numeric[hunger$Sex=="Female"] ~
| hunger$Year[hunger$Sex=="Female"]) at the R prompt or more simply lmF <-
| lm(Numeric[Sex=="Female"] ~ Year[Sex=="Female"],hunger)

> 
> 
> lmF <- lm(Numeric[Sex=="Female"] ~ Year[Sex=="Female"],hunger)

| You nailed it! Good job!

|==========================                                                   |  33%

| Do the same for male children and put the result in lmM.

> lmF <- lm(Numeric[Sex=="Male"] ~ Year[Sex=="Male"], hunger)

| You seem to have misspelled the model's name. I was expecting but you apparently
| typed .

| That's not the answer I was looking for, but try again. Or, type info() for more
| options.

| Type lmM <- lm(hunger$Numeric[hunger$Sex=="Male"] ~ hunger$Year[hunger$Sex=="Male"])
| at the R prompt or more simply lmM <- lm(Numeric[Sex=="Male"] ~
| Year[Sex=="Male"],hunger)

> lmM <- lm(Numeric[Sex=="Male"] ~ Year[Sex=="Male"], hunger)

| Keep up the great work!

|============================                                                 |  36%

| Now we'll plot the data points and fitted lines using different colors to
| distinguish between males (blue) and females (pink).

...

|==============================                                               |  39%

| We can see from the plot that the lines are not exactly parallel. On the right side
| of the graph (around the year 2010) they are closer together than on the left side
| (around 1970). Since they aren't parallel, their slopes must be different, though
| both are negative. Of the following R expressions which would confirm that the slope
| for males is negative?

1: lmF$coef[2]
2: lmM$coef[2]
3: lmM$coef[1]

Selection: 
Enter an item from the menu, or 0 to exit
Selection: 2

| You got it right!

|================================                                             |  42%

| Now instead of separating the data by subsetting the samples by gender we'll use
| gender as another predictor to create the linear model lmBoth. Recall that to do
| this in R we place a plus sign "+" between the independent variables, so the formula
| looks like dependent ~ independent1 + independent2.

...

|==================================                                           |  44%

| Create lmBoth now. Numeric is the dependent, Year and Sex are the independent
| variables. The data is "hunger". For lmBoth, make sure Year is first and Sex is
| second.

> fit <- lm(Numeric ~ Year + Sex, hunger)

| You seem to have misspelled the model's name. I was expecting but you apparently
| typed .

| Keep trying! Or, type info() for more options.

| Type lmBoth <- lm(hunger$Numeric ~ hunger$Year + hunger$Sex) or more simply lmBoth
| <- lm(Numeric ~ Year+Sex,hunger)

> lmBoth <- lm(Numeric ~ Year + Sex, hunger)

| That's a job well done!

|====================================                                         |  47%

| Now look at the summary of lmBoth with the R command summary.

> summary(lmBoth)

Call:
lm(formula = Numeric ~ Year + Sex, data = hunger)

Residuals:
Min      1Q  Median      3Q     Max 
-25.472 -11.297  -1.848   7.058  45.990 

Coefficients:
Estimate Std. Error t value Pr(>|t|)    
(Intercept) 633.5283   120.8950   5.240 1.98e-07 ***
Year         -0.3084     0.0604  -5.106 3.99e-07 ***
SexMale       1.9027     0.8576   2.219   0.0267 *  
---
Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

Residual standard error: 13.2 on 945 degrees of freedom
Multiple R-squared:  0.03175,  Adjusted R-squared:  0.0297 
F-statistic: 15.49 on 2 and 945 DF,  p-value: 2.392e-07


| You're the best!

|======================================                                       |  50%

| Notice that three estimates are given, the intercept, one for Year and one for Male.
| What happened to the estimate for Female? Note that Male and Female are categorical
| variables hence they are factors in this model. Recall from the last lesson (and
| slides) that R treats the first (alphabetical) factor as the reference and its
| estimate is the intercept which represents the percentage of hungry females at year
| 0. The estimate given for the factor Male is a distance from the intercept (the
| estimate of the reference group Female). To calculate the percentage of hungry males
| at year 0 you have to add together the intercept and the male estimate given by the
| model.

...

|=========================================                                    |  53%

| What percentage of young Males were hungry at year 0?

1: 1.9027
2: 633.2199
3: 635.431
4: I can't tell since the data starts at 1970.

Selection: 3

| Nice work!

|===========================================                                  |  56%

| What does the estimate for hunger$Year represent?

1: the annual decrease in percentage of hungry males
2: the annual decrease in percentage of hungry females
3: the annual decrease in percentage of hungry children of both genders

Selection: 3

| You are amazing!

|=============================================                                |  58%

| Now we'll replot the data points along with two new lines using different colors.
| The red line will have the female intercept and the blue line will have the male
| intercept.

...

|===============================================                              |  61%

| The lines appear parallel. This is because

1: they have slopes that are very close
2: they have the same slope
3: I have no idea

Selection: 1

| Not exactly. Give it another go.

| By definition parallel lines have the same slope.

1: they have the same slope
2: they have slopes that are very close
3: I have no idea

Selection: 1

| You are doing so well!

|=================================================                            |  64%

| Now we'll consider the interaction between year and gender to see how that affects
| changes in rates of hunger. To do this we'll add a third term to the predictor
| portion of our model formula, the product of year and gender.

...

|===================================================                          |  67%

| Create the model lmInter. Numeric is the outcome and the three predictors are Year,
| Sex, and Sex*Year. The data is "hunger".

> lmInter <- lm(Numeric ~ Year + Sex + Sex*Year, hunger)

| Excellent job!

|=====================================================                        |  69%

| Now look at the summary of lmInter with the R command summary.

> summary(lmInter)

Call:
lm(formula = Numeric ~ Year + Sex + Sex * Year, data = hunger)

Residuals:
Min      1Q  Median      3Q     Max 
-25.913 -11.248  -1.853   7.087  46.146 

Coefficients:
Estimate Std. Error t value Pr(>|t|)    
(Intercept)  603.50580  171.05519   3.528 0.000439 ***
Year          -0.29340    0.08547  -3.433 0.000623 ***
SexMale       61.94772  241.90858   0.256 0.797946    
Year:SexMale  -0.03000    0.12087  -0.248 0.804022    
---
Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

Residual standard error: 13.21 on 944 degrees of freedom
Multiple R-squared:  0.03181,	Adjusted R-squared:  0.02874 
F-statistic: 10.34 on 3 and 944 DF,  p-value: 1.064e-06


| You are doing so well!

|========================================================                     |  72%

| What is the percentage of hungry females at year 0?

1: 61.94772
2: The model doesn't say.
3: 603.5058

Selection: 3

| Nice work!

|==========================================================                   |  75%

| What is the percentage of hungry males at year 0?

1: 61.94772
2: 603.5058
3: 665.4535
4: The model doesn't say.

Selection: 3

| You got it!

|============================================================                 |  78%

| What is the annual change in percentage of hungry females?

1: 0.08547
2: -0.03000
3: The model doesn't say.
4: -0.29340

Selection: 4

| You got it!

|==============================================================               |  81%

| What is the annual change in percentage of hungry males?

1: The model doesn't say.
2: -0.32340
3: 0.12087
4: -0.03000

Selection: 2

| You are doing so well!

|================================================================             |  83%

| Now we'll replot the data points along with two new lines using different colors to
| distinguish between the genders.

...

|==================================================================           |  86%

| Which line has the steeper slope?

1: Male
2: They look about the same
3: Female

Selection: 1

| That's correct!

|====================================================================         |  89%

| Finally, we note that things are a little trickier when we're dealing with an
| interaction between predictors which are continuous (and not factors). The slides
| show the underlying algebra, but we can summarize.

...

|=======================================================================      |  92%

| Suppose we have two interacting predictors and one of them is held constant. The
| expected change in the outcome for a unit change in the other predictor is the
| coefficient of that changing predictor + the coefficient of the interaction * the
| value of the predictor held constant.

...

|=========================================================================    |  94%

| Suppose the linear model is Hi = b0 + (b1*Ii) + (b2*Yi)+ (b3*Ii*Yi) + ei. Here the
| H's represent the outcomes, the I's and Y's the predictors, neither of which is a
| category, and the b's represent the estimated coefficients of the predictors. We can
| ignore the e's which represent the residuals of the model. This equation models a
| continuous interaction since neither I nor Y is a category or factor. Suppose we fix
| I at some value and let Y vary.

...

|===========================================================================  |  97%

| Which expression represents the change in H per unit change in Y given that I is
| fixed at 5?

1: b1+5*b3
2: b0+b2
3: b2+b3*5
4: b2+b3*Y

Selection: 4

| That's not exactly what I'm looking for. Try again.

| The expected change in the outcome is the estimate of the changing predictor (Y) +
| the estimate of the interaction (b3) * the value of the predictor held constant (5).

1: b0+b2
2: b1+5*b3
3: b2+b3*5
4: b2+b3*Y

Selection: 3

| You are really on a roll!

|=============================================================================| 100%

| Congratulations! You've finished this final lesson in multivariable regression
| models.

...

| You've reached the end of this lesson! Returning to the main menu...

| Please choose a course, or type 0 to exit swirl.

1: Regression Models
2: Take me to the swirl course repository!


## 9

fit <- lm(y ~ x, out2)
plot(fit, which=1)
fitno <- lm(y ~ x, out2[-1,])
plot(fitno, which=1)
coef(fit) - coef(fitno)
head(dfbeta(fit))
resno
resno <- out2[1, "y"] - predict(fitno, out2[1,])
1-resid(fit)[1]/resno
head(hatvalues(fit))
sigma <- sqrt(sum(resid(fit)^2)/df.residual(fit))
sigma <- sqrt(deviance(fit)/df.residual(fit))
rstd <- resid(fit) / (sigma*sqrt(1-hatvalues(fit)))
head(cbind(rstd, rstandard(fit)))
plot(fit, which=2)
sigma1 <- sqrt(deviance(fitno)/df.residual(fitno))
resid(fit)[1] / (sigma1*sqrt(1-hatvalues(fit)[1]))
rstudent(fit)[1]
head(rstudent(fit))
dy <- predict(fitno, out2) - predict(fit, out2)
sum(dy^2) / (2*sigma^2)
plot(fit, which=5)
head(swiss)
mdl <- lm(Fertility ~ ., data=swiss)
vif(mdl)
mdl2 <- lm(Fertility ~ .-Examination, data=swiss)
vif(mdl2)

## 10
Selection: 10

| Attemping to load lesson dependencies...

| Package 'car' loaded correctly!

|                                                                             |   0%

| Variance Inflation Factors. (Slides for this and other Data Science courses may be
| found at github https://github.com/DataScienceSpecialization/courses. If you care to
| use them, they must be downloaded as a zip file and viewed locally. This lesson
| corresponds to Regression_Models/02_04_residuals_variation_diagnostics.)

...

|===                                                                          |   4%

| In modeling, our interest lies in parsimonious, interpretable representations of the
| data that enhance our understanding of the phenomena under study. Omitting variables
| results in bias in the coefficients of interest - unless their regressors are
| uncorrelated with the omitted ones. On the other hand, including any new variables
| increases (actual, not estimated) standard errors of other regressors. So we don't
| want to idly throw variables into the model. This lesson is about the second of
| these two issues, which is known as variance inflation.

...

|=======                                                                      |   9%

| We shall use simulations to illustrate variance inflation. The source code for these
| simulations is in a file named vifSims.R which I have copied into your working
| directory and tried to display in your source code editor. If I've failed to display
| it, you should open it manually.

...

|==========                                                                   |  13%

| Find the function, makelms, at the top of vifSims.R. The final expression in makelms
| creates 3 linear models. The first, lm(y ~ x1), predicts y in terms of x1, the
| second predicts y in terms of x1 and x2, the third in terms of all three regressors.
| The second coefficient of each model, for instance coef(lm(y ~ x1))[2], is extracted
| and returned in a 3-long vector. What does this second coefficient represent?

1: The coefficient of x1.
2: The coefficient of the intercept.
3: The coefficient of x2.

Selection: 1

| That's correct!

|=============                                                                |  17%

| In makelms, the simulated dependent variable, y, depends on which of the regressors?

1: x1
2: x1, x2, and x3
3: x1 and x2

Selection: 1

| Excellent job!

|=================                                                            |  22%

| In vifSims.R, find the functions, rgp1() and rgp2(). Both functions generate 3
| regressors, x1, x2, and x3. Compare the lines following the comment Point A in
| rgp1() with those following Point C in rgp2(). Which of the following statements
| about x1, x2, and x3 is true?

1: x1, x2, and x3 are correlated in both rgp1() and rgp2().
2: x1, x2, and x3 are uncorrelated in rgp1(), but not in rgp2().
3: x1, x2, and x3 are correlated in rgp1(), but not in rgp1().
4: x1, x2, and x3 are uncorrelated in both rgp1() and rgp2().

Selection: 2

| You are amazing!

|====================                                                         |  26%

| In the line following Point B in rgp1(), the function maklms(x1, x2, x3) is applied
| 1000 times. Each time it is applied, it simulates a new dependent variable, y, and
| returns estimates of the coefficient of x1 for each of the 3 models, y ~ x1, y ~ x1
| + x2, and y ~ x1 + x2 + x3. It thus computes 1000 estimates of the 3 coefficients,
| collecting the results in 3x1000 array, beta. In the next line, the expression,
| apply(betas, 1, var), does which of the following?

1: Computes the variance of each column.
2: Computes the variance of each row.

Selection: 2

| You're the best!

|=======================                                                      |  30%

| The function rgp1() computes the variance in estimates of the coefficient of x1 in
| each of the three models, y ~ x1, y ~ x1 + x2, and y ~ x1 + x2 + x3. (The results
| are rounded to 5 decimal places for convenient viewing.) This simulation
| approximates the variance (i.e., squared standard error) of x1's coefficient in each
| of these three models. Recall that variance inflation is due to correlated
| regressors and that in rgp1() the regressors are uncorrelated. Run the simulation
| rgp1() now. Be patient. It takes a while.

> rgp1()
[1] "Processing. Please wait."
x1      x1      x1 
0.00110 0.00111 0.00112 

| You got it!

|===========================                                                  |  35%

| The variances in each of the three models are approximately equal, as expected,
| since the other regressors, x2 and x3, are uncorrelated with the regressor of
| interest, x1. However, in rgp2(), x2 and x3 both depend on x1, so we should expect
| an effect. From the expressions assigning x2 and x3 which follow Point C, which is
| more strongly correlated with x1?

1: x3
2: x2

Selection: 1

| You got it right!

|==============================                                               |  39%

| Run rgp2() to simulate standard errors in the coefficient of x1 for cases in which
| x1 is correlated with the other regressors

> rgp2()
[1] "Processing. Please wait."
x1      x1      x1 
0.00110 0.00240 0.00981 

| You got it!

|=================================                                            |  43%

| In this case, variance inflation due to correlated regressors is clear, and is most
| pronounced in the third model, y ~ x1 + x2 + x3, since x3 is the regressor most
| strongly correlated with x1.

...

|=====================================                                        |  48%

| In these two simulations we had 1000 samples of estimated coefficients, hence could
| calculate sample variance in order to illustrate the effect. In a real case, we have
| only one set of coefficients and we depend on theoretical estimates. However,
| theoretical estimates contain an unknown constant of proportionality. We therefore
| depend on ratios of theoretical estimates called Variance Inflation Factors, or
| VIFs.

...

|========================================                                     |  52%

| A variance inflation factor (VIF) is a ratio of estimated variances, the variance
| due to including the ith regressor, divided by that due to including a corresponding
| ideal regressor which is uncorrelated with the others. VIF's can be calculated
| directly, but the car package provides a convenient method for the purpose as we
| will illustrate using the Swiss data from the datasets package.

...

|============================================                                 |  57%

| According to its documentation, the Swiss data set consists of a standardized
| fertility measure and socioeconomic indicators for each of 47 French-speaking
| provinces of Switzerland in about 1888 when Swiss fertility rates began to fall.
| Type head(swiss) or View(swiss) to examine the data.

> head(swiss)
Fertility Agriculture Examination Education Catholic Infant.Mortality
Courtelary        80.2        17.0          15        12     9.96             22.2
Delemont          83.1        45.1           6         9    84.84             22.2
Franches-Mnt      92.5        39.7           5         5    93.40             20.2
Moutier           85.8        36.5          12         7    33.77             20.3
Neuveville        76.9        43.5          17        15     5.16             20.6
Porrentruy        76.1        35.3           9         7    90.57             26.6

| Nice work!

|===============================================                              |  61%

| Fertility was thought to depend on five socioeconomic factors: the percent of males
| working in Agriculture, the percent of draftees receiving the highest grade on the
| army's Examination, the percent of draftees with Education beyond primary school,
| the percent of the population which was Roman Catholic, and the rate of Infant
| Mortality in the province. Use linear regression to model Fertility in terms of
| these five regressors and an intercept. Store the model in a variable named mdl.

> mdl <- lm(Fertility ~ ., swiss)

| You are amazing!

|==================================================                           |  65%

| Calculate the VIF's for each of the regressors using vif(mdl).

> vif(mdl)
Agriculture      Examination        Education         Catholic Infant.Mortality 
2.284129         3.675420         2.774943         1.937160         1.107542 

| You got it right!

|======================================================                       |  70%

| These VIF's show, for each regression coefficient, the variance inflation due to
| including all the others. For instance, the variance in the estimated coefficient of
| Education is 2.774943 times what it might have been if Education were not correlated
| with the other regressors. Since Education and score on an Examination are likely to
| be correlated, we might guess that most of the variance inflation for Education is
| due to including Examination.

...

|=========================================================                    |  74%

| Make a second linear model of Fertility in which Examination is omitted, but the
| other four regressors are included. Store the result in a variable named mdl2.

> mdl2 <- lm(Fertility ~ .-Examination, swiss)

| You are quite good my friend!

|============================================================                 |  78%

| Calculate the VIF's for this model using vif(mdl2).

> vif(mdl2)
Agriculture        Education         Catholic Infant.Mortality 
2.147153         1.816361         1.299916         1.107528 

| Great job!

|================================================================             |  83%

| As expected, omitting Examination has markedly decreased the VIF for Education, from
| 2.774943 to 1.816361. Note that omitting Examination has had almost no effect the
| VIF for Infant Mortality. Chances are Examination and Infant Mortality are not
| strongly correlated. Now, before finishing this lesson, let's review several
| significant points.

...

|===================================================================          |  87%

| A VIF describes the increase in the variance of a coefficient due to the correlation
| of its regressor with the other regressors. What is the relationship of a VIF to the
| standard error of its coefficient?

1: They are the same.
2: There is no relationship.
3: VIF is the square of standard error inflation.

Selection: 3

| You are doing so well!

|======================================================================       |  91%

| If a regressor is strongly correlated with others, hence will increase their VIF's,
| why shouldn't we just exclude it?

1: We should never exclude anything.
2: We should always exclude it.
3: Excluding it might bias coefficient estimates of regressors with which it is correlated.

Selection: 3

| Nice work!

|==========================================================================   |  96%

| The problems of variance inflation and bias due to excluded regressors both involve
| correlated regressors. However there are methods, such as factor analysis or
| principal componenent analysis, which can convert regressors to an equivalent
| uncorrelated set. Why then, when modeling, should we not just use uncorrelated
| regressors and avoid all the trouble?

1: We should always use uncorrelated regressors.
2: Using converted regressors may make interpretation difficult.
3: Factor analysis takes too much computation.

Selection: 2

| You are really on a roll!

|=============================================================================| 100%

| That completes the exercise in variance inflation. The issue of omitting regressors
| is discussed in another lesson.


## 11
| Please choose a lesson, or type 0 to return to course menu.

 1: Introduction
2: Residuals
3: Least Squares Estimation
4: Residual Variation
5: Introduction to Multivariable Regression
6: MultiVar Examples
7: MultiVar Examples2
8: MultiVar Examples3
9: Residuals Diagnostics and Variation
10: Variance Inflation Factors
11: Overfitting and Underfitting
12: Binary Outcomes
13: Count Outcomes

Selection: 11

| Attemping to load lesson dependencies...

| Package 'car' loaded correctly!

|                                                                             |   0%

| Overfitting and Underfitting. (Slides for this and other Data Science courses may be
| found at github https://github.com/DataScienceSpecialization/courses. If you care to
| use them, they must be downloaded as a zip file and viewed locally. This lesson
| corresponds to Regression_Models/02_04_residuals_variation_diagnostics.)

...

|===                                                                          |   4%

| The Variance Inflation Factors lesson demonstrated that including new variables will
| increase standard errors of coefficient estimates of other, correlated regressors.
| Hence, we don't want to idly throw variables into the model. On the other hand,
| omitting variables results in bias in coefficients of regressors which are
| correlated with the omitted ones. In this lesson we demonstrate the effect of
| omitted variables and discuss the use of ANOVA to construct parsimonious,
| interpretable representations of the data.

...

|======                                                                       |   8%

| First, I would like to illustrate how omitting a correlated regressor can bias
| estimates of a coefficient. The relevant source code is in a file named fitting.R
| which I have copied into your working directory and tried to display in your source
| code editor. If I've failed to display it, you should open it manually.

...

|=========                                                                    |  12%

| Find the function simbias() at the top of fitting.R. Below the comment labeled Point
| A three regressors, x1, x2, and x3, are defined. Which of these two are correlated?

1: x1 and x2
2: x1 and x3
3: x2 and x3

Selection: 1

| Keep up the great work!

|============                                                                 |  15%

| Within simbias() another function, f(n), is defined. It forms a dependent variable,
| y, and at Point C returns the coefficient of x1 as estimated by two models, y ~ x1 +
| x2, and y ~ x1 + x3. One regressor is missing in each model. In the expression for y
| (Point B,) what is the actual coefficient of x1?

1: 1
2: 1/sqrt(2)
3: 0.3

Selection: 1

| Keep up the great work!

|===============                                                              |  19%

| At Point D in simbias() the internal function, f(), is applied 150 times and the
| results returned as a 2x150 matrix. The first row of this matrix contains
| independent estimates of x1's coefficient in the case that x3, the regressor
| uncorrelated with x1, is omitted. The second row contains estimates of x1's
| coefficient when the correlated regressor, x2, is omitted. Use simbias(), accepting
| the default argument, to form these estimates and store the result in a variable
| called x1c. (The default argument just guarantees a nice histogram, in a figure to
| follow.)

> x1c <- simbias()

| You are quite good my friend!

|==================                                                           |  23%

| The actual coefficient of x1 is 1. Having been warned that omitting a correlated
| regressor would bias estimates of x1's coefficient, we would expect the mean
| estimate of x1c's second row to be farther from 1 than the mean of x1c's second row.
| Using apply(x1c, 1, mean), find the means of each row.

> apply(x1c, 1, mean)
x1       x1 
1.034403 1.476944 

| Great job!

|=====================                                                        |  27%

| Histograms of estimates from x1c's first row (blue) and second row (red) are shown.
| Estimates from the second row are clearly more than two standard deviations from the
| correct value of 1, and the bias due to omitting the correlated regressor is
| evident. (The code which produced this figure is incidental to the lesson, but is
| available as the function x1hist(), at the bottom of fitting.R.)

...

|========================                                                     |  31%

| Adding even irrelevant regressors can cause a model to tend toward a perfect fit. We
| illustrate this by adding random regressors to the swiss data and regressing on
| progressively more of them. As the number of regressors approaches the number of
| data points (47), the residual sum of squares, also known as the deviance,
| approaches 0. (The source code for this figure can be found as function bogus() in
| fitting.R.

...

|===========================                                                  |  35%

| In the figure, adding random regressors decreased deviance, but we would be mistaken
| to believe that such decreases are significant. To assess significance, we should
| take into account that adding regressors reduces residual degrees of freedom.
| Analysis of variance (ANOVA) is a useful way to quantify the significance of
| additional regressors. To exemplify its use, we will use the swiss data.

...

|==============================                                               |  38%

| Recall that the Swiss data set consists of a standardized fertility measure and
| socioeconomic indicators for each of 47 French-speaking provinces of Switzerland in
| 1888. Fertility was thought to depend on an intercept and five factors denoted as
| Agriculture, Examination, Education, Catholic, and Infant Mortality. To begin our
| ANOVA example, regress Fertility on Agriculture and store the result in a variable
| named fit1.

> fit1 <- lm(Fertility~Agriculture, swiss)

| Keep up the great work!

|=================================                                            |  42%

| Create another model, named fit3, by regressing Fertility on Agriculture and two
| additonal regressors, Examination and Education.

> fit3 <- lm(Fertility~Agriculture+Examination+Education, swiss)

| Keep up the great work!

|====================================                                         |  46%

| We'll now use anova to assess the significance of the two added regressors. The null
| hypothesis is that the added regressors are not significant. We'll explain in detail
| shortly, but right now just apply the significance test by entering anova(fit1,
| fit3).

> anova(fit1, fit3)
Analysis of Variance Table

Model 1: Fertility ~ Agriculture
Model 2: Fertility ~ Agriculture + Examination + Education
Res.Df    RSS Df Sum of Sq      F    Pr(>F)    
1     45 6283.1                                  
2     43 3180.9  2    3102.2 20.968 4.407e-07 ***
---
Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

| You nailed it! Good job!

|======================================                                       |  50%

| The three asterisks, ***, at the lower right of the printed table indicate that the
| null hypothesis is rejected at the 0.001 level, so at least one of the two
| additional regressors is significant. Rejection is based on a right-tailed F test,
| Pr(>F), applied to an F value. According to the table, what is that F value?

1: 3102.2
2: 20.968
3: 45

Selection: 1

| Give it another try.

| It's the only number in the column labeled F in the printed table.

1: 45
2: 3102.2
3: 20.968

Selection: 3

| Nice work!

|=========================================                                    |  54%

| An F statistic is a ratio of two sums of squares divided by their respective degrees
| of freedom. If the two scaled sums are independent and centrally chi-squared
| distributed with the same variance, the statistic will have an F distribution with
| parameters given by the two degrees of freedom. In our case, the two sums are
| residual sums of squares which, as we know, have mean zero hence are centrally
| chi-squared provided the residuals themselves are normally distributed. The two
| relevant sums are given in the RSS (Residual Sum of Squares) column of the table.
| What are they?

1: 6283.1 and 3180.9
2: 45 and 43
3: 2 and 3102.2

Selection: 1

| Nice work!

|============================================                                 |  58%

| R's function, deviance(model), calculates the residual sum of squares, also known as
| the deviance, of the linear model given as its argument. Using deviance(fit3),
| verify that 3180.9 is fit3's residual sum of squares. (Of course, fit3 is called
| Model 2 in the table.)

> deviance(fit3)
[1] 3180.925

| Great job!

|===============================================                              |  62%

| In the next several steps, we will show how to calculate the F value, 20.968, which
| appears in the table printed by anova(). We'll begin with the denominator, which is
| fit3's residual sum of squares divided by its degrees of freedom. Fit3 has 43
| residual degrees of freedom. This figure is obtained by subtracting 4, the the
| number of fit3's predictors (the 3 named and the intercept,) from 47, the number of
| samples in swiss. Store the value of deviance(fit3)/43 in a variable named d.

> d<-deviance(fit3)/43

| You are really on a roll!

|==================================================                           |  65%

| The numerator is the difference, deviance(fit1)-deviance(fit3), divided by the
| difference in the residual degrees of freedom of fit1 and fit3, namely 2. This
| calculation requires some theoretical justification which we omit, but the essential
| idea is that fit3 has 2 predictors in addition to those of fit1. Calculate the
| numerator and store it in a variable named n.

> n<-deviance(fit1)-deviance(fit3)

| Keep trying! Or, type info() for more options.

| Enter n <- (deviance(fit1) - deviance(fit3))/2 at the R prompt.

> n<-(deviance(fit1)-deviance(fit3))/2

| You are doing so well!

|=====================================================                        |  69%

| Calculate the ratio, n/d, to show it is essentially equal to the F value, 20.968,
| given by anova().

> n/d
[1] 20.96783

| That's correct!

|========================================================                     |  73%

| We'll now calculate the p-value, which is the probability that a value of n/d or
| larger would be drawn from an F distribution which has parameters 2 and 43. This
| value was given as 4.407e-07 in the column labeled Pr(>F) in the table printed by
| anova(), a very unlikely value if the null hypothesis were true. Calculate this
| p-value using pf(n/d, 2, 43, lower.tail=FALSE).

> pf(n/d, 2, 43, lower.tail=FALSE)
[1] 4.406913e-07

| You are doing so well!

|===========================================================                  |  77%

| Based on the calculated p-value, a false rejection of the null hypothesis is
| extremely unlikely. We are confident that fit3 is significantly better than fit1,
| with one caveat: analysis of variance is sensitive to its assumption that model
| residuals are approximately normal. If they are not, we could get a small p-value
| for that reason. It is thus worth testing residuals for normality. The Shapiro-Wilk
| test is quick and easy in R. Normality is its null hypothesis. Use
| shapiro.test(fit3$residuals) to test the residual of fit3.

> shapiro.test(fit3$residuals) 

Shapiro-Wilk normality test

data:  fit3$residuals
W = 0.9728, p-value = 0.336


| You got it!

|==============================================================               |  81%

| The Shapiro-Wilk p-value of 0.336 fails to reject normality, supporting confidence
| in our analysis of variance. In order to illustrate the use of anova() with more
| than two models, I have constructed fit5 and fit6 using the first 5 and all 6
| regressors (including the intercept) respectively. Thus fit1, fit3, fit5, and fit6
| form a nested sequence of models; the regressors of one are included in those of the
| next. Enter anova(fit1, fit3, fit5, fit6) at the R prompt now to get the flavor.

> anova(fit1, fit3, fit5, fit6)
Analysis of Variance Table

Model 1: Fertility ~ Agriculture
Model 2: Fertility ~ Agriculture + Examination + Education
Model 3: Fertility ~ Agriculture + Examination + Education + Catholic
Model 4: Fertility ~ Agriculture + Examination + Education + Catholic + 
Infant.Mortality
Res.Df    RSS Df Sum of Sq       F    Pr(>F)    
1     45 6283.1                                   
2     43 3180.9  2   3102.19 30.2107 8.638e-09 ***
3     42 2513.8  1    667.13 12.9937 0.0008387 ***
4     41 2105.0  1    408.75  7.9612 0.0073357 ** 
---
Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

| You are quite good my friend!

|=================================================================            |  85%

| It appears that each model is a significant improvement on its predecessor. Before
| ending the lesson, let's review a few salient points.

...

|====================================================================         |  88%

| Omitting a regressor can bias estimation of the coefficient of certain other
| regressors. Which ones?

1: Uncorrelated regressors
2: Correlated regressors

Selection: 2

| That's correct!

|=======================================================================      |  92%

| Including more regressors will reduce a model's residual sum of squares, even if the
| new regressors are irrelevant. True or False?

1: True
2: False
3: It depends on circumstances.

Selection: 1

| Nice work!

|==========================================================================   |  96%

| When adding regressors, the reduction in residual sums of squares should be tested
| for significance above and beyond that of reducing residual degrees of freedom. R's
| anova() function uses an F-test for this purpose. What else should be done to insure
| that anova() applies?

1: Regressors should be tested for normality.
2: Model residuals should be tested for normality.
3: The residuals should be tested for having zero means.

Selection: 2

| You are doing so well!

  |=============================================================================| 100%

| That completes the lesson on underfitting and overfitting.


## 12
Selection: 12
  |                                                                             |   0%

| Binary Outcomes. (Slides for this and other Data Science courses may be found at
| github https://github.com/DataScienceSpecialization/courses. If you care to use
| them, they must be downloaded as a zip file and viewed locally. This lesson
| corresponds to Regression_Models/03_02_binaryOutcomes.)

...

|===                                                                          |   4%

| Frequently we care about outcomes that have two values such as alive or dead, win or
| lose, success or failure. Such outcomes are called binary, Bernoulli, or 0/1. A
| collection of exchangeable binary outcomes for the same covariate data are called
| binomial outcomes. (Outcomes are exchangeable if their order doesn't matter.)

...

|======                                                                       |   8%

| In this unit we will use glm() to model a process with a binary outcome and a
| continuous predictor. We will also learn how to interpret glm coefficients, and how
| to find confidence intervals. But first, let's discuss odds.

...

|=========                                                                    |  12%

| The Baltimore Ravens are a team in the American Football League. In post season
| (championship) play they win about 2/3 of their games. In other words, they win
| about twice as often as they lose. If I wanted to bet on them, I would have to offer
| 2-to-1 odds--if they lost I would pay you $2, but if they won you would pay me only
| $1. That way, in the long run over many bets, we'd both expect to win as much money
| as we'd lost.

...

|============                                                                 |  16%

| During the regular season the Ravens win about 55% of their games. What odds would I
| have to offer in the regular season?

1: Any of these
2: 11 to 9
3: 1.22222 to 1
4: 55 to 45

Selection: 4

| You nailed it! Good job!

|===============                                                              |  20%

| All of the answers are correct because they all represent the same ratio. If p is
| the probability of an event, the associated odds are p/(1-p).

...

|==================                                                           |  24%

| Now suppose we want to see how the Ravens' odds depends on their offense. In other
| words, we want to model how p, or some function of it, depends on how many points
| the Ravens are able to score. Of course, we can't observe p, we can only observe
| wins, losses, and the associated scores. Here is a Box plot of one season's worth of
| such observations.

...

|======================                                                       |  28%

| We can see that the Ravens tend to win more when they score more points. In fact,
| about 3/4 of their losses are at or below a certain score and about 3/4 of their
| wins are at or above it. What score am I talking about? (Remember that the purple
| boxes represent 50% of the samples, and the "T's" 25%.)

1: 23
2: 18
3: 30
4: 40

Selection: 1

| You are doing so well!

|=========================                                                    |  32%

| There were 9 games in which the Ravens scored 23 points or less. They won 4 of these
| games, so we might guess their probability of winning, given that they score 23
| points or less, is about 1/2.

...

|============================                                                 |  36%

| There were 11 games in which the Ravens scored 24 points or more. They won all but
| one of these. Verify this by checking the data yourself. It is in a data frame
| called ravenData. Look at it by typing either ravenData or View(ravenData).

> View(ravenData)

| Great job!

|===============================                                              |  40%

| We see a fairly rapid transition in the Ravens' win/loss record between 23 and 28
| points. At 23 points and below they win about half their games, between 24 and 28
| points they win 3 of 4, and above 28 points they win them all. From this, we get a
| very crude idea of the correspondence between points scored and the probability of a
| win. We get an S shaped curve, a graffiti S anyway.

...

|==================================                                           |  44%

| Of course, we would expect a real curve to be smoother. We would not, for instance,
| expect the Ravens to win half the games in which they scored zero points, nor to win
| all the games in which they scored more than 28. A generalized linear model which
| has these properties supposes that the log odds of a win depend linearly on the
| score. That is, log(p/(1-p)) = b0 + b1*score. The link function, log(p/(1-p)), is
| called the logit, and the process of finding the best b0 and b1, is called logistic
| regression.

...

|=====================================                                        |  48%

| The "best" b0 and b1 are those which maximize the likelihood of the actual win/loss
| record. Based on the score of a game, b0 and b1 give us a log odds, which we can
| convert to a probability, p, of a win. We would like p to be high for the scores of
| winning games, and low for the scores of losses.

...

|========================================                                     |  52%

| We can use R's glm() function to find the b0 and b1 which maximize the likelihood of
| our observations. Referring back to the data frame, we want to predict the binary
| outcomes, ravenWinNum, from the points scored, ravenScore. This corresponds to the
| formula, ravenWinNum ~ ravenScore, which is the first argument to glm. The second
| argument, family, describes the outcomes, which in our case are binomial. The third
| argument is the data, ravenData. Call glm with these parameters and store the result
| in a variable named mdl.

> mdl <- glm(ravenWinNum ~ ravenScore, family = 'binomial', data = ravenData)

| That's correct!
  
  |===========================================                                  |  56%

| The probabilities estimated by logistic regression using glm() are represented by
| the black curve. It is more reasonable than our crude estimate in several respects:
  | It increases smoothly with score, it estimates that 15 points give the Ravens a 50%
| chance of winning, that 28 points give them an 80% chance, and that 55 points make a
| win very likely (98%) but not absolutely certain.

...

|==============================================                               |  60%

| The model is less credible at scores lower than 9. Of course, there is no data in
| that region; the Ravens scored at least 9 points in every game. The model gives them
| a 33% chance of winning if they score 9 points, which may be reasonable, but it also
| gives them a 16% chance of winning even if they score no points! We can use R's
| predict() function to see the model's estimates for lower scores. The function will
| take mdl and a data frame of scores as arguments and will return log odds for the
| give scores. Call predict(mdl, data.frame(ravenScore=c(0, 3, 6)) and store the
| result in a variable called lodds.

> lodds <- predict(mdl, data.frame(ravenScore=c(0, 3, 6))
                   + )

| Nice work!
  
  |=================================================                            |  64%

| Since predict() gives us log odds, we will have to convert to probabilities. To
| convert log odds to probabilities use exp(lodds)/(1+exp(lodds)). Don't bother to
| store the result in a variable. We won't need it.

> exp(lodds)/(1+exp(lodds))
1         2         3 
0.1570943 0.2041977 0.2610505 

| Nice work!
  
  |====================================================                         |  68%

| As you can see, a person could make a lot of money betting against this model. When
| the Ravens score no points, the model might like 16 to 84 odds. As it turns out,
| though, the model is not that sure of itself. Typing summary(mdl) you can see the
| estimated coefficients are both within 2 standard errors of zero. Check out the
| summary now.

> summary(mdl)

Call:
  glm(formula = ravenWinNum ~ ravenScore, family = "binomial", 
      data = ravenData)

Deviance Residuals: 
  Min       1Q   Median       3Q      Max  
-1.7575  -1.0999   0.5305   0.8060   1.4947  

Coefficients:
  Estimate Std. Error z value Pr(>|z|)
(Intercept) -1.68001    1.55412  -1.081     0.28
ravenScore   0.10658    0.06674   1.597     0.11

(Dispersion parameter for binomial family taken to be 1)

Null deviance: 24.435  on 19  degrees of freedom
Residual deviance: 20.895  on 18  degrees of freedom
AIC: 24.895

Number of Fisher Scoring iterations: 5


| That's correct!

|=======================================================                      |  72%

| The coefficients estimate log odds as a linear function of points scored. They have
| a natural interpretation in terms of odds because, if b0 + b1*score estimates log
| odds, then exp(b0 + b1*score)=exp(b0)exp(b1*score) estimates odds. Thus exp(b0) is
| the odds of winning with a score of 0 (in our case 16/84,) and exp(b1) is the factor
| by which the odds of winning increase with every point scored. In our case exp(b1) =
| exp(0.10658) = 1.11. In other words, the odds of winning increase by 11% for each
| point scored.

...

|===========================================================                  |  76%

| However, the coefficients have relatively large standard errors. A 95% confidence
| interval is roughly 2 standard errors either side of a coefficient. R's function
| confint() will find the exact lower and upper bounds to the 95% confidence intervals
| for the coefficients b0 and b1. To get the corresponding intervals for exp(b0) and
| exp(b1) we would just exponentiate the output of confint(mdl). Do this now.

> confint(mdl)
Waiting for profiling to be done...
2.5 %    97.5 %
  (Intercept) -5.171690634 1.1334595
ravenScore  -0.003777464 0.2649023

| That's not exactly what I'm looking for. Try again. Or, type info() for more
| options.

| Just type exp(confint(mdl)).

> exp(confint(mdl))
Waiting for profiling to be done...
2.5 %   97.5 %
  (Intercept) 0.005674966 3.106384
ravenScore  0.996229662 1.303304

| You are amazing!
  
  |==============================================================               |  80%

| What is the 2.5% confidence bound on the odds of winning with a score of 0 points?

1: 0.996229662
2: 2.5%
3: 0.005674966

Selection: 3

| You got it!
  
  |=================================================================            |  84%

| The lower confidence bound on the odds of winning with a score of 0 is near zero,
| which seems much more realistic than the 16/84 figure of the maximum likelihood
| model. Now look at the lower bound on exp(b1), the exponentiated coefficient of
| ravenScore. How does it suggest the odds of winning will be affected by each
| additional point scored?

1: They will increase by 30%
2: They will decrease slightly
3: They will increase slightly

Selection: 1

| Not quite right, but keep trying.

| If you multiply a positive number by 0.996229662, do you increase or decrease the
| value?

1: They will decrease slightly
2: They will increase slightly
3: They will increase by 30%

Selection: 1

| Excellent job!
  
  |====================================================================         |  88%

| The lower confidence bound on exp(b1) suggests that the odds of winning would
| decrease slightly with every additional point scored. This is obviously unrealistic.
| Of course, confidence intervals are based on large sample assumptions and our sample
| consists of only 20 games. In fact, the GLM version of analysis of variance will
| show that if we ignore scores altogether, we don't do much worse.

...

|=======================================================================      |  92%

| Linear regression minimizes the squared difference between predicted and actual
| observations, i.e., minimizes the variance of the residual. If an additional
| predictor significantly reduces the residual's variance, the predictor is deemed
| important. Deviance extends this idea to generalized linear regression, using
| (negative) log likelihoods in place of variance. (For a detailed explanation, see
                                                    | the slides and lectures.) To see the analysis of deviance for our model, type
| anova(mdl).

> anova(mdl)
Analysis of Deviance Table

Model: binomial, link: logit

Response: ravenWinNum

Terms added sequentially (first to last)


Df Deviance Resid. Df Resid. Dev
NULL                          19     24.435
ravenScore  1   3.5398        18     20.895

| Excellent job!
  
  |==========================================================================   |  96%

| The value, 3.5398, labeled as the deviance of ravenScore, is actually the difference
| between the deviance of our model, which includes a slope, and that of a model which
| includes only an intercept, b0. This value is centrally chi-square distributed (for
                                                                                  | large samples) with 1 degree of freedom (2 parameters minus 1 parameter, or
                                                                                                                             | equivalently 19-18.) The null hypothesis is that the coefficient of ravenScore is
| zero. To confidently reject this hypothesis, we would want 3.5398 to be larger than
| the 95th percentile of chi-square distribution with one degree of freedom. Use
| qchisq(0.95, 1) to compute the threshold of this percentile.

> qchisq(0.95, 1)
[1] 3.841459

| Keep up the great work!
  
  |=============================================================================| 100%

| As you can see, 3.5398 is close to but less than the 95th percentile threshold,
| 3.841459, hence would be regarded as consistent with the null hypothesis at the
| conventional 5% level. In other words, ravenScore adds very little to a model which
| just guesses that the Ravens win with probability 70% (their actual record that
                                                         | season) or odds 7 to 3 is almost as good. If you like, you can verify this using
| mdl0 <- glm(ravenWinNum ~ 1, binomial, ravenData), but this concludes the Binary
| Outcomes example. Thank you.

mdl0 <- glm(ravenWinNum ~ 1, binomial, ravenData)

## 13

Selection: 13
|                                                                             |   0%

| Count Outcomes. (Slides for this and other Data Science courses may be found at
                   | github https://github.com/DataScienceSpecialization/courses. If you care to use
                   | them, they must be downloaded as a zip file and viewed locally. This lesson
                   | corresponds to Regression_Models/03_03_countOutcomes.)

...

|==                                                                           |   3%

| Many data take the form of counts. These might be calls to a call center, number of
| flu cases in an area, or number of cars that cross a bridge. Data may also be in the
| form of rates, e.g., percent of children passing a test. In this lesson we will use
| Poisson regression to analyze daily visits to a web site as the web site's
| popularity grows, and to analyze the percent of visits which are due to references
| from a different site.

...

|=====                                                                        |   6%

| Visits to a web site tend to occur independently, one at a time, at a certain
| average rate. The Poisson distribution describes random processes of this type. A
| Poisson process is characterized by a single parameter, the expected rate of
| occurrence, which is usually called lambda. In our case, lambda will be expected
| visits per day. Of course, as the web site becomes more popular, lambda will grow.
| In other words, our lambda will depend on time. We will use Poisson regression to
| model this dependence.

...

|=======                                                                      |  10%

| Somwhat remarkably, the variance of a Poisson process has the same value as its
| mean, lambda. You can quickly illustrate this by generating, say, n=1000 samples
| from a Poisson process using R's rpois(n, lambda) and calculating the sample
| variance. For example, type var(rpois(1000, 50)). The sample variance won't be
| exactly equal to the theoretical value, of course, but it will be fairly close.

> var(rpois(1000, 50))
[1] 48.13154

| Keep up the great work!

|==========                                                                   |  13%

| A famous theorem implies that properly normalized sums of independent, identically
| distributed random variables will tend to become normally distributed as the number
| of samples grows large. What is that theorem?

1: The Central Limit Theorem
2: The Gauss-Markov BLUE Theorem
3: The Pythagorean Theorem

Selection: 1

| You're the best!
  
  |============                                                                 |  16%

| The counts generated by a Poisson process are, strictly speaking, slightly different
| than the normalized sums of the Central Limit Theorem. However, the counts in a
| given period of time will represent sums of larger numbers of terms as lambda
| increases. In fact, it can be formally shown that for large lambda a Poisson
| distribution is well approximated by a normal. The figure illustrates this effect.
| It shows progression from a sparse, asymetric, Poisson probability mass function on
| the left, to a dense, bell-shaped curve on the right as lambda varies from 2 to 100.

...

|===============                                                              |  19%

| In a Poisson regression, the log of lambda is assumed to be a linear function of the
| predictors. Since we will try to model the growth of visits to a web site, the log
| of lambda will be a linear function the date: log(lambda) = b0 + b1*date. This
| implies that the average number of hits per day, lambda, is exponential in the date:
  | lambda = exp(b0)*exp(b1)^date. Exponential growth is also suggested by the smooth,
| black curve drawn though the data. Thus exp(b1) would represent the percentage by
| which visits grow per day.

...

|=================                                                            |  23%

| If you are connected to the internet right now, would you care to visit the Leek
| Group website?

Yes or No? Yes

| Type nxt() to continue
> nxt()

| Resuming lesson...

|====================                                                         |  26%

| Our data is in a data frame named hits. Use View(hits), head(hits), or tail(hits) to
| examine the data now.

> head(hits)
date visits simplystats
1 2011-01-01      0           0
2 2011-01-02      0           0
3 2011-01-03      0           0
4 2011-01-04      0           0
5 2011-01-05      0           0
6 2011-01-06      0           0

| Excellent job!
  
  |======================                                                       |  29%

| There are three columns of data labeled date, visits, and simplystats respectively.
| The simplystats column records the number of visits which are due to references from
| another site, the Simply Statistics blog. We'll come back to that column later. For
| now, we are interested in the date and visits columns. The date will be our
| predictor.

...

|=========================                                                    |  32%

| Our dates are represented in terms of R's class, Date. Verify this by typing
| class(hits[,'date']), or something equivalent.

> class(hits[,'date'])
[1] "Date"

| Keep up the great work!
  
  |===========================                                                  |  35%

| R's Date class represents dates as days since or prior to January 1, 1970. They are
| essentially numbers, and to some extent can be treated as such. Dates can, for
| example, be added or subtracted, or easily coverted to numbers. Type
| as.integer(head(hits[,'date'])) to see what I mean.

> as.integer(head(hits[,'date']))
[1] 14975 14976 14977 14978 14979 14980

| That's a job well done!
  
  |==============================                                               |  39%

| The arithmetic properties of Dates allow us to use them as predictors. We'll use
| Poisson regression to predict log(lambda) as a linear function of date in a way
| which maximizes the likelihood of the counts we actually see. Our formula will be
| visits ~ date. Since our outcomes (visits) are counts, our family will be 'poisson',
| and our third argument will be the data, hits. Create such a model and store it in a
| variable called mdl using the following expression or something equivalent, mdl <-
| glm(visits ~ date, poisson, hits).

> mdl <-
+     | glm(visits ~ date, poisson, hits)
Error: unexpected '|' in:
"mdl <-
|"
> mdl <- glm(visits ~ date, poisson, hits)

| Excellent job!

|================================                                             |  42%

| The figure suggests that our Poisson regression fits the data very well. The black
| line is the estimated lambda, or mean number of visits per day. We see that mean
| visits per day increased from around 5 in early 2011 to around 10 by 2012, and to
| around 20 by late 2013. It is approximately doubling every year.

...

|===================================                                          |  45%

| Type summary(mdl) to examine the estimated coefficients and their significance.

> summary(mdl)

Call:
glm(formula = visits ~ date, family = poisson, data = hits)

Deviance Residuals: 
Min       1Q   Median       3Q      Max  
-5.0466  -1.5908  -0.3198   0.9128  10.6545  

Coefficients:
Estimate Std. Error z value Pr(>|z|)    
(Intercept) -3.275e+01  8.130e-01  -40.28   <2e-16 ***
date         2.293e-03  5.266e-05   43.55   <2e-16 ***
---
Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

(Dispersion parameter for poisson family taken to be 1)

Null deviance: 5150.0  on 730  degrees of freedom
Residual deviance: 3121.6  on 729  degrees of freedom
AIC: 6069.6

Number of Fisher Scoring iterations: 5


| You are doing so well!

|=====================================                                        |  48%

| Both coefficients are significant, being far more than two standard errors from
| zero. The Residual deviance is also very significantly less than the Null,
| indicating a strong effect. (Recall that the difference between Null and Residual
| deviance is approximately chi-square with 1 degree of freedom.) The Intercept
| coefficient, b0, just represents log average hits on R's Date 0, namely January 1,
| 1970. We will ignore it and focus on the coefficient of date, b1, since exp(b1) will
| estimate the percentage at which average visits increase per day of the site's life.

...

|========================================                                     |  52%

| Get the 95% confidence interval for exp(b1) by exponentiating confint(mdl, 'date')

> confint(mdl, 'date')
Waiting for profiling to be done...
2.5 %      97.5 % 
0.002190043 0.002396461 

| Not quite! Try again. Or, type info() for more options.

| Just type exp(confint(mdl, 'date')) or exp(confint(mdl, 2)).

> exp(confint(mdl, 'date'))
Waiting for profiling to be done...
2.5 %   97.5 % 
1.002192 1.002399 

| You are quite good my friend!

|==========================================                                   |  55%

| Visits are estimated to increase by a factor of between 1.002192 and 1.002399 per
| day. That is, between 0.2192% and 0.2399% per day. This actually represents more
| than a doubling every year.

...

|=============================================                                |  58%

| Our model looks like a pretty good description of the data, but no model is perfect
| and we can often learn about a data generation process by looking for a model's
| shortcomings. As shown in the figure, one thing about our model is 'zero inflation'
| in the first two weeks of January 2011, before the site had any visits. The model
| systematically overestimates the number of visits during this time. A less obvious
| thing is that the standard deviation of the data may be increasing with lambda
| faster than a Poisson model allows. This possibility can be seen in the rightmost
| plot by visually comparing the spread of green dots with the standard deviation
| predicted by the model (black dashes.) Also, there are four or five bursts of
| popularity during which the number of visits far exceeds two standard deviations
| over average. Perhaps these are due to mentions on another site.

...

|===============================================                              |  61%

| It seems that at least some of them are. The simplystats column of our data records
| the number of visits to the Leek Group site which come from the related site, Simply
| Statistics. (I.e., visits due to clicks on a link to the Leek Group which appeared
               | in a Simply Statisics post.)

...

|==================================================                           |  65%

| In the figure, the maximum number of visits occurred in late 2012. Visits from the
| Simply Statistics blog were also at their maximum that day. To find the exact date
| we can use which.max(hits[,'visits']. Do this now.
                       
                       > which.max(hits[,'visits'])
                       [1] 704
                       
                       | You are doing so well!
                         
                         |====================================================                         |  68%
                       
                       | The maximum number of visits is recorded in row 704 of our data frame. Print that
                       | row by typing hits[704,].
                       
                       > hits[704,]
                       date visits simplystats
                       704 2012-12-04     94          64
                       
                       | You are quite good my friend!
                         
                         |=======================================================                      |  71%
                       
                       | The maximum number of visits, 94, occurred on December 4, 2012, of which 64 came
                       | from the Simply Statistics blog. We might consider the 64 visits to be a special
                       | event, over and above normal. Can the difference, 94-64=30 visits, be attributed to
                       | normal traffic as estimated by our model? To check, we will need the value of lambda
                       | on December 4, 2012. This will be entry 704 of the fitted.values element of our
                       | model. Extract mdl$fitted.values[704] and store it in a variable named lambda.
                       
                       > lambda <- mdl$fitted.values[704]
                       
                       | You got it right!
                         
                         |=========================================================                    |  74%
                       
                       | The number of visits explained by our model on December 4, 2012 are those of a
                       | Poisson random variable with mean lambda. We can find the 95th percentile of this
                       | distribution using qpois(.95, lambda). Try this now.
                       
                       > qpois(.95, lambda)
                       [1] 33
                       
                       | You are really on a roll!
                         
                         |============================================================                 |  77%
                       
                       | So, 95% of the time we would see 33 or fewer visits, hence 30 visits would not be
                       | rare according to our model. It would seem that on December 4, 2012, the very high
                       | number of visits was due to references from Simply Statistics. To gauge the
                       | importance of references from Simply Statistics we may wish to model the proportion
                       | of traffic such references represent. Doing so will also illustrate the use of glm's
                       | parameter, offset, to model frequencies and proportions.
                       
                       ...
                       
                       |==============================================================               |  81%
                       
                       | A Poisson process generates counts, and counts are whole numbers, 0, 1, 2, 3, etc. A
                       | proportion is a fraction. So how can a Poisson process model a proportion? The trick
                       | is to include the denominator of the fraction, or more precisely its log, as an
                       | offset. Recall that in our data set, 'simplystats' is the visits from Simply
                       | Statistics, and 'visits' is the total number of visits. We would like to model the
                       | fraction simplystats/visits, but to avoid division by zero we'll actually use
                       | simplystats/(visits+1). A Poisson model assumes that log(lambda) is a linear
                       | combination of predictors. Suppose we assume that log(lambda) = log(visits+1) + b0 +
                         | b1*date. In other words, if we insist that the coefficient of log(visits+1) be equal
                       | to 1, we are predicting the log of mean visits from Simply Statistics as a
                       | proportion of total visits: log(lambda/(visits+1)) = b0 + b1*date.
                       
                       ...
                       
                       |=================================================================            |  84%
                       
                       | glm's parameter, offset, has precisely this effect. It fixes the coefficient of the
                       | offset to 1. To create a model for the proportion of visits from Simply Statistics,
                       | we let offset=log(visits+1). Create such a Poisson model now and store it as a
                       | variable called mdl2.
                       
                       > mdl2 <- glm(visits ~ date, poisson, hits, offset=log(visits+1))
                       
                       | Give it another try. Or, type info() for more options.
                       
                       | Enter mdl2 <- glm(formula = simplystats ~ date, family = poisson, data = hits,
                       | offset = log(visits + 1)), or something equivalent.
                       
                       > mdl2 <- glm(simplystats ~ date, poisson, hits, offset=log(visits+1))
                       
                       | That's a job well done!
                         
                         |===================================================================          |  87%
                       
                       | Although summary(mdl2) will show that the estimated coefficients are significantly
                       | different than zero, the model is actually not impressive. We can illustrate why by
                       | looking at December 4, 2012, once again. On that day there were 64 actual visits
                       | from Simply Statistics. However, according to mdl2, 64 visits would be extremely
                       | unlikely. You can verify this weakness in the model by finding mdl2's 95th
                       | percentile for that day. Recalling that December 4, 2012 was sample 704, find
                       | qpois(.95, mdl2$fitted.values[704]).
                       
                       > qpois(.95, mdl2$fitted.values[704])
                       [1] 47
                       
                       | That's correct!
                         
                         |======================================================================       |  90%
                       
                       | A Poisson distribution with lambda=1000 will be well approximated by a normal
                       | distribution. What will be the variance of that normal distribution?
                       
                       1: lambda
                       2: lambda squared
                       3: the square root of lambda.
                       
                       Selection: 1
                       
                       | That's a job well done!
                       
                       |========================================================================     |  94%
                       
                       | When modeling count outcomes as a Poisson process, what is modeled as a linear
                       | combination of the predictors?
                       
                       1: The log of the mean
                       2: The counts
                       3: The mean
                       
                       Selection: 1
                       
                       | Nice work!
                       
                       |===========================================================================  |  97%
                       
                       | What parameter of the glm function allows you to include a predictor whose
                       | coefficient is fixed to the value 1?
                       
                       1: offset
                       2: b0
                       3: family
                       4: data
                       5: formula
                       
                       Selection: 1
                       
                       | That's a job well done!
                         
                         |=============================================================================| 100%
                       
                       | That completes the Poisson GLM example. Thanks for sticking with it. I hope we've
                       | made it count.
                       
                       ...
                       
                       | Are you currently enrolled in the Coursera course associated with this lesson?
                       
                       1: Yes
                       2: No
                       
                       Selection: 1
                       
                       | Would you like me to notify Coursera that you've completed this lesson? If so, I'll
                       | need to get some more info from you.
                       
                       1: Yes
                       2: No
                       3: Maybe later
                       
                       Selection: 1
                       
                       | Is the following information correct?
                       
                       Course ID: regmods-002
                       Submission login (email): sandipan.dey@gmail.com
                       Submission password: P7N3y8jkyC
                       
                       1: Yes, go ahead!
                       2: No, I need to change something.
                       
                       Selection: 1
                       
                       | I'll try to tell Coursera you've completed this lesson now.
                       
                       | Great work!