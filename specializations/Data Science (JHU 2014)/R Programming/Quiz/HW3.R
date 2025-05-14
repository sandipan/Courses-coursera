setwd("E:/Academics/Coursera/R Programming")
outcome <- read.csv("data3/outcome-of-care-measures.csv", colClasses = "character")
head(outcome)
ncol(outcome)
nrow(outcome)
names(outcome)
outcome[, 11] <- as.numeric(outcome[, 11])
## You may get a warning about NAs being introduced; that is okay
hist(outcome[, 11])
source("best.R")
best("TX", "heart attack")
# "CYPRESS FAIRBANKS MEDICAL CENTER"
best("TX", "heart failure")
# "FORT DUNCAN MEDICAL CENTER"
best("MD", "heart attack")
# "JOHNS HOPKINS HOSPITAL, THE"
best("MD", "pneumonia")
# "GREATER BALTIMORE MEDICAL CENTER"
best("BB", "heart attack")
# Error in best("BB", "heart attack") : invalid state
best("NY", "hert attack")
# Error in best("NY", "hert attack") : invalid outcome
source("rankhospital.R")
rankhospital("TX", "heart failure", 4)
# "DETAR HOSPITAL NAVARRO"
rankhospital("MD", "heart attack", "worst")
# "HARFORD MEMORIAL HOSPITAL"
rankhospital("MN", "heart attack", 5000)
# NA
source("rankall.R")
head(rankall("heart attack", 20), 10)
#hospital state
#AK <NA> AK
#AL D W MCMILLAN MEMORIAL HOSPITAL AL
#AR ARKANSAS METHODIST MEDICAL CENTER AR
#AZ JOHN C LINCOLN DEER VALLEY HOSPITAL AZ
#CA SHERMAN OAKS HOSPITAL CA
#CO SKY RIDGE MEDICAL CENTER CO
#CT MIDSTATE MEDICAL CENTER CT
#DC <NA> DC
#DE <NA> DE
#FL SOUTH FLORIDA BAPTIST HOSPITAL FL
tail(rankall("pneumonia", "worst"), 3)
#hospital state
#WI MAYO CLINIC HEALTH SYSTEM - NORTHLAND, INC WI
#WV PLATEAU MEDICAL CENTER WV
#WY NORTH BIG HORN HOSPITAL DISTRICT WY
tail(rankall("heart failure"), 10)
#hospital state
#TN WELLMONT HAWKINS COUNTY MEMORIAL HOSPITAL TN
#TX FORT DUNCAN MEDICAL CENTER TX
#UT VA SALT LAKE CITY HEALTHCARE - GEORGE E. WAHLEN VA MEDICAL CENTER UT
#VA SENTARA POTOMAC HOSPITAL VA
#VI GOV JUAN F LUIS HOSPITAL & MEDICAL CTR VI
#VT SPRINGFIELD HOSPITAL VT
#WA HARBORVIEW MEDICAL CENTER WA
#WI AURORA ST LUKES MEDICAL CENTER WI
#WV FAIRMONT GENERAL HOSPITAL WV
#WY CHEYENNE VA MEDICAL CENTER WY



AkhW2vZGyf


#test <- function(n) {
#	sys.call()
#}