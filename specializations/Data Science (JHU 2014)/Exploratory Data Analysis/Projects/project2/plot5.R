# read the RDS files
NEI <- readRDS("summarySCC_PM25.rds")
SCC <- readRDS("Source_Classification_Code.rds")

NEIBaltimore <- subset(NEI, fips == "24510")
NEIBSCC <- merge(NEIBaltimore, SCC, by.x="SCC", by.y="SCC")
#sort(unique(NEIBSCC$Short.Name))
NEIBSCC <- NEIBSCC[NEIBSCC$Short.Name %in% grep("Vehicle", unique(NEIBSCC$Short.Name), value=TRUE),]
 
summaryEmissions <- tapply(NEIBSCC$Emissions, NEIBSCC$year, sum)
# plot
png(filename = "plot5.png", width = 480, height = 480)
barplot(summaryEmissions, col = 2*summaryEmissions/10, border = "dark blue", density = 5*summaryEmissions/10)
lines(summaryEmissions / 2, lty=2)
points(summaryEmissions / 2)
title("Emissions from Vehicle sources at Baltimore", xlab="Year", ylab="Emissions")
dev.off()

NEIBSCC <- merge(NEIBaltimore, SCC, by.x="SCC", by.y="SCC")
#sort(unique(NEIBSCC$Short.Name))
NEIBSCC <- NEIBSCC[NEIBSCC$Short.Name %in% grep("Motor Vehicle", unique(NEIBSCC$Short.Name), value=TRUE),]
 
summaryEmissions <- tapply(NEIBSCC$Emissions, NEIBSCC$year, sum)
# plot
png(filename = "plot5.1.png", width = 480, height = 480)
barplot(summaryEmissions, col = 2*summaryEmissions/10, border = "dark blue", density = 5*summaryEmissions/10)
lines(summaryEmissions / 2, lty=2)
points(summaryEmissions / 2)
title("Emissions from Motor Vehicle sources at Baltimore", xlab="Year", ylab="Emissions")
dev.off()