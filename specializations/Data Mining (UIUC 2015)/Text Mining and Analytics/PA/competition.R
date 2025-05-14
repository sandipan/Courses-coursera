#install.packages("C:/courses/Coursera/Current/Text Mining and Analytics/Lectures/rJava_0.9-7.tar.gz", repos = NULL, type="source")
#Sys.setenv(JAVA_HOME="C:\\Program Files\\Java\\jdk1.7.0_75\\jre")

setwd('C:/courses/Coursera/Current/Text Mining and Analytics/PA')

library(tm)
library(RTextTools)
library(stringr)
#library(RWeka)
#library(lsa)
#library(wordcloud)
#library(topicmodels)

#UniBigramTokenizer <- function(x) NGramTokenizer(x, Weka_control(min = 1, max = 2))
#UniBiTrigramTokenizer <- function(x) NGramTokenizer(x, Weka_control(min = 1, max = 3))

get.dtm <- function(sdf) {
  
  corpus <- Corpus(VectorSource(sdf$text))
  corpus <- tm_map(corpus, content_transformer(tolower))
  corpus <- tm_map(corpus, content_transformer(function(x) str_replace_all(x, "'", "")))
  corpus <- tm_map(corpus, content_transformer(function(x) str_replace_all(x, '[[:punct:]]',' ')))
  #corpus <- tm_map(corpus, content_transformer(function(x) removePunctuation(x, preserve_intra_word_dashes = TRUE)))
  corpus <- tm_map(corpus, content_transformer(stripWhitespace))
  corpus <- tm_map(corpus, content_transformer(removeNumbers))
  corpus <- tm_map(corpus, content_transformer(removeWords), setdiff(c(stopwords('english')), c('not', 'very', 'so'))) #, 'also', 'the', 'they',
                                                              #'cant', 'dont', 'doesnt', 'its', 'hasnt', 'havnt'))
  corpus <- tm_map(corpus, content_transformer(stemDocument))

  matrix <- DocumentTermMatrix(corpus, control = list(
    tokenize=scan_tokenizer, 
    #bounds = list(global = c(nrow(sdf) * 0.01, nrow(sdf) * 0.8)), # minDocFreq, maxDocFreq
    #tokenize=UniBigramTokenizer,
    #tokenize=UniBiTrigramTokenizer #,
    #toLower=TRUE,                                                    
    #stopwords = TRUE,
    #removePunctuation = TRUE,
    #stripWhitespace = TRUE,
    #stemWords=TRUE, 
    removeSparseTerms = TRUE, #function(x) removeSparseTerms(x, 0.2) #,
    #removeNumbers = TRUE ,
    #weighting = function(x) weightTfIdf(x, normalize = TRUE),
    weighting = function(x) weightSMART(x, spec = "ntc"),
    tokenize=UniBigramTokenizer
  ))
  return(matrix)
}

find.frequent <- function(sdf, thres) {
  matrix <- get.dtm(sdf)
  return(findFreqTerms(matrix, lowfreq=thres))
}

df <- as.data.frame(readLines(con <- file("hygiene.dat"))) #, encoding = "UCS-2LE"))
#df <- do.call("rbind", lapply(rdmTweets, as.data.frame))
names(df) <- 'text'
close(con)
df$label <- readLines(con <- file("hygiene.dat.labels"))
close(con)
df <- df[1:546,]
df <- df[sample(1:(nrow(df)),size=nrow(df),replace=FALSE),]
training_codes <- df$label

#matrix <- create_matrix(df, language="english", 
#                        removeNumbers=FALSE, 
#                        stemWords=TRUE, 
#                        removePunctuation=TRUE, 
#                        ngramLength=1, 
#                        weighting=weightTfIdf
#                        )

