setwd("E:/Academics/Coursera/Data Cleaning/")

dfm <- read.csv("getdata-data-ss06hid.csv")
sort(names(dfm))
#head(dfm)
strsplit(names(dfm), split="wgtp")[[123]]

dfm <- read.csv("getdata-data-GDP.csv")
names(dfm)
head(dfm)
mean(as.integer(gsub(',', '', dfm$millions.of.US.dollars[1:190])))

with(dfm, grep("^United", countryNames))
sum(with(dfm, grepl("^United", countryNames)))
#by(mydata, mydatat$byvar, function(x) mean(x))

dfmedu <- read.csv("getdata-data-EDSTATS_Country.csv")
names(dfmedu)
head(dfmedu)

dfmm <- merge(dfm, dfmedu, by.x="Country", by.y="CountryCode")
names(dfmm)
head(dfmm)
dfmm$Special.Notes[grepl("Fiscal year end: June", dfmm$Special.Notes)]
sum(grepl("Fiscal year end: June", dfmm$Special.Notes))

library(quantmod)
amzn = getSymbols("AMZN",auto.assign=FALSE)
sampleTimes = index(amzn) 
names(amzn)
head(amzn)
dates <- index(amzn)
format(dates,"%b")
format(dates,"%Y")
#as.POSIXlt(dates)$mday
cbind(.indexyear(amzn), format(dates,"%Y"))
amzn[.indexyear(amzn)==112,] # == amzn[format(index(amzn),"%Y") == "2012",]
amzn[.indexwday(amzn)==1 & .indexyear(amzn)==112,]
nrow(amzn[format(index(amzn),"%Y") == "2012",])
nrow(amzn[.indexyear(amzn)==112,])
nrow(amzn[.indexwday(amzn)==1 & .indexyear(amzn)==112,])
#getSymbols("SPY")
#SPY[.indexmon(SPY)==0]   # January for all years (note zero-based indexing!)
#SPY[.indexmday(SPY)==1]  # The first of every month
#SPY[.indexwday(SPY)==1]  # All Mondays