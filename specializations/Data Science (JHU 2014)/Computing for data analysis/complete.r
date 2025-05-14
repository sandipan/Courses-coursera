complete <- function(directory, ids = 1:332) {
	
	## 'directory' is a character vector of length 1 indicating
	## the location of the CSV files

	## 'id' is an integer vector indicating the monitor ID numbers
	## to be used
	
	## Return a data frame of the form:
	## id nobs
	## 1  117
	## 2  1041
	## ...
	## where 'id' is the monitor ID number and 'nobs' is the
	## number of complete cases
	
	id <- c()
	nobs <- c()
	for (i in ids) {	
		
		f <- paste(directory, "/", sprintf("%03d", as.integer(i)), ".csv", sep = "") 
		rows <- read.csv(f, header = TRUE,  strip.white = TRUE)
		id <- c(id, i)
		nobs <- c(nobs, sum(complete.cases(rows)))		
	}
		
	return(data.frame(id, nobs))
}