library(ggplot2)

# read the RDS files
NEI <- readRDS("summarySCC_PM25.rds")
SCC <- readRDS("Source_Classification_Code.rds")

NEIB <- subset(NEI, fips == "24510")
NEIBty <- aggregate(NEIB$Emissions,list(NEIB$year, NEIB$type),sum) 
names(NEIBty) <- c("year", "type", "Emissions")
png(filename = "plot3.png", width = 480, height = 480)
ggplot(NEIBty, aes(x=year, y=Emissions, group=type)) + 
geom_line(aes(colour=type, linetype=type)) + 
geom_point() + 
scale_x_continuous(breaks=seq(1999, 2008, 1)) +
scale_y_continuous(breaks=seq(0, 2500, 250)) +
scale_linetype_manual(values=c("solid", "twodash", "longdash", "dashed")) +
ggtitle("Emissions from 1999–2008 for Baltimore City by types of sources")
dev.off()