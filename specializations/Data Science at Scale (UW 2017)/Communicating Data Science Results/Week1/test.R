setwd('C:/work/analytics/R/packages/nfl-predictive-package')
df <- read.csv('train3.csv')
train <- df[1:150,-(1:2)]
m <- rpart(SHOWUP~., train, cp=0)
test <- df[151:170,-(1:2)]
predict(m, test)

df1 <- df2 %>% group_by(Day, Hr) %>% summarise(count=n()) #, Summarized.Offense.Description)
df1 <- as.data.frame(df1)
df1$Hr <- as.integer(df1$Hr)
df1 <- as.matrix(as.data.frame(cast(df1, Day ~ Hr)))
heatmap(df1, col = cm.colors(256), scale = "column", margins = c(5,10))
library(gplots)
heatmap.2(as.matrix(df1),cellnote=as.matrix(df1), dendrogram = "none",
          notecol="black",col=redblue(256),scale="none",key=TRUE, keysize=1.5,
          density.info="none", trace="none", cexRow=0.7,cexCol=1.2)


addresses <- with(visit.wine, 
                  paste(Address, City, "CA", sep=", ")
)
locs <- geocode(addresses[1:5], output='more')

seattle <- geocode("SEATTLE")
map.seattle_city <- get_map(location = c(lon = seattle$lon, lat = seattle$lat), source='google', zoom = 15)
#df1 <- df2 %>% group_by(Latitude, Longitude) %>% summarise(count=n())
#names(df1) <- c('lon', 'lat', 'count')
df1<- df2 %>% select(lon=Longitude, lat=Latitude, Month) #, Summarized.Offense.Description)
df1 <- df1 %>% filter(lon < 0.0 | lat > 0.0)
ggmap(map.seattle_city, extent = "normal", maprange=FALSE) + 
  #geom_tile(data = df1, aes(x = lon, y = lat, alpha = ..count..), fill = 'red') + 
  stat_density2d(data=df1, aes(alpha = ..level.., fill=..level..), geom = 'polygon') +
  scale_alpha(range = c(0.00, 0.25), guide = FALSE) +
  scale_fill_gradient(low = "green", high = "red") +
  coord_map(projection="mercator", 
            xlim=c(attr(map.seattle_city, "bb")$ll.lon, attr(map.seattle_city, "bb")$ur.lon),
            ylim=c(attr(map.seattle_city, "bb")$ll.lat, attr(map.seattle_city, "bb")$ur.lat)) +
  facet_wrap(~Month) +
  theme(legend.position = "none", axis.title = element_blank(), text = element_text(size = 12))

seattle <- geocode("SEATTLE")
map.seattle_city <- get_map(location = c(lon = seattle$lon, lat = seattle$lat), source='google', zoom = 15)
#df1 <- df2 %>% group_by(Latitude, Longitude) %>% summarise(count=n())
#names(df1) <- c('lon', 'lat', 'count')
df1<- df2 %>% select(lon=Longitude, lat=Latitude, Month) #, Summarized.Offense.Description)
df1 <- df1 %>% filter(lon < 0.0 | lat > 0.0)
ggmap(map.seattle_city, extent = "normal", maprange=FALSE) + 
  #geom_tile(data = df1, aes(x = lon, y = lat, alpha = ..count..), fill = 'red') + 
  stat_density2d(data=df1, aes(alpha = ..level.., fill=..level..), geom = 'polygon') +
  scale_alpha(range = c(0.00, 0.25), guide = FALSE) +
  scale_fill_gradient(low = "green", high = "red") +
  coord_map(projection="mercator", 
            xlim=c(attr(map.seattle_city, "bb")$ll.lon, attr(map.seattle_city, "bb")$ur.lon),
            ylim=c(attr(map.seattle_city, "bb")$ll.lat, attr(map.seattle_city, "bb")$ur.lat)) +
  facet_wrap(~Month) +
  theme(legend.position = "none", axis.title = element_blank(), text = element_text(size = 12))

