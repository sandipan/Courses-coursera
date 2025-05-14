corr <- function(directory, threshold = 0) {
        ## 'directory' is a character vector of length 1 indicating
        ## the location of the CSV files

        ## 'threshold' is a numeric vector of length 1 indicating the
        ## number of completely observed observations (on all
        ## variables) required to compute the correlation between
        ## nitrate and sulfate; the default is 0
		
		corvec <- c()
		for (i in 1:332) {	
		
			f <- paste(directory, "/", sprintf("%03d", as.integer(i)), ".csv", sep = "") 
			rows <- read.csv(f, header = TRUE,  strip.white = TRUE)
			crows <- rows[complete.cases(rows),]
		
			if (dim(crows)[[1]] > threshold) {
				corvec <- c(corvec, cor(crows[,2], crows[,3]))
			}
		}
		return(corvec)
	
        ## Return a numeric vector of correlations
}

# X=cbind(c(1,1,1,1,1),0:4)
# Y=c(3,6,7,8,11)
# w=solve(t(X)%*%X)%*%(t(X)%*%Y)
# w=lm(Y~X[,2])
# plot(X[,2],Y)
# abline(w[1],w[2])