compute_z <- function(xbar, mu, sigma, n) {
  z <- (xbar - mu) / (sigma / sqrt(n))
  z
  
  pnorm(z)
  pnorm(xbar, mu, sigma / sqrt(n))  
}

xbar <- 18.86
mu <- 20
sigma <- 8.6
n <- 73

compute_z(xbar, mu, sigma, n)

compute_z(xbar=11.3, mu=15, sigma=sqrt(6.43), n=12)

#Phi((xbar - mu) / (sigma / sqrt(n))) <= 0.05
#xbar > mu + qnorm(0.05)*(sigma / sqrt(n))
15 + qnorm(0.05)*(sqrt(6.43) / sqrt(12))

#1-Phi((xbar - mu) / (sigma / sqrt(n))) >= 0.01
#xbar  <= mu + qnorm(0.01, lower.tail = FALSE)*(sigma / sqrt(n))
#round(50 + qnorm(0.01, lower.tail = FALSE)*(3.2 / sqrt(15)), 2)
round(50 - qnorm(0.01, lower.tail = FALSE)*(3.2 / sqrt(15)), 2)

mu <- p <- 0.6 # p
n <- 100
xbar <- phat <- 68 / n
sigma <- sqrt(phat*(1-phat)/n)
qnorm(0.03, lower.tail=FALSE)
pnorm((phat - p)/sqrt(phat*(1-phat)/n), lower.tail=FALSE)

x <- c(179, 156, 167,183, 178, 165)
xbar <- mean(x)
xbar
mu <- 170
sigma <- 4.2
#compute_z(xbar, mu, sigma, n)
qnorm(0.02, lower.tail = FALSE)
pnorm((xbar - mu)/(sigma/sqrt(length(x))), lower.tail=FALSE)


powers <- c()
mu0 <- 220
mus <- seq(mu0-20, mu0+20,1)
alpha <- 0.05
qalpha2 <- qnorm(alpha/2, lower.tail = FALSE)
qalpha2
xbar <- 232
sigma <- 15
n <- 10
for (mu in mus) {
  #z <- (xbar-mu)/(sigma/sqrt(n))
  powers <- c(powers, pnorm((mu0-qalpha2*sigma/sqrt(n)-mu)/(sigma/sqrt(n))) + pnorm((mu0+qalpha2*sigma/sqrt(n)-mu)/(sigma/sqrt(n)), lower.tail = FALSE))
  #powers <- c(powers, pnorm(-alpha/2, z) + pnorm(alpha/2, z, lower.tail = FALSE))
}
plot(mus, powers, type='l')

xbar <- 13.8
xbar
mu <- 14
sigma <- 0.08
n <- 20
#compute_z(xbar, mu, sigma, n)
alpha <- 0.05
qalpha2 <- qnorm(alpha/2, lower.tail = FALSE)
#mu - alpha2*(sigma / sqrt(n)) <= xbar  <= mu + alpha2*(sigma / sqrt(n))
c(mu - qalpha2*(sigma / sqrt(n)), mu + qalpha2*(sigma / sqrt(n)))
#pnorm((xbar - mu)/(sigma/sqrt(n)))

xbar <- 38.8
mu <- 40
S <- sqrt(2.8)
n <- 10
2*pt((xbar - mu) / (S/sqrt(n)), df=n-1) # two-tailed p-value


xbar <- 53.87
mu <- 50
S <- 6.82
n <- 15
(xbar - mu) / (S/sqrt(n))
qt(0.05, n-1, lower.tail = FALSE)
pt((xbar - mu) / (S/sqrt(n)), df=n-1, lower.tail = FALSE) # one-tailed p-value

x1bar <- 4.1
x2bar <- 3.3
S1 <- 2.1
S2 <- 1.5
n1 <- 120
n2 <- 100
(x1bar - x2bar) / sqrt(1/n1+1/n2) / sqrt(((n1-1)*S1^2+(n2-1)*S2^2)/(n1+n2-2))
Sp2 <- ((n1-1)*S1^2+(n2-1)*S2^2)/(n1+n2-2)
(x1bar - x2bar) / sqrt((1/n1+1/n2)*Sp2)

x1bar <- 4.1
x2bar <- 3.3
S1 <- 2.1
S2 <- 1.5
n1 <- 120
n2 <- 100
(x1bar - x2bar) / sqrt(S1^2/n1+S2^2/n2)

qchisq(1-0.01, 9) + qt(1-0.9, 6)

pchisq((10-1)*(5.2/4)^2, df=10-1, lower.tail=FALSE)

s12 <- 13.2 
n1 <- 8
s22 <- 15.1
n2 <- 6

s22 / s12

qf(0.03/2, n2-1, n1-1, lower.tail=FALSE) 

qchisq(0.05, 1, lower.tail = FALSE)

my_data = structure(list(id = 1:8, reviews = c("I guess the employee decided to buy their lunch with my card my card hoping I wouldn't notice but since it took so long to run my car I want to head and check my bank account and sure enough they had bought food on my card that I did not receive leave. Had to demand for and for a refund because they acted like it was my fault and told me the charges are still pending even though they are for 2 different amounts.", 
                                               "I went to McDonald's and they charge me 50 for Big Mac when I only came with 49. The casher told me that I can't read correctly and told me to get glasses. I am file a report on your casher and now I'm mad.", 
                                               "I really think that if you can buy breakfast anytime then I should be able to get a cheeseburger anytime especially since I really don't care for breakfast food. I really like McDonald's food but I preferred tree lunch rather than breakfast. Thank you thank you thank you.", 
                                               "I guess the employee decided to buy their lunch with my card my card hoping I wouldn't notice but since it took so long to run my car I want to head and check my bank account and sure enough they had bought food on my card that I did not receive leave. Had to demand for and for a refund because they acted like it was my fault and told me the charges are still pending even though they are for 2 different amounts.", 
                                               "Never order McDonald's from Uber or Skip or any delivery service for that matter, most particularly one on Elgin Street and Rideau Street, they never get the order right. Workers at either of these locations don't know how to follow simple instructions. Don't waste your money at these two locations.", 
                                               "Employees left me out in the snow and wouldn't answer the drive through. They locked the doors and it was freezing. I asked the employee a simple question and they were so stupid they answered a completely different question. Dumb employees and bad food.", 
                                               "McDonalds food was always so good but ever since they add new/more crispy chicken sandwiches it has come out bad. At first I thought oh they must haven't had a good day but every time I go there now it's always soggy, and has no flavor. They need to fix this!!!", 
                                               "I just ordered the new crispy chicken sandwich and I'm very disappointed. Not only did it taste horrible, but it was more bun than chicken. Not at all like the commercial shows. I hate sweet pickles and there were two slices on my sandwich. I wish I could add a photo to show the huge bun and tiny chicken."
)), class = "data.frame", row.names = c(NA, -8L))

my_data


library(udpipe)
library(BTM)
data("brussels_reviews_anno", package = "udpipe")

## Taking only nouns of Dutch data
x <- subset(brussels_reviews_anno, language == "nl")
x <- subset(x, xpos %in% c("NN", "NNP", "NNS"))
x <- x[, c("doc_id", "lemma")]

## Building the model
set.seed(321)
model  <- BTM(x, k = 3, beta = 0.01, iter = 1000, trace = 100)

## Inspect the model - topic frequency + conditional term probabilities
model$theta

topicterms <- terms(model, top_n = 10)
topicterms