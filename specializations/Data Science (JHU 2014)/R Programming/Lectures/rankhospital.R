rankhospital <- function(state, outcome, num = "best") {
	## Read outcome data
	out <- read.csv("data3/outcome-of-care-measures.csv", colClasses = "character")
	out[, 11] <- suppressWarnings(as.numeric(out[, 11]))
	out[, 17] <- suppressWarnings(as.numeric(out[, 17]))
	out[, 23] <- suppressWarnings(as.numeric(out[, 23]))
	## Check that state and outcome are valid
	if (!(state %in% out$State)) {
		stop("invalid state")
	}
	if (!(outcome %in% c("heart attack", "heart failure", "pneumonia"))) {
		stop("invalid outcome")
	}
	## Return hospital name in that state with the given rank
	column <- ifelse(outcome == "heart attack", 11, ifelse(outcome == "heart failure", 17, 23))
	sout <- subset(out, State == state)
	sout <- sout[!is.na(sout[,column]),]
	total <- nrow(sout)
	if (num == "best") {
		num <- 1
	} 
	else if (num == "worst") {
		num <- total
	}
	else if (num < 1 | num > total) {
		return (NA)
	}
	#print(sout[order(sout[,column],sout[,2]),][,c(2,column)][1:num,])
	## 30-day death rate
	return(sout[order(sout[,column],sout[,2]),]$Hospital.Name[num])
}