complete <- function(directory, id = 1:332) {
	## 'directory' is a character vector of length 1 indicating
	## the location of the CSV files
	files <- list.files(directory)
	dfm <- data.frame(id = id, nobs = 0)
	for (f in files) {
		d <- na.omit(read.csv(paste(directory, '/', f, sep='')))
		ID <- unique(d$ID)[1]
		if (ID %in% id) {
			dfm[dfm$id == ID,]$nobs <- nrow(d)
		}
	}
	## 'id' is an integer vector indicating the monitor ID numbers
	## to be used
	## Return a data frame of the form:
	## id nobs
	## 1  117
	## 2  1041
	## ...
	## where 'id' is the monitor ID number and 'nobs' is the
	## number of complete cases
	return(dfm)
}