#myCorpus <- Corpus(VectorSource(df$text))
#matrix <- DocumentTermMatrix(myCorpus, control = list(
#                                                   tokenize=scan_tokenizer, 
#                                                   #tokenize=UniBigramTokenizer,
#                                                   toLower=TRUE,                                                    
#                                                   stopwords = TRUE,
#                                                   removePunctuation = TRUE,
#                                                   stripWhitespace = TRUE,
#                                                   stemWords=TRUE, 
#                                                   removeSparseTerms = function(x) removeSparseTerms(x, 0.2),
#                                                   removeNumbers = TRUE,
#                                                   weighting = function(x) weightTfIdf(x, normalize = TRUE) #,
#                                                   #tokenize=UniBigramTokenizer
#                                                   ))
#matrixLSASpace <- lsa(matrix)
#dim(matrix)
#dim(as.textmatrix(matrixLSASpace))
#head(as.textmatrix(matrixLSASpace))

#matrix1 <- get.dtm(df)

#thres <- 0.05
#posfreq <- find.frequent(df[df$label == 1,], thres)
#negfreq <- find.frequent(df[df$label == 0,], thres)

#features <- unique(c(posfreq, negfreq))

#features <- intersect(matrix1$dimnames$Terms, features)
#matrix <- matrix1[,features]

#matrix <- matrix1
matrix <- get.dtm(df)

matrix <- cbind(matrix, grepl(paste(1, 'star'), tolower(df$text)))
for (i in 2:20) {
  matrix <- cbind(matrix, grepl(paste(i, 'stars'), tolower(df$text)))
}

#matrix <- cbind(matrix, grepl('place', tolower(df$text)) & grepl('clean', tolower(df$text)))
#matrix <- cbind(matrix, grepl('area', tolower(df$text)) & grepl('clean', tolower(df$text)))
bigrams <- c('very clean', 'not clean', 'not very clean', 'not so clean', 'pretty clean', 'super clean', 'good cleaning', 'so clean',
             'severe cleaning', 'extremely clean', 'decore clean', 'severe cleaning', 'quite clean', 'clean finish', 'fairly clean', 'clean decor',
             'clean line', 'seldom clean', 'cleanest', 'not the cleanest')
clean_words <- c('space', 'place', 'area', 'spot', 'location', 'atmosphere',  'environment', 'ambience', 'surroundings',
                       'establishment', 'restaurant', 'department', 'outside', 'outlets', 'interior', 'inside',
                       'parking', 'kitchen', 'bathroom', 'wall', 'things', 'look', 'towels', 'utensils', 'food',
                       'carpet', 'dish', 'table', 'bars', 'floors',  'glasses', 'seat', 'flavors', 
                       'rice', 'foam', 'hair',  'socks', 'cup', 'tray', 'pan', 'hands', 'fingers', 'spoon',
                       'complain', 'issues', 'love',
                       'quiet', 'tidy', 'nice', 'organized', 'healthy', 'sanitary', 'bright', 'spacious', 'fresh', 'taste', 'cheap',
                       'walk', 'hole', 'windows', 'dim',  #'tablecloth', 
                       'birds', 'martini', 'palate',
                       'pipe',  'vodka', 'wok', 'not', 'very', 'good', 'seldom',
                       'going', 'graffiti', 'leftover')
dirty_words <- c('space', 'place', 'area', 'spot', 'location', 'atmosphere',  'environment', 'ambience',
                 'establishment', 'restaurant', 'department', 'outside', 'outlets', 'interior', 'inside',
                 'parking', 'kitchen', 'bathroom', 'wall', 'things', 'look', 'towels', 'utensils', 'food',
                 'carpet', 'dish', 'table', 'bars', 'floors',  'glasses', 'seat', 'flavors', 
                 'rice', 'foam', 'hair',  'socks', 'cup', 'tray', 'hands', 'fingers',
                 
                 'warm', 'nasty', 'hot', 'noise', 'disgusting', 'untidy',
                 
                 'walk', 'hole', 'windows', 'dim',  #'tablecloth', 
                 'birds', 'martini', 'palate',
                 'pipe',  'vodka', 'wok', 'not',
                 'going', 'graffiti', 'leftover')
hygiene_words <- c('trust', 'scary', 'suspect', 'good', 'issues'. 'faith', 'no')

#for (word in bigrams) {
#  print(word)
#  f <- apply(cbind(as.matrix(matrix[,'clean']), as.matrix(matrix[,word])), 1, min)
#  matrix <- cbind(matrix, f)
#}

