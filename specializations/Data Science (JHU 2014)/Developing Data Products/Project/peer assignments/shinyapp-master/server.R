library(shiny)
shinyServer(
    function(input, output) {
        bmi <- reactive({as.numeric(input$weight) * as.numeric(input$sex) / (as.numeric(input$height) / 100) ** 2})
        scale <- reactive({c(15, 16, 18.5, 25, 30, 35, 40) * as.numeric(input$sex)})
        normal_avg <- reactive({(scale()[4] - scale()[3]) / 2 + scale()[3]})
        message1 <- reactive({ if (bmi() > scale()[4]) {
                                        paste("You BMI is", bmi() - scale()[4], 
                                              "points higher than upper normal boundary.*")
                                } else if (bmi() < scale()[3]) {
                                        paste("You BMI is", bmi() - scale()[4], 
                                              "points lower than lower normal boundary.*")
                                } else {
                                        "You BMI is normal.*"
                                }
                            })
        message2 <- reactive({ if ((bmi() > scale()[3]) & (bmi() < scale()[4])) {
                                    "Normal (healthy weight)*"
                             } else if ((bmi() > scale()[2]) & (bmi() < scale()[3])) {
                                    "Underweight*"
                             } else if ((bmi() > scale()[1]) & (bmi() < scale()[2])) {
                                    "Severely underweight*"
                             } else if ((bmi() < scale()[1])) {
                                    "Very severely underweight*"
                             } else if ((bmi() > scale()[4]) & (bmi() < scale()[5])) {
                                    "Overweight*"
                             } else if ((bmi() > scale()[5]) & (bmi() < scale()[6])) {
                                    "Obesety Class I (Moderately obesety)*"
                             } else if ((bmi() > scale()[6]) & (bmi() < scale()[7])) {
                                    "Obesety Class II (Severely obesety)*"
                             } else {
                                    "Obesety Class III (Very severely obesety)*"
                             }
                        })
        output$bmi <- renderPrint({ if (input$goButton >= 1) {bmi()} })
        output$message1 <- renderPrint({ if (input$goButton >= 1) {message1()} })
        output$message2 <- renderPrint({ if (input$goButton >= 1) {message2()} })
        output$bar_plot <- renderPlot({ if (input$goButton >= 1) {
                                            barplot(c(normal_avg(), bmi()), horiz=TRUE, 
                                                    col=c("palegreen", "skyblue"), 
                                                    xlim=c(0, (max(bmi(), normal_avg()) * 2)),
                                                    xlab="BMI");
                                            legend("topleft", legend=c("You BMI", "Normal average BMI*"), 
                                                   fill=c("skyblue", "palegreen"));
                                            abline(v=scale()[1:6], col=c("red", "yellow", "darkgreen", 
                                                                         "darkgreen", "yellow", "red"), lwd=2);
                                            legend("bottomleft", legend=c("Normal boarders", 
                                                                          "Overweight/underweight boarders",
                                                                          "Severely underweight/obese boarders"), 
                                                   col=c("darkgreen", "yellow", "red"), lty=1, lwd=2)
                                        }
                                     })
    }    
)