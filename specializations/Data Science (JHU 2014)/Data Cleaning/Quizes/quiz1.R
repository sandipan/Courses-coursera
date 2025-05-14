setwd("E:/Academics/Johns Hopkins/Data Cleaning/")
d <- read.csv("getdata-data-ss06hid.csv")
names(d)
head(d)
unique(d$VAL)
length(d[!is.na(d$VAL) & d$VAL >= 24,]$VAL) #  >= $1000000
#d$FES
#install.packages('XLConnect')
#library(XLConnect)
#d <- readWorksheetFromFile("getdata-data-DATA.gov_NGAP.xslx", sheet=1)
install.packages('xlsx')
library(xlsx)
dat <- read.xlsx("getdata-data-DATA.gov_NGAP.xlsx", sheetIndex = 1, rowIndex = 18:23, colIndex = 7:15)
sum(dat$Zip*dat$Ext,na.rm=T)
require(XML)
d <- xmlParse("getdata-data-restaurants.xml")
xml_data <- xmlToList(d)
count <- 0
for (i in 1:length(xml_data$row)) {
	if (xml_data$row[[i]]$zipcode == 21231) {
		count <- count + 1
	}
}
print(count)
#xmldf <- do.call("rbind", lapply(xml_data$row, as.data.frame))
#nrow(subset(xmldf, zipcode==21231))
#head(xmldf)
require(data.table)
system.time(DT <- fread("getdata-data-ss06pid.csv"))
system.time(sapply(split(DT$pwgtp15,DT$SEX),mean))
system.time(tapply(DT$pwgtp15,DT$SEX,mean))
system.time(DT[,mean(pwgtp15),by=SEX])
#mean(DT$pwgtp15,by=DT$SEX)
