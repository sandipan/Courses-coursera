## makeCacheMatrix and cacheSolve are the functions that can be used together to invert a matrix with cache support 
## (once a matrix object is inverted, the inverted matrix will get cached and any future calls to invert the same matrix object,
## will use cache to retrieve the previously-computed inverted value)

## This function provides an interface with a list of functions to cache / retrieve the inverse of a matrix
## The original (invertible) matrix must be passed as argument to this function
makeCacheMatrix <- function(x = matrix()) {
	inv <- NULL
	set <- function(y) {
			x <<- y
			inv <<- NULL
	}
	get <- function() x
	setinv <- function(inverted) inv <<- inverted
	getinv <- function() inv
	list(set = set, get = get,
		 setinv = setinv,
		 getinv = getinv)
}

## This function inverts the matrix passed as argument and uses the other function to cache the result
## Assumption: the argument matrix x must be invertible 
cacheSolve <- function(x, ...) {
	## Return a matrix that is the inverse of 'x'
	inv <- x$getinv()
	if(!is.null(inv)) {
			message("getting cached data")
			return(inv)
	}
	data <- x$get()
	inv <- solve(data, ...)
	x$setinv(inv)
	inv
}

# Setup / Testing
# source("cacheMatrix.R")
# r <- replicate(25, rnorm(25))
# cacheSolve(makeCacheMatrix(r))
# cacheSolve(makeCacheMatrix(r)) %*% r
# git remote -v
# git remote rm origin
# git remote add origin https://github.com/sandipan/coursera
# git config master.remote origin
# git config master.merge refs/heads/master
# git config --global user.name sandipan
# git config --global user.email sandipan.dey@gmail.com
# git commit -a
# git push origin master