seattle <- geocode("San Francisco")
map.seattle_city <- get_map(location = c(lon = seattle$lon, lat = seattle$lat), source='google', zoom = 14)
#df1 <- df2 %>% group_by(Latitude, Longitude) %>% summarise(count=n())
#names(df1) <- c('lon', 'lat', 'count')
df1<- df %>% select(lon=X, lat=Y, Month) #, Summarized.Offense.Description)
df1 <- df1 %>% filter(lon < 0.0 | lat > 0.0)
ggmap(map.seattle_city, extent = "normal", maprange=FALSE) + 
  #geom_tile(data = df1, aes(x = lon, y = lat, alpha = ..count..), fill = 'red') + 
  stat_density2d(data=df1, aes(alpha = ..level.., fill=..level..), geom = 'polygon') +
  scale_alpha(range = c(0.00, 0.25), guide = FALSE) +
  scale_fill_gradient(low = "green", high = "red") +
  coord_map(projection="mercator", 
            xlim=c(attr(map.seattle_city, "bb")$ll.lon, attr(map.seattle_city, "bb")$ur.lon),
            ylim=c(attr(map.seattle_city, "bb")$ll.lat, attr(map.seattle_city, "bb")$ur.lat)) +
  facet_wrap(~Month) +
  theme(legend.position = "none", axis.title = element_blank(), text = element_text(size = 12))

df1<- df2 %>% group_by(Day, Hr) %>% summarise(count=n()) #, Summarized.Offense.Description)
df1 <- as.data.frame(df1)
df1$Hr <- as.integer(df1$Hr)
ggplot(df1, aes(Day, Hr)) + 
  geom_tile(aes(fill = count), colour = "white") + 
  scale_x_continuous(breaks=1:31) +
  scale_y_continuous(breaks=0:23) +
  scale_fill_gradient(low="green", high="red") + #low = "white", high = "steelblue")
  xlab('Day of Month [1-31]') +
  ylab('Hour [0-24)') +
  theme(panel.background = element_blank(), axis.ticks = element_blank(), text = element_text(size = 15)) #, panel.ontop = TRUE)

df1<- df %>% group_by(Day, Hr) %>% summarise(count=n()) #, Summarized.Offense.Description)
df1 <- as.data.frame(df1)
df1$Hr <- as.integer(df1$Hr)
ggplot(df1, aes(Day, Hr)) + 
  geom_tile(aes(fill = count), colour = "white") + 
  scale_x_continuous(breaks=1:31) +
  scale_y_continuous(breaks=0:23) +
  scale_fill_gradient(low="green", high="red") + #low = "white", high = "steelblue")
  xlab('Day of Month [1-31]') +
  ylab('Hour [0-24)') +
  ggtitle('Crime Heatmap in San Francisco during the Summer in 2014') +
  theme(panel.background = element_blank(), axis.ticks = element_blank(), text = element_text(size = 15)) #, panel.ontop = TRUE)



legend(y=1.1, x=.25, xpd=TRUE,     
       legend = unique(dat$GO),
       col = unique(as.numeric(dat$GO)), 
       lty= 1,             
       lwd = 5,           
       cex=.7
)

pngoutfile <-  'day_hr.png'
open3d()
plot3d(df1[,1], df1[,2], df1[,3], col = 'green', type='s', size=1, xlab='x', ylab='y', zlab='count')
rgl.snapshot(pngoutfile)
rgl.close()

seattle <- geocode("SEATTLE")
map.seattle_city <- get_map(location = c(lon = seattle$lon, lat = seattle$lat), source='google', zoom = 14)
#df1 <- df2 %>% group_by(Latitude, Longitude) %>% summarise(count=n())
#names(df1) <- c('lon', 'lat', 'count')
df1<- df2 %>% select(lon=Longitude, lat=Latitude) #, Summarized.Offense.Description)
df1 <- df1 %>% filter(lon < 0.0 | lat > 0.0)
ggmap(map.seattle_city, extent = "normal", maprange=FALSE) + 
  #geom_tile(data = df1, aes(x = lon, y = lat, alpha = ..count..), fill = 'red') + 
  stat_density2d(data=df1, aes(alpha = ..level.., fill=..level..), geom = 'polygon') +
  scale_alpha(range = c(0.00, 0.25), guide = FALSE) +
  scale_fill_gradient(low = "green", high = "red") +
  coord_map(projection="mercator", 
            xlim=c(attr(map.seattle_city, "bb")$ll.lon, attr(map.seattle_city, "bb")$ur.lon),
            ylim=c(attr(map.seattle_city, "bb")$ll.lat, attr(map.seattle_city, "bb")$ur.lat)) +
  theme(legend.position = "none", axis.title = element_blank(), text = element_text(size = 12))
