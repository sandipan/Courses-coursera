shinyUI(pageWithSidebar(

  headerPanel("Shiny with mtcars"),

  sidebarPanel(

	h4("Description"),
	p("The application is meant to provide a simple visualization for the mtcars dataset.", 
	"This Motor Trend Car Road Tests dataset comes along with the R base packages.",
	"It comprises of the fuel consumption and 10 aspects of automobile design / performance."),
	conditionalPanel(condition="input.conditionedPanels == 'Tables'",  
		   p("In the first tab (Tables), first select a variable (such as fuel consumption mpg) 
		   from the drop down: The summary statistics for the variable will be shown immediately.", 
		   "Also, enter the number of observations for the selected variable to view, in the text box",
		   "only that many rows of values for that variable will be shown"),
           selectInput(inputId = "var",
                       label = "Select a variable to display the summary statistics",
                       choices = names(mtcars),
                       selected = "mpg"),
           numericInput("obs", "Number of observations to view:", min = 0, max = nrow(mtcars), value = 5)
    ),                     
    conditionalPanel(condition="input.conditionedPanels == 'Plot'",  
      	   p("The second tab (Plot) is meant to display linear regression (OLS) model fits",
	       "for the output variable mpg (fuel consumption in miles / gallon).",
	       "Choose an input (independent) variable (such as weight) from the drop down list.",
	       "The corresponding straight line will be fit and immediately shown in the plot.",
	       "Also select another input variable (such as number of cylinders) as color.",
		   "Different values of this color variable will be shown by color coding."),
           selectInput(inputId = "color",
                       label = "select the color variable",
                       choices = c("cyl", "gear", "vs", "carb"),
                       selected = "cyl"),
           selectInput(inputId = "x",
                       label = "Select input variables",
                       choices = c("wt", "qsec", "am", "disp"),
                       selected = "wt")
    ),
	p("See the pdf documentation and R codes at ",
	"https://github.com/sandipan/DevelopingDataProducts")    
  ),

  mainPanel(
    tabsetPanel(
      tabPanel("Tables",  
               h4("Summary"), 
               verbatimTextOutput("summary"), 
               tableOutput("view")
      ), 
      tabPanel("Plot", plotOutput("plot", width="100%", height="400px")),
      id = "conditionedPanels" 
    )    
  )
))
