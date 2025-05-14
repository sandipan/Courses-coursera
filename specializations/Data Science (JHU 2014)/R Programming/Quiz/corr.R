corr <- function(directory, threshold = 0) {
	## 'directory' is a character vector of length 1 indicating
	## the location of the CSV files
	files <- list.files(directory)
	id <- 1:332
	crv <- c()
	for (f in files) {
		d <- read.csv(paste(directory, '/', f, sep=''))
		d <- na.omit(d)
		ID <- unique(d$ID)[1]
		if (ID %in% id) {
			nobs <- nrow(d)
			if (nobs > threshold) {
				crv <- c(crv, cor(d$sulfate, d$nitrate))
			}
		}
	}
	## 'threshold' is a numeric vector of length 1 indicating the
	## number of completely observed observations (on all
	## variables) required to compute the correlation between
	## nitrate and sulfate; the default is 0
	return(crv)
	## Return a numeric vector of correlations
}