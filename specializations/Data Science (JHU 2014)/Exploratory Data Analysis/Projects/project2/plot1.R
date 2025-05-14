# read the RDS files
NEI <- readRDS("summarySCC_PM25.rds")
SCC <- readRDS("Source_Classification_Code.rds")

# yearwise total emission
summaryEmissions <- tapply(NEI$Emissions, NEI$year, sum)
# plot
png(filename = "plot1.png", width = 480, height = 480)
barplot(summaryEmissions, col = 2*summaryEmissions/10^6, border = "dark blue", density = 5*summaryEmissions/10^6, yaxt = "n") #col = heat.colors(6), log = "y"
axis(2, at = seq(0, 8000000, 1000000), labels = 0:8, las = 2)
lines(summaryEmissions / 2, lty=2)
points(summaryEmissions / 2)
title("Total PM2.5 Emissions in the USA", xlab="Year", ylab="Emissions (in millions)")
dev.off()