#theme(axis.title.y = element_blank(), axis.title.x = element_blank())

seattle <- geocode("San Francisco")
map.seattle_city <- get_map(location = c(lon = seattle$lon, lat = seattle$lat), source='google', zoom = 16)
#df1 <- df2 %>% group_by(Latitude, Longitude) %>% summarise(count=n())
#names(df1) <- c('lon', 'lat', 'count')
df1<- df %>% select(lon=X, lat=Y) #, Summarized.Offense.Description)
df1 <- df1 %>% filter(lon < 0.0 | lat > 0.0)
ggmap(map.seattle_city, extent = "normal", maprange=FALSE) + 
  #geom_tile(data = df1, aes(x = lon, y = lat, alpha = ..count..), fill = 'red') + 
  stat_density2d(data=df1, aes(alpha = ..level.., fill=..level..), geom = 'polygon') +
  scale_alpha(range = c(0.00, 0.25), guide = FALSE) +
  scale_fill_gradient(low = "green", high = "red") +
  coord_map(projection="mercator", 
            xlim=c(attr(map.seattle_city, "bb")$ll.lon, attr(map.seattle_city, "bb")$ur.lon),
            ylim=c(attr(map.seattle_city, "bb")$ll.lat, attr(map.seattle_city, "bb")$ur.lat)) +
  theme(legend.position = "none", axis.title = element_blank(), text = element_text(size = 12))
#theme(axis.title.y = element_blank(), axis.title.x = element_blank())


df1 <- df %>% group_by(DayOfWeek, Month, Day, Hr, PdDistrict) %>% summarise(numIncidents=n())
ggplot(df1, aes(x=DayOfWeek, y=numIncidents)) + geom_boxplot() #geom_violin() + stat_smooth()
ggplot(df1, aes(x=as.factor(Month), y=numIncidents)) + geom_boxplot() #+ stat_smooth()
ggplot(df1, aes(x=PdDistrict, y=numIncidents)) + geom_boxplot() #geom_violin() + stat_smooth()

#df1 <- df %>% group_by(DayOfWeek, Month, Day, Hr, PdDistrict, Category) %>% summarise(numIncidents=n())
#c <- ggplot(df1, aes(x=Day, y=numIncidents, colour=factor(Category)))
#c + stat_smooth(method=lm) + geom_point()
df1 <- df %>% group_by(Day, Hr, Category) %>% summarise(numIncidents=n())
ggplot(df1, aes(Day, Hr)) + stat_binhex(binwidth = c(5, 3)) +facet_wrap(~Category)

ggplot(df1, aes(x=Day, y=numIncidents)) + stat_smooth()
ggplot(df1, aes(x=Hr, y=numIncidents)) + stat_smooth()
m <- lm(numIncidents~., df1)
m <- rpart(numIncidents~., df1)

library(rpart)
m <- rpart(Resolution ~ ., df)

df1 <- df %>% group_by(X, Y, Category) %>% summarise(count=n()) 
seattle <- geocode("San Francisco")
map.seattle_city <- get_map(location = c(lon = seattle$lon, lat = seattle$lat), source='google', zoom=13) #qmap(, zoom = 11, source="google")
map.seattle_city
df1 <- df1 %>% filter(Category %in% c('ASSAULT', 'LARCENY/THEFT', 'ROBBERY', 'VEHICLE THEFT', 'FRAUD',  'WARRANTS', 
                                      'WEAPON LAWS', 'MISSING PERSON'))
