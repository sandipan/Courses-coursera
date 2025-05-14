library(shiny)
shinyUI(pageWithSidebar(
        headerPanel("Body Mass Index Calculator"),
        sidebarPanel(
            h3("Description"),
            p("Body mass index (BMI) is a measure of body fat based on height and ", 
              "weight that applies to adult men and women. BMI provides a simple ", 
              "numeric measure of a person's thickness or thinness, allowing health ", 
              "professionals to discuss overweight and underweight problems more ",
              "objectively with their patients. It is a simple mean of classifying ",
              "sedentary (physically inactive) individuals."),
            p("To calculate you body mass index, please enter you parameters and ",
              'press "Calculate BMI" button. After that you can compare you BMI with ', 
              'World Health Organization standarts and normal BMI on the "Plot" tab, or check', 
              'exect BMI index and some description on the "Summary" tab'),
            h3("Parameters:"),
            sliderInput("height", "Enter you height in centimeters here:", value=170, 
                        min=120, max=220, step=1),
            sliderInput("weight", "Enter you weight in kilograms here:", value=60, 
                        min=30, max=200, step=1),
            radioButtons("sex", "Choose your sex:", selected="1.1",
                         c("male" = "1.1",
                           "female" = "1")),
            actionButton("goButton", "Calculate BMI")
        ),
        mainPanel(
            h3("Results:"),
            tabsetPanel(
                        type = "tabs",
                        tabPanel("Plot", plotOutput("bar_plot")),
                        tabPanel("Summary",
                                 h4("You Body Mass Index is:"),
                                 verbatimTextOutput("bmi"),
                                 h4("How far from normal is it?"),
                                 verbatimTextOutput("message1"),
                                 h4("Classification according to World Health Organization Database:"),
                                 verbatimTextOutput("message2")
                        )),
            p("* According to BMI Classification. Global Database on Body Mass Index. World Health ", 
              "Organization. 2006.")
        )
))
