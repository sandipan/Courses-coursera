setwd("C:/Users/SANDIPAN DEY/Desktop/coursera/Reproducible Research/assignment2")


#Questions
#Your data analysis must address the following questions:
#Across the United States, which types of events (as indicated in the 
#EVTYPE variable) are most harmful with respect to population health?
#Across the United States, which types of events have the greatest 
#economic consequences?
#Consider writing your report as if it were to be read by a government or 
#municipal manager who might be responsible for preparing for severe weather 
#events and will need to prioritize resources for different types of events. 
#However, there is no need to make any specific recommendations in your report.
storm <- read.csv(bzfile("repdata-data-StormData.csv.bz2"))
names(storm)
head(storm)
dim(storm)

#loc_vars <- c("STATE", "BGN_DATE", "BGN_TIME", "END_DATE", "END_TIME", "EVTYPE")
loc_vars <- c("STATE", "BGN_DATE", "EVTYPE")
health_vars <- c("FATALITIES", "INJURIES")
prop_vars <- c("PROPDMG", "CROPDMG") #, "PROPDMGEXP", "CROPDMGEXP")
  
storm1 <- storm[c(loc_vars, health_vars)]
storm1$Health_Hazards <- storm1$FATALITIES + storm1$INJURIES
h <- sort(tapply(storm1$Health_Hazards, storm1$EVTYPE, sum), decreasing=TRUE)
f <- sort(tapply(storm1$FATALITIES, storm1$EVTYPE, sum), decreasing=TRUE)
i <- sort(tapply(storm1$INJURIES, storm1$EVTYPE, sum), decreasing=TRUE)
n <- 25
h <- head(h, n) #h[h > 0]
f <- head(f, n) #f[f > 0]
i <- head(i, n) #i[i > 0]
par(mfrow=c(1,3))
barplot(h, col=terrain.colors(n), names.arg=names(h), las=2, cex.names=0.9)
barplot(i, beside=T, col=topo.colors(n), names.arg=names(i), las=2, cex.names=0.9)
barplot(f, beside=T, col=heat.colors(n), names.arg=names(f), las=2, cex.names=0.9)

library(ggplot2)

h <- as.data.frame(cbind(event=names(h), count=h, type="Health Hazard"))
h$count <- as.integer(as.character(h$count))
h <- transform(h, event = reorder(event, count))
ggplot(h, aes(event, count)) + geom_bar(stat="identity") + 
theme(axis.text.x=element_text(angle=90,hjust=1,vjust=0.5)) + 
coord_flip()

h <- as.data.frame(cbind(event=names(h), count=h, type="Health Hazard"))
f <- as.data.frame(cbind(event=names(f), count=f, type="Fatalities"))
i <- as.data.frame(cbind(event=names(i), count=i, type="Injuries"))
d <- rbind(h, f, i)
d$count <- as.integer(as.character(d$count))
d <- transform(d, event = reorder(event, -count))
ggplot(d, aes(event, count, fill = type)) + geom_bar(position = "dodge") + theme(axis.text.x=element_text(angle=90,hjust=1,vjust=0.5)) #+ coord_flip()
ggplot(d, aes(x=event, y=count, fill=type)) + geom_bar(stat="identity") + facet_wrap(~type, scales = "free") + theme(axis.text.x=element_text(angle=90,hjust=1,vjust=0.5)) #+ coord_flip()

d1 <- d[d$event != "TORNADO",]
ggplot(d1, aes(event, count, fill = type)) + geom_bar(position = "dodge") + theme(axis.text.x=element_text(angle=90,hjust=1,vjust=0.5)) #+coord_flip()
#qplot(count, data=d, geom="density", fill=type) + theme(axis.text.x=element_text(angle=90,hjust=1,vjust=0.5))
#qplot(event, count, data=d, geom=c("boxplot", "jitter"), fill=type) + theme(axis.text.x=element_text(angle=90,hjust=1,vjust=0.5))
ggplot(d, aes(x=event, y=count)) + geom_bar(stat="identity")

#library(sqldf)
#storm2 <- sqldf("select STATE, EVTYPE, count(*) as COUNT from storm1 group by EVTYPE")
#ggplot(storm2, aes(EVTYPE, COUNT)) + geom_bar(stat="identity") + facet_wrap(~STATE) + theme(axis.text.x=element_text(angle=90,hjust=1,vjust=0.5)) #+ coord_flip()

#ggplot(storm2, aes(STATE, EVTYPE)) + 
#geom_tile(aes(fill = exp(-scale(COUNT, center=FALSE))), colour = "white") + 
#scale_fill_gradient(low = "black", high = "steelblue")