for (word in clean_words) {
  print(word)
  f <- apply(cbind(as.matrix(matrix[,'clean']), as.matrix(matrix[,word])), 1, min)
  matrix <- cbind(matrix, f)
}

for (word in dirty_words) {
  print(word)
  f <- apply(cbind(as.matrix(matrix[,'clean']), as.matrix(matrix[,word])), 1, min)
  matrix <- cbind(matrix, f)
}

for (word in hygiene_words) {
  print(word)
  f <- apply(cbind(as.matrix(matrix[,'clean']), as.matrix(matrix[,word])), 1, min)
  matrix <- cbind(matrix, f)
}

#f <- apply(cbind(as.matrix(matrix[,'free']), as.matrix(matrix[,'wifi'])), 1, min)
#matrix <- cbind(matrix, f)

#matrix <- as.DocumentTermMatrix(matrix, weighting = function(x) weightTfIdf(x, normalize = FALSE))
matrix <- as.textmatrix(lsa(matrix))

#matrix <- as.DocumentTermMatrix(matrix, weighting = function(x) weightTfIdf(x, normalize = TRUE))
#wordsh <- findAssocs(matrix, 'hygiene', 0.80)
#wordsc <- findAssocs(matrix, 'clean', 0.80)
#wordsd <- findAssocs(matrix, 'dirty', 0.80)
#for (word in wordsh) matrix <- cbind(matrix, grepl(word, tolower(df$text)) & grepl('hygiene', tolower(df$text)))
#for (word in wordsc) matrix <- cbind(matrix, grepl(word, tolower(df$text)) & grepl('clean', tolower(df$text)))
#for (word in wordsd) matrix <- cbind(matrix, grepl(word, tolower(df$text)) & grepl('dirty', tolower(df$text)))
#matrix <- as.DocumentTermMatrix(matrix, weighting = function(x) weightTfIdf(x, normalize = TRUE), removeSparseTerms=TRUE)

#findAssocs(matrix, "dirty", 0.3)

#lw_bintf(matrix) * gw_idf(matrix)

#inspect(matrix[1:5,145:160])

#num <- 10 # Show this many top frequent terms
#matrix[findFreqTerms(matrix)[1:num],] %>%
#  as.matrix() %>%
#  rowSums()

container <- create_container(matrix,t(training_codes),trainSize=1:300, testSize=301:546,virgin=FALSE)
#container <- create_container(as.textmatrix(matrixLSASpace), t(training_codes),trainSize=1:300, testSize=301:546,virgin=FALSE)
models <- train_models(container, algorithms=c("RF", "MAXENT")) #"MAXENT" "BAGGING")) #, "BOOSTING", "GLMNET", "SLDA"))
                         #c("MAXENT","SVM","GLMNET","SLDA","TREE","BAGGING","BOOSTING","RF"))

results <- classify_models(container, models)
analytics <- create_analytics(container, results)
create_precisionRecallSummary(container, results)
ensemble <- create_ensembleSummary(analytics@document_summary)
ensemble
score_summary <- create_scoreSummary(container, results)

#maxent <- cross_validate(container, 2, algorithm="MAXENT")



df <- as.data.frame(readLines(con <- file("hygiene.dat")))
names(df) <- 'text'
close(con)
df$label <- readLines(con <- file("hygiene.dat.labels"))
close(con)
training_codes <- df$label

matrix <- get.dtm(df)

matrix <- cbind(matrix, grepl(paste(1, 'star'), tolower(df$text)))
for (i in 2:20) {
  matrix <- cbind(matrix, grepl(paste(i, 'stars'), tolower(df$text)))
}

bigrams <- c('very clean', 'not clean', 'not very clean', 'not so clean', 'pretty clean', 'super clean', 'good cleaning', 'so clean',
             'severe cleaning', 'extremely clean', 'decore clean', 'severe cleaning', 'quite clean', 'clean finish', 'fairly clean', 'clean decor',
             'clean line', 'seldom clean', 'cleanest', 'not the cleanest')