#colourCount = 12
#getPalette = colorRampPalette(brewer.pal(9, "Set1"))
ggmap(map.seattle_city) + 
  facet_wrap(~Category) +
  geom_point(aes(x=X, y=Y, fill=Category, size=count), colour="black", shape=21, data=df1) + 
#scale_colour_manual(values=c("dark blue","orange"))+
#labs(fill="Summarized.Offense.Description") +
  xlab('Longitude') +
  ylab('Latitude') +
  scale_fill_brewer(palette="Dark2") + guides(fill = guide_legend(override.aes = list(size=15)))
#scale_color_manual(values=wes_palette(n=8, name="GrandBudapest"))
#scale_colour_hue(l=80, c=150)
#scale_shape_manual(values = 1:48) 



df1 <- df2 %>% group_by(Summarized.Offense.Description, Day) %>% summarise(count=n()) 
df1<-cast(df1, Day~Summarized.Offense.Description)[-1]
names(df1) <- gsub(' ', '_', names(df1))
names(df1) <- gsub('/', '_', names(df1))
names(df1) <- gsub('-', '_', names(df1))
png('cor2.png', width = 1500, height = 1500)
ggpairs(df1[c(3,5,6,8,9,19,20,
              25,38,39,41,42,43,45)],
        lower = list(continuous = "smooth"))  +   
        theme(legend.position = "none",
        panel.grid.major = element_blank(),
        axis.ticks = element_blank(),
        axis.text.x = element_text(angle = 90, hjust = 1), 
        axis.text.y = element_text(angle = 90, hjust = 1), 
        axis.title.x = element_text(angle = 180, vjust = 1, color = "black"), text = element_text(size = 10),
        panel.border = element_rect(fill = NA))
dev.off()



ggplot(df, aes(Day, fill=Category)) + geom_bar() +
  #scale_x_continuous(breaks=seq(0, 24, 5)) +
  facet_wrap(~Category, scale='free') +
  xlab('Hour [0-24)') +
  ylab('Number of incidents') +
  theme(axis.text.x = element_text(angle = 90, hjust = 1), legend.position="none", 
        text = element_text(size = 15)) 




df1 <- df %>% group_by(PdDistrict, Hr) %>% summarise(count=n()) 
ggplot(df1, aes(Hr, count)) + geom_point(size=2) + geom_line() + facet_grid(~PdDistrict)#, scales='free')
symbols(df1$Hr, df1$PdDistrict, circles=df1$count, bg=df1$PdDistrict)
df1 <- df %>% group_by(Category, Hr) %>% summarise(count=n()) 
ggplot(df1, aes(Hr, count)) + geom_point(aes(color=Category),size=3) + geom_line(aes(color=Category)) + facet_grid(~Category) + #,scales='free')
  theme(axis.text.x = element_text(angle = 90, hjust = 1), strip.text.x = element_text(size = 12, colour = "red", angle = 90),
        legend.position="none", text = element_text(size = 10)) 
#symbols(df1$Hr, df1$Category, circles=df1$count, bg=df1$Category)
df1 <- df %>% group_by(DayOfWeek, Hr) %>% summarise(count=n()) 
ggplot(df1, aes(Hr, count)) + geom_point(aes(color=DayOfWeek),size=5) + geom_line(aes(color=DayOfWeek)) + facet_grid(~DayOfWeek) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1), legend.position="none", text = element_text(size = 20)) 
symbols(df1$Hr, df1$DayOfWeek, circles=df1$count, bg=df1$DayOfWeek)
df1 <- df %>% group_by(Month, Hr) %>% summarise(count=n()) 
ggplot(df1, aes(Hr, count)) + geom_point(aes(color=Month),size=5) + geom_line(aes(color=Month)) + facet_grid(~Month) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1), legend.position="none", text = element_text(size = 20)) 
#symbols(df1$Hr, df1$Month, circles=df1$count, bg=df1$Month)
df1 <- df %>% group_by(PdDistrict, Category) %>% summarise(count=n()) 
symbols(df1$Category, df1$PdDistrict, circles=df1$count, bg=df1$PdDistrict)
ggplot(df1, aes(x=Category, y=count, fill=PdDistrict)) + geom_bar(position=position_dodge(),stat="identity") +
  scale_fill_brewer(palette="Set1") +
  theme(axis.text.x = element_text(angle = 90, hjust = 1), text = element_text(size = 15)) 

