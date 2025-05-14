# read the RDS files
NEI <- readRDS("summarySCC_PM25.rds")
SCC <- readRDS("Source_Classification_Code.rds")

NEIBaltimore <- subset(NEI, fips == "24510")
NEILosAngeles <- subset(NEI, fips == "06037")
NEIBSCC <- merge(NEIBaltimore, SCC, by.x="SCC", by.y="SCC")
NEIBSCC <- NEIBSCC[NEIBSCC$Short.Name %in% grep("Vehicle", unique(NEIBSCC$Short.Name), value=TRUE),]
NEILSCC <- merge(NEILosAngeles, SCC, by.x="SCC", by.y="SCC")
NEILSCC <- NEILSCC[NEILSCC$Short.Name %in% grep("Vehicle", unique(NEILSCC$Short.Name), value=TRUE),]

summaryBEmissions <- tapply(NEIBSCC$Emissions, NEIBSCC$year, sum)
summaryLEmissions <- tapply(NEILSCC$Emissions, NEILSCC$year, sum)
# plot
png(filename = "plot6.png", width = 480, height = 480)
height <- rbind(summaryBEmissions, summaryLEmissions)
mp <- barplot(height, ylim = c(0, max(height)+100), names.arg = names(height), col=c("darkblue","red"), density = c(50, 50), beside = TRUE)
text(mp, height, labels = format(round(height,2), 4), pos = 3, cex = .7)
legend("topright", legend = c("Baltimore", "Los Angeles"),  fill = c("darkblue", "red"), density = c(50, 50))
title("Emissions from Vehicle sources at Baltimore", xlab="Year", ylab="Emissions")
dev.off()

NEIBaltimore <- subset(NEI, fips == "24510")
NEILosAngeles <- subset(NEI, fips == "06037")
NEIBSCC <- merge(NEIBaltimore, SCC, by.x="SCC", by.y="SCC")
NEIBSCC <- NEIBSCC[NEIBSCC$Short.Name %in% grep("Motor Vehicle", unique(NEIBSCC$Short.Name), value=TRUE),]
NEILSCC <- merge(NEILosAngeles, SCC, by.x="SCC", by.y="SCC")
NEILSCC <- NEILSCC[NEILSCC$Short.Name %in% grep("Motor Vehicle", unique(NEILSCC$Short.Name), value=TRUE),]

summaryBEmissions <- NULL
summaryBEmissions[c('1999', '2002', '2005', '2008')] <- 0
tmp <- tapply(NEIBSCC$Emissions, NEIBSCC$year, sum)
summaryBEmissions[names(tmp)] <- tmp
summaryBEmissions['2008'] <- 0
summaryLEmissions <- tapply(NEILSCC$Emissions, NEILSCC$year, sum)
# plot
png(filename = "plot6.1.png", width = 480, height = 480)
height <- rbind(summaryBEmissions, summaryLEmissions)
mp <- barplot(height, ylim = c(0, max(height)+100), names.arg = names(height), col=c("darkblue","red"), density = c(50, 50), beside = TRUE)
text(mp, height, labels = format(round(height,2), 4), pos = 3, cex = .7)
legend("topright", legend = c("Baltimore", "Los Angeles"),  fill = c("darkblue", "red"), density = c(50, 50))
title("Emissions from Motor Vehicle sources at Baltimore", xlab="Year", ylab="Emissions")
dev.off()