clean_words <- c('space', 'place', 'area', 'spot', 'location', 'atmosphere',  'environment', 'ambience', 'surroundings',
                 'establishment', 'restaurant', 'department', 'outside', 'outlets', 'interior', 'inside',
                 'parking', 'kitchen', 'bathroom', 'wall', 'things', 'look', 'towels', 'utensils', 'food',
                 'carpet', 'dish', 'table', 'bars', 'floors',  'glasses', 'seat', 'flavors', 
                 'rice', 'foam', 'hair',  'socks', 'cup', 'tray', 'pan', 'hands', 'fingers', 'spoon',
                 'complain', 'issues', 'love',
                 'quiet', 'tidy', 'nice', 'organized', 'healthy', 'sanitary', 'bright', 'spacious', 'fresh', 'taste', 'cheap',
                 'walk', 'hole', 'windows', 'dim',  #'tablecloth', 
                 'birds', 'martini', 'palate',
                 'pipe',  'vodka', 'wok', 'not', 'very', 'good', 'seldom',
                 'going', 'graffiti', 'leftover')
dirty_words <- c('space', 'place', 'area', 'spot', 'location', 'atmosphere',  'environment', 'ambience',
                 'establishment', 'restaurant', 'department', 'outside', 'outlets', 'interior', 'inside',
                 'parking', 'kitchen', 'bathroom', 'wall', 'things', 'look', 'towels', 'utensils', 'food',
                 'carpet', 'dish', 'table', 'bars', 'floors',  'glasses', 'seat', 'flavors', 
                 'rice', 'foam', 'hair',  'socks', 'cup', 'tray', 'hands', 'fingers',
                 
                 'warm', 'nasty', 'hot', 'noise', 'disgusting', 'untidy',
                 
                 'walk', 'hole', 'windows', 'dim',  #'tablecloth', 
                 'birds', 'martini', 'palate',
                 'pipe',  'vodka', 'wok', 'not',
                 'going', 'graffiti', 'leftover')
hygiene_words <- c('trust', 'scary', 'suspect', 'good', 'issues'. 'faith', 'no')

#for (word in bigrams) {
#  print(word)
#  f <- apply(cbind(as.matrix(matrix[,'clean']), as.matrix(matrix[,word])), 1, min)
#  matrix <- cbind(matrix, f)
#}

for (word in clean_words) {
  print(word)
  f <- apply(cbind(as.matrix(matrix[,'clean']), as.matrix(matrix[,word])), 1, min)
  matrix <- cbind(matrix, f)
}

for (word in dirty_words) {
  print(word)
  f <- apply(cbind(as.matrix(matrix[,'clean']), as.matrix(matrix[,word])), 1, min)
  matrix <- cbind(matrix, f)
}

for (word in hygiene_words) {
  print(word)
  f <- apply(cbind(as.matrix(matrix[,'clean']), as.matrix(matrix[,word])), 1, min)
  matrix <- cbind(matrix, f)
}

#matrix <- as.DocumentTermMatrix(matrix, weighting = function(x) weightTfIdf(x, normalize = FALSE))
#matrix <- as.textmatrix(lsa(matrix))

container <- create_container(matrix,t(training_codes),trainSize=1:546, testSize=547:746,virgin=FALSE)
models <- train_models(container, algorithms=c("RF", "SVM", "MAXENT")) #MAXENT")) #, "BOOSTING", "GLMNET", "SLDA"))
#c("MAXENT","SVM","GLMNET","SLDA","TREE","BAGGING","BOOSTING","RF"))
results <- classify_models(container, models)
#analytics <- create_analytics(container, results)
#create_precisionRecallSummary(container, results)
#ensemble <- create_ensembleSummary(analytics@document_summary)
#ensemble
score_summary <- create_scoreSummary(container, results)



df <- as.data.frame(readLines(con <- file("hygiene.dat"))) #, encoding = "UCS-2LE"))
#df <- do.call("rbind", lapply(rdmTweets, as.data.frame))
close(con)
names(df) <- 'text'
df$label <- readLines(con <- file("hygiene.dat.labels"))
close(con)
training_codes <- df$label

#matrix <- create_matrix(df, language="english", 
#                        removeNumbers=FALSE, 
#                        stemWords=TRUE, 
#                        removePunctuation=TRUE, 
#                        weighting=weightTfIdf
#)

