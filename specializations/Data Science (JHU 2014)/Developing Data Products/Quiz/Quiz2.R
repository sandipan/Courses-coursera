library(devtools)
library(slidify)
setwd("C:/Users/SANDIPAN DEY/Desktop/coursera/Developing Data Products/project")
author("test_deck")
slidify("index.Rmd")
browseURL("index.html")
#publish_github("sandipan", "slidify")

```{r, echo=FALSE}
fit <- lm(y ~ x1 + x2 + x3)
summary(fit)
```

```{r, results=hide'}
fit <- lm(y ~ x1 + x2 + x3)
summary(fit)
```
