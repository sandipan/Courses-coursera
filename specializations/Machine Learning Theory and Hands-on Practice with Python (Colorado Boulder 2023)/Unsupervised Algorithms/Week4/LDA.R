rawdocs <- c(
  "eat turkey on turkey day holiday",
  "i like to eat cake on holiday",
  "turkey trot race on thanksgiving holiday",
  "snail race the turtle",
  "time travel space race",
  "movie on thanksgiving",
  "movie at air and space museum is cool movie",
  "aspiring movie star"
)
docs <- strsplit(rawdocs, split = " ")

# unique words
vocab <- unique( unlist(docs) )

# replace words in documents with wordIDs
for( i in 1:length(docs) ) {
  docs[[i]] <- match( docs[[i]], vocab )
}
docs

# cluster number 
K <- 2 

# initialize count matrices 
# @wt : word-topic matrix 
wt <- matrix( 0, K, length(vocab) )
colnames(wt) <- vocab

# @ta : topic assignment list
ta <- lapply( docs, function(x) rep( 0, length(x) ) ) 
names(ta) <- paste0( "doc", 1:length(docs) )

# @dt : counts correspond to the number of words assigned to each topic for each document
dt <- matrix( 0, length(docs), K )

set.seed(1234)
for( d in 1:length(docs) ) { 
  # randomly assign topic to word w
  for( w in 1:length( docs[[d]] ) ) {
    ta[[d]][w] <- sample(1:K, 1) 
    
    # extract the topic index, word id and update the corresponding cell 
    # in the word-topic count matrix  
    ti <- ta[[d]][w]
    wi <- docs[[d]][w]
    wt[ti, wi] <- wt[ti, wi] + 1    
  }
  
  # count words in document d assigned to each topic t
  for( t in 1:K ) {
    dt[d, t] <- sum( ta[[d]] == t )
  }
}

# randomly assigned topic to each word
print(ta)


print(wt)
print(dt)


LDA1 <- function( docs, vocab, K, alpha, eta, iterations )
{
  # initialize count matrices 
  # @wt : word-topic matrix 
  wt <- matrix( 0, K, length(vocab) )
  colnames(wt) <- vocab
  
  # @ta : topic assignment list
  ta <- lapply( docs, function(x) rep( 0, length(x) ) ) 
  names(ta) <- paste0( "doc", 1:length(docs) )
  
  # @dt : counts correspond to the number of words assigned to each topic for each document
  dt <- matrix( 0, length(docs), K )
  
  for( d in 1:length(docs) )
  { 
    # randomly assign topic to word w
    for( w in 1:length( docs[[d]] ) )
    {		
      ta[[d]][w] <- sample( 1:K, 1 ) 
      
      # extract the topic index, word id and update the corresponding cell 
      # in the word-topic count matrix  
      ti <- ta[[d]][w]
      wi <- docs[[d]][w]
      wt[ ti, wi ] <- wt[ ti, wi ] + 1    
    }
    
    # count words in document d assigned to each topic t
    for( t in 1:K )  
      dt[ d, t ] <- sum( ta[[d]] == t ) 
  }
  
  # for each pass through the corpus
  for( i in 1:iterations ) 
  {
    # for each document
    for( d in 1:length(docs) )
    {
      # for each word
      for( w in 1:length( docs[[d]] ) )
      {
        t0  <- ta[[d]][w]
        wid <- docs[[d]][w]
        
        dt[ d, t0 ]   <- dt[ d, t0 ] - 1
        wt[ t0, wid ] <- wt[ t0, wid ] - 1 
        
        left  <- ( wt[ , wid ] + eta ) / ( rowSums(wt) + length(vocab) * eta )
        right <- ( dt[ d, ] + alpha ) / ( sum( dt[ d, ] ) + K * alpha )
        
        t1 <- sample( 1:K, 1, prob = left * right )
        
        # update topic assignment list with newly sampled topic for token w.	
        # and re-increment word-topic and document-topic count matrices with 
        # the new sampled topic for token w.
        ta[[d]][w] <- t1 
        dt[ d, t1 ]   <- dt[ d, t1 ] + 1  
        wt[ t1, wid ] <- wt[ t1, wid ] + 1
        
        # examine when topic assignments change
        # if( t0 != t1 ) 
        #	 print( paste0( "doc:", d, " token:" , w, " topic:", t0, "=>", t1 ) ) 
      }
    }
  }
  
  return( list( wt = wt, dt = dt ) )
}

# parameters 
alpha <- 1
eta <- 1

# initial topics assigned to the first word of the first document
# and its corresponding word id 
t0  <- ta[[1]][1]
wid <- docs[[1]][1]

# z_-i means that we do not include token w in our word-topic and document-topic 
# count matrix when sampling for token w, 
# only leave the topic assignments of all other tokens for document 1
dt[1, t0] <- dt[1, t0] - 1 
wt[t0, wid] <- wt[t0, wid] - 1

# Calculate left side and right side of equal sign
left  <- ( wt[, wid] + eta ) / ( rowSums(wt) + length(vocab) * eta )
right <- ( dt[1, ] + alpha ) / ( sum( dt[1, ] ) + K * alpha )

# draw new topic for the first word in the first document 
# The optional prob argument can be used to give a vector of weights for obtaining the elements of the vector being sampled. They need not sum to one, but they should be non-negative and not all zero.
t1 <- sample(1:K, 1, prob = left * right)
t1

K <- 2 
alpha <- 1
eta <- 0.001
iterations <- 1000

set.seed(4321)
lda1 <- LDA1( docs = docs, vocab = vocab, 
              K = K, alpha = alpha, eta = eta, iterations = iterations )
lda1