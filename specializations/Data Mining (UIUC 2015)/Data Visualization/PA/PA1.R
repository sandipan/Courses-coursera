library(reshape2)
library(ggplot2)
library(RColorBrewer)

setwd('C:/courses/Coursera/Current/Data Visualization/PA')
df <- read.csv('ExcelFormattedGISTEMPDataCSV.csv')
df2 <- read.csv('ExcelFormattedGISTEMPData2CSV.csv')
head(df)

df <- df[c('Year','DJF','MAM','JJA','SON')]
mdf <- melt(df, id='Year')
mdf$Decade <- as.integer(mdf$Year / 10) * 10
mdf$Year <- mdf$Year - mdf$Decade
mdf$Decade <- as.factor(mdf$Decade)
mdf$value <- as.integer(mdf$value)

myColors <- c("#688FFC",
              "#97FB29",
              "#A0200C",
              "#244F3F",
              "#E271A1",
              "#A08206",
              "#34BFCA",
              "#30FD98",
              "#4B0623",
              "#B00AA1",
              "#A7B9E0",
              "#1D1D02",
              "#C30039",
              "#6A2703") 
myColors <-   c("#EE3069",
              "#1DE631",
              "#34E0D9",
              "#144E9A",
              "#15591E",
              "#EB7808",
              "#F0D697",
              "#321825",
              "#F8FE51",
              "#8D1785",
              "#B1BAFC",
              "#C583F3",
              "#02A629",
              "#A31136") #brewer.pal(14,"Set1")
names(myColors) <- levels(mdf$Decade)

ggplot(mdf, aes(x=Year,y=value, group=Decade, color=Decade)) + #, linetype=Decade)) + 
  geom_point(size=5, color='black') + geom_line(size=1.5) + facet_wrap(~variable) +
  scale_x_continuous(breaks=0:9) +
  scale_y_continuous(breaks=seq(-80, +80, 10)) +
  scale_colour_manual(name = "Decade",values = myColors) +
  xlab("From the start (year 0) to the end (year 9) for each decade") +
  ylab("Deviation") +
  theme(text = element_text(size = 20))


setwd('C:/courses/Coursera/Current/Data Visualization/PA')
df <- read.csv('ExcelFormattedGISTEMPDataCSV.csv')
df2 <- read.csv('ExcelFormattedGISTEMPData2CSV.csv')
head(df)

df <- df[c('Year','J.D')]
mdf <- melt(df, id='Year')
mdf$Decade <- as.integer(mdf$Year / 10) * 10
mdf$Year <- as.integer(mdf$Year - mdf$Decade)
mdf$Decade <- as.factor(mdf$Decade)
mdf$value <- as.integer(mdf$value)

ggplot(mdf, aes(x=Year,y=value, group=Decade, color=Decade)) + #, linetype=Decade)) + 
  geom_point(size=5, color='black') + geom_line(size=1.5) +
  scale_x_continuous(breaks=0:9) +
  scale_y_continuous(breaks=seq(-80, +80, 10)) +
  scale_colour_manual(name = "Decade",values = myColors) +
  xlab("From the start (year 0) to the end (year 9) for each decade") +
  ylab("Deviation") +
  theme(text = element_text(size = 20))

#p <- ggplot(mdf, aes(Year, value, group=Decade, color=Decade, fill=Decade))
#p + geom_area(position="fill") +
p <- ggplot(mdf, aes(Year, value))
p + geom_area(aes(colour = Decade, fill= Decade), position = 'stack') +
  scale_x_continuous(breaks=0:9) +
  #scale_y_continuous(breaks=seq(-80, +80, 10)) +
  scale_colour_manual(name = "Decade",values = myColors) +
  scale_fill_manual(name = "Decade",values = myColors) +
  xlab("From the start (year 0) to the end (year 9) for each decade") +
  ylab("Deviation") +
  theme(text = element_text(size = 20))


ggplot(mdf, aes(x = Year, y = value, fill = Decade)) + 
  geom_bar(stat = "identity", position='stack') +
  scale_x_continuous(breaks=0:9) +
  scale_y_continuous(breaks=seq(-80, +80, 10)) +
  scale_colour_manual(name = "Decade",values = myColors) +
  scale_fill_manual(name = "Decade",values = myColors) +
  xlab("From the start (year 0) to the end (year 9) for each decade") +
  ylab("Deviation") +
  theme(text = element_text(size = 20))

df2 <- df2[c('Year', 'Glob', 'NHem', 'SHem')]
df2 <- melt(df2, id='Year')

myColors <- c("#00FF00", "#FF0000", "#0000FF")
names(myColors) <- levels(df2$value)

ggplot(df2, aes(x=Year,y=value, group=variable, color=variable)) + #, linetype=variable)) + 
  geom_point(size=5, color='black') + geom_line(size=1.2) +
  scale_x_continuous(breaks=seq(1880, 2000, 20)) +
  scale_y_continuous(breaks=seq(-100, +100, 10)) +
  scale_colour_manual(name = "Hemespheres",values = myColors) +
  ylab("Deviation") +
  theme(text = element_text(size = 20))

df2$Decade <- as.integer(df2$Year / 10) * 10
df2$Year <- as.integer(df2$Year - df2$Decade)
df2$Decade <- as.factor(df2$Decade)

ggplot(df2, aes(x=Year,y=value, group=Decade, color=Decade)) + #, linetype=Decade)) + 
  geom_point(size=5, color='black') + geom_line(size=1.5) + facet_wrap(~variable) + #, scales='free') +
  scale_x_continuous(breaks=0:9) +
  scale_y_continuous(breaks=seq(-80, +80, 10)) +
  scale_colour_manual(name = "Decade",values = myColors) +
  xlab("From the start (year 0) to the end (year 9) for each decade") +
  ylab("Deviation") +
  theme(text = element_text(size = 20))


#qplot(Year, value, data = mdf, fill = Decade, geom = "area")

#source("https://gist.github.com/fawda123/6589541/raw/8de8b1f26c7904ad5b32d56ce0902e1d93b89420/plot_area.r")
#plot.area(mdf)

if (FALSE) {
  library(shiny)
  library(ggvis)
  
  runApp(list(ui = pageWithSidebar(
    div(),
    sidebarPanel(
      sliderInput("n", "Number of points", min = 1, max = nrow(mtcars),
                  value = 10, step = 1),
      uiOutput("plot_ui")
    ),
    mainPanel(
      ggvisOutput("plot"),
      tableOutput("mtc_table")
    )
  )
  , server= function(input, output, session) {
    # A reactive subset of mtcars
    mtc <- reactive({
      data = mtcars[1:input$n, ]
      data$long = as.character(paste0("A car with ",data$cyl," cylinders and ",data$gear," gears and ",data$carb, " carburators"))
      data
    })
    # A simple visualisation. In shiny apps, need to register observers
    # and tell shiny where to put the controls
    mtc %>%
      ggvis(~wt, ~mpg, key:= ~long) %>%
      layer_points(fill = ~factor(long)) %>%
      add_tooltip(function(data){
        paste0("Wt: ", data$wt, "<br>", "Mpg: ",as.character(data$mpg), "<br>", "String: ", as.character(data$long))
      }, "hover") %>%
      bind_shiny("plot", "plot_ui")
    
    output$mtc_table <- renderTable({
      mtc()[, c("wt", "mpg", "long")]
    })
  })
  )
  
  #shinyApp(ui = ui, server = server)
  
}
