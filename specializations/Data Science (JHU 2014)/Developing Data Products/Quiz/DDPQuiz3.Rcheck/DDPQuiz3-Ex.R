pkgname <- "DDPQuiz3"
source(file.path(R.home("share"), "R", "examples-header.R"))
options(warn = 1)
options(pager = "console")
library('DDPQuiz3')

base::assign(".oldSearch", base::search(), pos = 'CheckExEnv')
cleanEx()
nameEx("createmean")
### * createmean

flush(stderr()); flush(stdout())

### Name: createmean
### Title: This function calculates the mean
### Aliases: createmean

### ** Examples

x <- 1:10
createmean(x)



### * <FOOTER>
###
options(digits = 7L)
base::cat("Time elapsed: ", proc.time() - base::get("ptime", pos = 'CheckExEnv'),"\n")
grDevices::dev.off()
###
### Local variables: ***
### mode: outline-minor ***
### outline-regexp: "\\(> \\)?### [*]+" ***
### End: ***
quit('no')
