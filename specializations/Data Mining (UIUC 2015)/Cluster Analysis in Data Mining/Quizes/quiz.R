text1 <- text2 <- rep(0, 16)
text1[1:12] <- 1
text2[1:4] <- 1
text2[13:16] <- 1
cosine(text1, text2)

purity <- function(df) {
 nC <- rowSums(df)
 nT <- colSums(df)
 n <- sum(nC)
 #print(nC)
 #print(nT)
 #print(n)
 p <- c()
 for (i in 1:nrow(df))  {
   p <- c(p, max(df[i,]) / nC[i])
 }
 #print(p)
 print(sum(p * nC) / n)
}

#purity(matrix(c(10, 40, 10, 20, 10, 30, 30, 0, 50), nrow=3, ncol=3, byrow=T))
purity(matrix(c(20, 30, 10, 30, 40, 10, 0, 0, 60), nrow=3, ncol=3, byrow=T))

library(combinat)
maxMatch <- function(df) {
  nC <- rowSums(df)
  nT <- colSums(df)
  n <- sum(nC)
  #print(nC)
  #print(nT)
  #print(n)
  p <- c()
  for (T in permn(1:nrow(df))) {
    tot <- 0 
    for (i in 1:nrow(df)) {
     tot <- tot + df[i, T[i]]
    }
    p <- c(p, tot / n)
    #print(T)
    #print(tot / n)
  }
  print(max(p))
}

#maxMatch(matrix(c(20, 30, 10, 30, 40, 10, 0, 0, 60), nrow=3, ncol=3, byrow=T))
maxMatch(matrix(c(10, 40, 10, 20, 10, 30, 30, 0, 50), nrow=3, ncol=3, byrow=T))

pairwise_external <- function(df) {
  nC <- rowSums(df)
  nT <- colSums(df)
  n <- sum(nC)
  #print(nC)
  #print(nT)
  #print(n)
  TP <- sum(sapply(df, function(x) x*(x-1)/2))
  FN <- sum(sapply(nT, function(x) x*(x-1)/2)) - TP
  FP <- sum(sapply(nC, function(x) x*(x-1)/2)) - TP
  TN <- n * (n - 1) / 2 - (TP + FN + FP)
  print(TP)
  print(FN)
  print(FP)
  print(TN)
}

pairwise_external(matrix(c(8, 2, 3, 7), nrow=2, ncol=2, byrow=T))

