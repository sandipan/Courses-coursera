best <- function(state, outcome) {
	## Read outcome data
	out <- read.csv("data3/outcome-of-care-measures.csv", colClasses = "character")
	out[, 11] <- suppressWarnings(as.numeric(out[, 11]))
	out[, 17] <- suppressWarnings(as.numeric(out[, 17]))
	out[, 23] <- suppressWarnings(as.numeric(out[, 23]))
	## Check that state and outcome are valid
	if (!(state %in% out$State)) {
		#message(paste("Error in best(\"", state, "\", \"", outcome, "\"): invalid state", sep="")) and return
		stop("invalid state")
	}
	if (!(outcome %in% c("heart attack", "heart failure", "pneumonia"))) {
		stop("invalid outcome")
	}
	## Return hospital name in that state with lowest 30-day death
	sout <- subset(out, State == state)
	if (outcome == "heart attack") {
		#return(sout[order(sout$Number.of.Patients...Hospital.30.Day.Death..Mortality..Rates.from.Heart.Attack),]$Hospital.Name[1])
		return(sout[order(sout[,11]),]$Hospital.Name[1])
	}
	else if (outcome == "heart failure") {
		#return(sout[order(as.integer(sout$Number.of.Patients...Hospital.30.Day.Death..Mortality..Rates.from.Heart.Failure)),]$Hospital.Name[1])
		return(sout[order(sout[,17]),]$Hospital.Name[1])
	}
	else {
		#return(sout[order(as.integer(sout$Number.of.Patients...Hospital.30.Day.Death..Mortality..Rates.from.Pneumonia)),]$Hospital.Name[1])
		return(sout[order(sout[,23]),]$Hospital.Name[1])
	}
	## rate
}