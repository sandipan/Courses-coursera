makeVector <- function(x = numeric()) {
	m <- NULL
	set <- function(y) {
			x <<- y
			m <<- NULL
	}
	get <- function() x
	setmean <- function(mean) m <<- mean
	getmean <- function() m
	list(set = set, get = get,
		 setmean = setmean,
		 getmean = getmean)
}

cachemean <- function(x, ...) {
	m <- x$getmean()
	if(!is.null(m)) {
			message("getting cached data")
			return(m)
	}
	data <- x$get()
	m <- mean(data, ...)
	x$setmean(m)
	m
}

# source("cacheMean.R")
# r <- rnorm(10000000)
# cachemean(makeVector(r))
# git clone https://github.com/rdpeng/ProgrammingAssignment2 "E:/Academics/Coursera/R Programming/Assignments"