myCorpus <- Corpus(VectorSource(df$text))
matrix <- DocumentTermMatrix(myCorpus, control = list(tokenize=scan_tokenizer, #scan_tokenizer,
                                                      toLower=TRUE,                                                    
                                                      stopwords = TRUE,
                                                      removePunctuation = TRUE,
                                                      stripWhitespace = TRUE,
                                                      stemWords=TRUE, 
                                                      removeSparseTerms = TRUE,
                                                      removeNumbers = TRUE,
                                                      weighting = function(x) weightTfIdf(x, normalize = TRUE),
                                                      tokenize=UniBigramTokenizer
))

container <- create_container(matrix,t(training_codes),trainSize=1:546, testSize=547:746,virgin=FALSE)
models <- train_models(container, algorithms=c("RF", "MAXENT","BOOSTING"))
#c("MAXENT","SVM","GLMNET","SLDA","TREE","BAGGING","BOOSTING","RF"))
results <- classify_models(container, models)
#analytics <- create_analytics(container, results)
#create_precisionRecallSummary(container, results)
#ensemble <- create_ensembleSummary(analytics@document_summary)
#ensemble
score_summary <- create_scoreSummary(container, results)






findFreqTerms(matrix, lowfreq=1)
findAssocs(matrix1, 'dirty', 0.30)
findAssocs(matrix1, 'clean', 0.30)
findAssocs(matrix1, 'hygiene', 0.30)


# VIEW THE RESULTS BY CREATING ANALYTICS
analytics <- create_analytics(container, results)

myDtm <- TermDocumentMatrix(myCorpus, control = list(minWordLength = 1))
#inspect(myDtm[266:270,31:40])

#findFreqTerms(myDtm, lowfreq=10)
# which words are associated with "r"?
#findAssocs(myDtm, 'dirty', 0.30)
#findAssocs(myDtm, 'clean', 0.30)

m <- as.matrix(myDtm)
# calculate the frequency of words
v <- sort(rowSums(m), decreasing=TRUE)
myNames <- names(v)
#k <- which(names(v)=="clean")
#myNames[k] <- "clean"
d <- data.frame(word=myNames, freq=v)
wordcloud(d$word, d$freq, min.freq=3)



data(cora.documents)
data(cora.vocab)
#26 word.counts
K <- 10 ## Num clusters
result <- lda.collapsed.gibbs.sampler(cora.documents,
                                      K, ## Num clusters
                                      cora.vocab,
                                      25, ## Num iterations
                                      0.1,
                                      0.1)
## Get the top words in the cluster
top.words <- top.topic.words(result$topics, 5, by.score=TRUE)


df <- as.data.frame(readLines(con <- file("hygiene.dat"))) #, encoding = "UCS-2LE"))
#df <- do.call("rbind", lapply(rdmTweets, as.data.frame))
names(df) <- 'text'
df$label <- readLines(con <- file("hygiene.dat.labels"))

train <- df[1:546,]
test <- df[547:746,]

df <- train
dim(df)

myCorpus <- Corpus(VectorSource(df$text))
myCorpus <- tm_map(myCorpus, content_transformer(tolower))
# remove punctuation
myCorpus <- tm_map(myCorpus, content_transformer(removePunctuation))
# remove numbers
myCorpus <- tm_map(myCorpus, content_transformer(removeNumbers))
# remove stopwords
# keep "r" by removing it from stopwords
myStopwords <- c(stopwords('english'))
#idx <- which(myStopwords == "r")
#myStopwords <- myStopwords[-idx]
myCorpus <- tm_map(myCorpus, content_transformer(removeWords), myStopwords)

#dictCorpus <- myCorpus
# stem words in a text document with the snowball stemmers,
# which requires packages Snowball, RWeka, rJava, RWekajars
#myCorpus <- tm_map(myCorpus, content_transformer(stemDocument))
# inspect the first three ``documents"
#inspect(myCorpus[1:3])

# stem completion
#myCorpus <- tm_map(myCorpus, content_transformer(stemCompletion), dictionary=dictCorpus)
#inspect(myCorpus[1:3])

dtm <- DocumentTermMatrix(myCorpus, control = list(weighting = weightTfIdf, stopwords = TRUE))
