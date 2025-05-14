getmonitor <- function(id, directory, summarize = FALSE) {
	## 'id' is a vector of length 1 indicating the monitor ID
	## number. The user can specify 'id' as either an integer, a
	## character, or a numeric.

	## 'directory' is a character vector of length 1 indicating
	## the location of the CSV files

	## 'summarize' is a logical indicating whether a summary of
	## the data should be printed to the console; the default is
	## FALSE

	## Your code here
	f <- paste(directory, "/", sprintf("%03d", as.integer(id)), ".csv", sep = "") 
	rows <- read.csv(f, header = TRUE,  strip.white = TRUE)
	if (summarize) {
		print(summary(rows))
	}
	return(rows)
}

#data <- getmonitor(1, "specdata", TRUE)
#setwd