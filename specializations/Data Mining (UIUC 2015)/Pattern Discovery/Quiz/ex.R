setwd("C:/courses/Coursera/Pattern Discovery")
library(arules)
library(arulesViz)
transacs <- read.transactions(file="tr.csv", format="basket", sep=",");
rules <- apriori(transacs, parameter = list(sup = 0.5, conf = 0.5, target="rules"))
rules <- apriori(transacs, parameter = list(sup = 0.4, conf = 0.5, target="rules"))
as(rules, "data.frame")
plot(rules)
plot(rules, method="grouped")
plot(rules, method="graph", control=list(type="items", arrowSize=0.2))

contingency <- function(tbl) {
  
  chisq <- 0
  rows <- rowSums(tbl)
  cols <- colSums(tbl)
  total <- sum(tbl)
  for (i in 1:2) {
    for (j in 1:2) {
      observed <- tbl[i, j]
      expected <- rows[i] * cols[j] / total
      chisq <- chisq + (observed - expected)^2 / expected
      #print(paste(rownames(tbl)[i], names(tbl)[j], 'observed', observed, 'expected', expected, (observed - expected)^2 / expected))
      print(paste('lift', rownames(tbl)[i], names(tbl)[j], tbl[i,j]*total/(rows[i]*cols[j])))      
      print(paste('allconf', rownames(tbl)[i], names(tbl)[j], tbl[i,j]/max(rows[i], cols[j])))      
      print(paste('jaccard', rownames(tbl)[i], names(tbl)[j], tbl[i,j]/(rows[i] + cols[j] - tbl[i,j])))     
      print(paste('cosine', rownames(tbl)[i], names(tbl)[j], tbl[i,j]/sqrt(rows[i]*cols[j])))      
      print(paste('kulczynski', rownames(tbl)[i], names(tbl)[j], 0.5*(tbl[i,j]/rows[i] + tbl[i,j]/cols[j])))      
      print(paste('maxconf', rownames(tbl)[i], names(tbl)[j], max(tbl[i,j] / rows[i] , tbl[i,j] / cols[j])))   
      print(paste('ir', rownames(tbl)[i], names(tbl)[j], abs(rows[i]-cols[j])/(rows[i] + cols[j] - tbl[i,j])))     
      print('')
    }
  }
  print(paste('chisq', chisq))
}

tbl <- as.data.frame(matrix(c(400, 350, 200, 50), nrow=2, byrow=TRUE))
names(tbl) <- c("B", "~B")
rownames(tbl) <- c("C", "~C")
contingency(tbl)

tbl <- as.data.frame(matrix(c(100, 1000, 1000, 100000), nrow=2, byrow=TRUE))
names(tbl) <- c("B", "~B")
rownames(tbl) <- c("C", "~C")
contingency(tbl)

tbl <- as.data.frame(matrix(c(10000, 1000, 1000, 100000), nrow=2, byrow=TRUE))
tbl <- as.data.frame(matrix(c(50000, 7000, 3000, 600000), nrow=2, byrow=TRUE))

tbl <- as.data.frame(matrix(c(100000, 7000, 3000, 300), nrow=2, byrow=TRUE))
tbl <- as.data.frame(matrix(c(100000, 7000, 3000, 90000), nrow=2, byrow=TRUE))
names(tbl) <- c("A", "~A")
rownames(tbl) <- c("B", "~B")
contingency(tbl)
# 1.000816622811   0.952726612830052
# 1.81471735777153 0.952726612830052

tbl <- as.data.frame(matrix(c(100000, 1000, 1000, 100), nrow=2, byrow=TRUE))
names(tbl) <- c("m", "~m")
rownames(tbl) <- c("c", "~c")
contingency(tbl)

tbl <- as.data.frame(matrix(c(700, 300, 500, 1500), nrow=2, byrow=TRUE))
names(tbl) <- c("DM", "~DM")
rownames(tbl) <- c("ML", "~ML")
contingency(tbl)

tbl <- as.data.frame(matrix(c(40, 24, 210, 126), nrow=2, byrow=TRUE))
names(tbl) <- c("HD", "~HD")
rownames(tbl) <- c("HM", "~HM")
contingency(tbl)

0.5 * (10 / 1000 + 10 / 1000) <= 0.01 # null invariant
(10 / 1000000) / ((1000 / 1000000)*(1000 / 1000000)) < 1 # support

0.5 * (500 / 5000 + 500 / 50000) <= 0.01
(5000 / 5000000) / ((50000 / 5000000)*(500 / 5000000)) < 1

1 - 205211 / 205227  # D(P1, P2)
1 - 101758 / 205227 # D(P1, P3)
1 - 161563 / 205227 # D(P1, P4)
1 - 161576 / 205227 # D(P1, P5)

0.5 * (600 / 10000 + 600 / 5000) <= 0.1 # null invariant
(600 / 100000) / ((10000 / 100000)*(5000 / 100000)) < 1 # support


library(arulesSequences)
x <- read_baskets(con = file("seq.txt"), info = c("sequenceID","eventID","SIZE"))
as(x, "data.frame")
## mine frequent sequences
s1 <- cspade(x, parameter = list(support = 0.75),
             control = list(verbose = TRUE, tidLists = TRUE))
summary(s1)
as(s1, "data.frame")

library(arulesSequences)
x <- read_baskets(con = file("seq1.txt"), info = c("sequenceID","eventID","SIZE"))
as(x, "data.frame")
## mine frequent sequences
s1 <- cspade(x, parameter = list(support = 1.0),
             control = list(verbose = TRUE, tidLists = TRUE))
summary(s1)
as(s1, "data.frame")







output$rankAds <- renderUI({ #renderText({
  input$rank
  r <- sort(rankAds(input$userid), decreasing=TRUE, index.return=TRUE)
  updateTextInput(session, inputId = "topMatch",
                  label = "Top match",
                  value = r$idx[1]
  )
  paste('Matched Ad: ad', r$ix[1], 'with score', r$x[1], 'Ad ids:', paste(r$ix, collapse=' '), 'Ad match scores:', paste(r$x, collapse=''))
})