storm2 <- storm[c(loc_vars, prop_vars)]
storm2$PROPDMG <- as.numeric(as.character(storm2$PROPDMG))
storm2$CROPDMG <- as.numeric(as.character(storm2$CROPDMG))
storm2$Prop_Hazards <- storm2$PROPDMG + storm2$CROPDMG
p <- sort(tapply(storm2$Prop_Hazards, storm2$EVTYPE, sum), decreasing=TRUE)
p1 <- sort(tapply(storm2$PROPDMG, storm2$EVTYPE, sum), decreasing=TRUE)
p2 <- sort(tapply(storm2$CROPDMG, storm2$EVTYPE, sum), decreasing=TRUE)
n <- 25
p1 <- head(p1, n)
p2 <- head(p2, n)
p <- head(p, n)

p <- as.data.frame(cbind(event=names(p), count=p, type="Prop Hazard"))
p1 <- as.data.frame(cbind(event=names(p1), count=p1, type="Prop Dmg"))
p2 <- as.data.frame(cbind(event=names(p2), count=p2, type="Crop Dmg"))
d <- rbind(p, p1, p2)
d$count <- as.integer(as.character(d$count))
d <- transform(d, event = reorder(event, -count))
ggplot(d, aes(event, count, fill = type)) + geom_bar(position = "dodge") + theme(axis.text.x=element_text(angle=90,hjust=1,vjust=0.5)) #+ coord_flip()
ggplot(d, aes(x=event, y=count, fill=type)) + geom_bar(stat="identity") + facet_wrap(~type, scales = "free") + theme(axis.text.x=element_text(angle=90,hjust=1,vjust=0.5)) #+ coord_flip()


library(reshape)
library(scales)
library(ggplot2)
nba <- read.csv("http://datasets.flowingdata.com/ppg2008.csv")
nba$Name <- with(nba, reorder(Name, PTS))
nba.m <- melt(nba)
nba.m <- ddply(nba.m, .(variable), transform, rescale = rescale(value))
(p <- ggplot(nba.m, aes(variable, Name)) + 
   geom_tile(aes(fill = rescale), colour = "white") + 
   scale_fill_gradient(low = "white", high = "steelblue"))
                  
base_size <- 9
p + theme_grey(base_size = base_size) + 
  labs(x = "", y = "") + scale_x_discrete(expand = c(0, 0)) +
  scale_y_discrete(expand = c(0, 0)) + 
  opts(legend.position = "none", axis.ticks = theme_blank(), 
  axis.text.x = theme_text(size = base_size * 0.8, angle = 330, hjust = 0, colour = "grey50"))

require(graphics); require(grDevices)
x  <- as.matrix(mtcars)
rc <- rainbow(nrow(x), start = 0, end = .3)
cc <- rainbow(ncol(x), start = 0, end = .3)
hv <- heatmap(x, col = cm.colors(256), scale = "column",
              RowSideColors = rc, ColSideColors = cc, margins = c(5,10),
              xlab = "specification variables", ylab =  "Car Models",
              main = "heatmap(<Mtcars data>, ..., scale = \"column\")")
utils::str(hv) # the two re-ordering index vectors

library(reshape)
library(ggplot2)
# Using ggplot2 0.9.2.1

nba <- read.csv("http://datasets.flowingdata.com/ppg2008.csv")
nba$Name <- with(nba, reorder(Name, PTS))
nba.m <- melt(nba)
nba.m <- ddply(nba.m, .(variable), transform, value = scale(value))

# Convert the factor levels to numeric + quanity to determine size of hole.
nba.m$var2 = as.numeric(nba.m$variable) + 15

# Labels and breaks need to be added with scale_y_discrete.
y_labels = levels(nba.m$variable)
y_breaks = seq_along(y_labels) + 15

p2 = ggplot(nba.m, aes(x=Name, y=var2, fill=value)) +
  geom_tile(colour="white") +
  scale_fill_gradient(low = "white", high = "steelblue") +
  ylim(c(0, max(nba.m$var2) + 0.5)) +
  scale_y_discrete(breaks=y_breaks, labels=y_labels) +
  coord_polar(theta="x") +
  theme(panel.background=element_blank(),
        axis.title=element_blank(),
        panel.grid=element_blank(),
        axis.text.x=element_blank(),
        axis.ticks=element_blank(),
        axis.text.y=element_text(size=5))


ggsave(filename="plot_2.png", plot=p2, height=7, width=7)

library(gridExtra)
grid.arrange(tableGrob(tblHealth), nrow=1, as.table=TRUE)

par(mfrow=c(1,3))
barplot(h, col=terrain.colors(n), names.arg=names(h), las=2, cex.names=0.9)
barplot(i, beside=T, col=topo.colors(n), names.arg=names(i), las=2, cex.names=0.9)
barplot(f, beside=T, col=heat.colors(n), names.arg=names(f), las=2, cex.names=0.9)

p <- ggplot(data=d, 
            aes(x=factor(1),
                y=count,
                fill = factor(event))
)
print(unique(d$event))
p <- p + geom_bar(stat = "identity") #(width = 1)
p <- p + facet_grid(facets = . ~ type, scales = "free") 
# + theme(legend.text = element_text(size = 5))
p # + scale_y_continuous(formatter = 'percent')  + xlab("") 
p + coord_polar(theta="y")  