ggplot(df, aes(PdDistrict, fill=Category)) + geom_bar() +
  theme(axis.text.x = element_text(angle = 90, hjust = 1), text = element_text(size = 15))

ggplot(df, aes(Category, fill=PdDistrict)) + geom_bar() +
  theme(axis.text.x = element_text(angle = 90, hjust = 1), text = element_text(size = 15)) +
  scale_fill_brewer(palette="Set3") #+
#scale_fill_brewer()

ggplot(df, aes(Category, fill=PdDistrict)) + geom_bar(position='dodge') +
  theme(axis.text.x = element_text(angle = 90, hjust = 1), text = element_text(size = 15)) +
  scale_fill_brewer(palette="Set3")


ggplot(df, aes(Category, fill=Category)) + geom_bar() + facet_wrap(~ PdDistrict) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1), text = element_text(size = 15))

ggplot(df, aes(Resolution, fill=Resolution)) + geom_bar() + facet_wrap(~ PdDistrict) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1), text = element_text(size = 15))

df1 <- df %>% group_by(PdDistrict, Category, Month) %>% summarise(count=n()) 
#symbols(df1$Category, df1$PdDistrict, circles=df1$count, bg=df1$PdDistrict)
ggplot(df1, aes(x=Category, y=count, fill=PdDistrict)) + geom_bar(position=position_dodge(),stat="identity") +
  scale_fill_brewer(palette="Set1") +
  theme(axis.text.x = element_text(angle = 90, hjust = 1), text = element_text(size = 15))  + facet_wrap(~Month)

df1 <- df %>% group_by(PdDistrict, Month, Hr) %>% summarise(count=n()) 
ggplot(df1, aes(Hr, count, color=as.factor(Month))) + geom_point(aes(shape=PdDistrict, size=count)) + #, scales='free')
  scale_shape_manual(values=1:10)
df1 <- df %>% group_by(PdDistrict, Category, Hr) %>% summarise(count=n()) 
ggplot(df1, aes(Hr, count, color=as.factor(Category))) + geom_point(aes(shape=PdDistrict, size=count)) + #, scales='free')
  scale_shape_manual(values=1:10)

df1 <- df %>% group_by(PdDistrict, Month) %>% summarise(count=n()) 
ggplot(df1, aes(Month, count, color=as.factor(PdDistrict))) + geom_point(size=4) + geom_line(size=1.4, linetype=2) + #, scales='free')
  scale_colour_brewer(palette="Set3")

df1 <- df %>% group_by(PdDistrict, Resolution) %>% summarise(count=n()) 
ggplot(df1, aes(PdDistrict, Resolution, color=count)) + geom_point(aes(size=count)) + #, scales='free')
  scale_colour_brewer(palette="Set3")

df1 <- df %>% group_by(Category, Resolution) %>% summarise(count=n()) 
ggplot(df1, aes(Category, Resolution, color=count)) + geom_point(aes(size=count)) + #, scales='free')
  theme(axis.text.x = element_text(angle = 90, hjust = 1), text = element_text(size = 15))
scale_colour_brewer(palette="Set3")

df1 <- as.data.frame(df1)
library(gplots)
h2 <- hist2d(df[c(1,6)])
library(RColorBrewer)
rf <- colorRampPalette(rev(brewer.pal(11,'Spectral')))
r <- rf(32)
h2 <- hist2d(df1[3:4], nbins=25, col=r)
h2 <- hist2d(df1[3:4], nbins=25, col=r, FUN=function(x) log(length(x)))
library(MASS)
k <- kde2d(as.integer(df[,1]), as.integer(df[,6]), n=200)
image(k, col=r)
