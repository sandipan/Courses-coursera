# read the RDS files
NEI <- readRDS("summarySCC_PM25.rds")
SCC <- readRDS("Source_Classification_Code.rds")

#unique(SCC$EI.Sector)
SCC <- SCC[SCC$EI.Sector %in% grep("Coal", unique(SCC$EI.Sector), value=TRUE),]
NEISCC <- merge(NEI, SCC, by.x="SCC", by.y="SCC")
 
summaryEmissions <- tapply(NEISCC$Emissions, NEISCC$year, sum)
# plot
png(filename = "plot4.png", width = 480, height = 480)
barplot(summaryEmissions, col = 2*summaryEmissions/10^5, border = "dark blue", density = 5*summaryEmissions/10^5, yaxt = "n")
axis(2, at = seq(0, 700000, 100000), labels = 0:7, las = 2)
lines(summaryEmissions / 2, lty=2)
points(summaryEmissions / 2)
title("Emissions from coal combustion-related sources in the USA", xlab="Year", ylab="Emissions (x 10^6)")
dev.off()