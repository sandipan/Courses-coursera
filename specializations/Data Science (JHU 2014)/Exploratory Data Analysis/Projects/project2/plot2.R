# read the RDS files
NEI <- readRDS("summarySCC_PM25.rds")
SCC <- readRDS("Source_Classification_Code.rds")

# yearwise emission at Baltimore
NEIBaltimore <- subset(NEI, fips == "24510")
summaryEmissions <- tapply(NEIBaltimore$Emissions, NEIBaltimore$year, sum)
# plot
png(filename = "plot2.png", width = 480, height = 480)
barplot(summaryEmissions, col = rainbow(4), border = "dark blue", density = 5*summaryEmissions/10^3)
lines(summaryEmissions / 2, lty=2)
points(summaryEmissions / 2)
title("PM2.5 Emissions in Maryland Baltimore", xlab="Year", ylab="Emissions")
dev.off()