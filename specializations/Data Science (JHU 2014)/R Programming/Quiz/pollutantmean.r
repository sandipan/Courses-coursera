pollutantmean <- function(directory, pollutant, id = 1:332) {
	## 'directory' is a character vector of length 1 indicating
	## the location of the CSV files
	files <- list.files(directory)
	p <- NULL
	for (f in files) {
		## 'pollutant' is a character vector of length 1 indicating
		## the name of the pollutant for which we will calculate the
		## mean; either "sulfate" or "nitrate".
		d <- read.csv(paste(directory, '/', f, sep=''))
		ID <- unique(d$ID)[1]
		if (ID %in% id) {
			p <- rbind(p, d[!is.na(d[pollutant]), ][pollutant])
			## 'id' is an integer vector indicating the monitor ID numbers
			## to be used
		}
	}
	## Return the mean of the pollutant across all monitors list
	## in the 'id' vector (ignoring NA values)
	return (apply(p, 2, mean))
	#return (mean(p[,1]))
}
