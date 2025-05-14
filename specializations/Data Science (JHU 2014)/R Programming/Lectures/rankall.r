rankall <- function(outcome, num = "best") {
	## Read outcome data
	out <- read.csv("data3/outcome-of-care-measures.csv", colClasses = "character")
	out[, 11] <- suppressWarnings(as.numeric(out[, 11]))
	out[, 17] <- suppressWarnings(as.numeric(out[, 17]))
	out[, 23] <- suppressWarnings(as.numeric(out[, 23]))
	## Check that outcome is valid
	if (!(outcome %in% c("heart attack", "heart failure", "pneumonia"))) {
		stop("invalid outcome")
	}
	## For each state, find the hospital of the given rank
	column <- ifelse(outcome == "heart attack", 11, ifelse(outcome == "heart failure", 17, 23))
	dfhosstate <- NULL 
	for (state in unique(out$State)) {
		sout <- subset(out, State == state)
		sout <- sout[!is.na(sout[,column]),]
		total <- nrow(sout)
		hospital <- NA
		r <- ifelse(num == "best", 1, ifelse(num == "worst", total, num))
		if ((r >= 1) & (r <= total)) {
			hospital <- sout[order(sout[,column],sout[,2]),]$Hospital.Name[r]
		}
		dfhosstate <- rbind(dfhosstate, data.frame(hospital=hospital, state=state))
	}
	dfhosstate <- dfhosstate[order(as.character(dfhosstate$state)),]
	rownames(dfhosstate) <- dfhosstate$state
	## Return a data frame with the hospital names and the
	## (abbreviated) state name
	return(dfhosstate)
}
