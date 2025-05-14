# see documentation and code at github
# https://github.com/sandipan/DevelopingDataProducts/tree/master/shinyProject

library(shiny)
library(ggplot2)

shinyServer(function(input, output) {

  output$plot <- renderPlot({
      col <- mtcars[input$color][,1]
      p <- qplot(mtcars[input$x][,1], mpg, data=mtcars, geom=c("point", "smooth"), 
          method="lm", formula=y~x, color=col, 
          main="Linear Regression (OLS) Fit", 
          xlab=input$x, ylab="mpg")
    
      print(p)
  })
  datasetInput <- reactive({
    switch(input$var, mtcars[input$var])
  })
  output$summary <- renderPrint({
    dataset <- datasetInput()
    summary(dataset)
  })
  output$view <- renderTable({
    head(datasetInput(), n = input$obs)
  })
})