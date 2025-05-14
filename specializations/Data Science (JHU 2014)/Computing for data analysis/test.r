checkSanity <- function() {
	if(!file.exists("specdata"))
			stop("directory 'specdata' not found; please change your working directory")
	if(!file.exists("getmonitor.R"))
			stop("file 'getmonitor.R' not found; please change your working directory or name your code file accordingly")
	source("getmonitor.R", local = TRUE)
	if(!exists("getmonitor"))
			stop("function 'getmonitor' cannot be found")
}       

getmonitor.testscript <- function() {
	checkSanity()
	outputfiles <- sprintf("getmonitor-testoutput%d.txt", 1:2)
	op <- options(); options(scipen = 4); on.exit(options(op))

	## cat("sourcing 'getmonitor.R'\n")
	source("getmonitor.R", local = TRUE)

	data <- getmonitor(1, "specdata")
	s1 <- as.character(as.numeric(summary(data$nitrate)))
				   
	capture.output(data <- getmonitor(101, "specdata", TRUE))
	s2 <- as.character(as.numeric(summary(data$sulfate)))
	writeLines(c(s1, s2), outputfiles[1])

	data <- getmonitor("200", "specdata")
	qq <- quantile(data$nitrate, c(0.25, 0.75), na.rm = TRUE)

	data <- getmonitor(25, "specdata")
	set.seed(2)
	h <- head(data[sample(nrow(data)), ])
	s <- as.character(h[1, 2:3])
	writeLines(c(qq, s), outputfiles[2])

	cat("please upload the files\n\t", paste(outputfiles, collapse = "\n\t"), "\nto the Coursera web site\n", sep = "")
	return(invisible())
}

local({
        checkSanity <- function() {
                if(!file.exists("specdata"))
                        stop("directory 'specdata' not found; please change your working directory")
                if(!file.exists("getmonitor.R"))
                        stop("file 'getmonitor.R' not found; this file is needed to run these tests; please change your working directory or name your code file accordingly")
                if(!file.exists("complete.R"))
                        stop("file 'complete.R' not found; please change your working directory or name your code file accordingly")
                source("getmonitor.R", local = TRUE)
                if(!exists("getmonitor"))
                        stop("function 'getmonitor' cannot be found")
                source("complete.R", local = TRUE)
                if(!exists("complete"))
                        stop("function 'complete' cannot be found")
        }
        complete.testscript <- function() {
                checkSanity()
                outputfiles <- sprintf("complete-testoutput%d.txt", 1:3)

                op <- options(); options(scipen = 4); on.exit(options(op))

                source("getmonitor.R", local = TRUE)
                source("complete.R", local = TRUE)

                ## Run all monitors
                cc <- complete("specdata", 332:1)
                stopifnot(all(names(cc) %in% c("id", "nobs")))
                cc$id <- as.integer(cc$id)
                cc <- cc[order(cc$id), ]
                set.seed(248)
                out <- as.numeric(head(cc[sample(332, 10), "nobs"]))
                writeLines(as.character(out), outputfiles[1])

                ## Single monitor
                cc <- complete("specdata", 24)
                writeLines(as.character(as.numeric(cc$nobs)), outputfiles[2])

                ## Subset
                set.seed(42)
                cc <- complete("specdata", sample(332, 10))
                cc$id <- as.integer(cc$id)
                cc <- cc[order(cc$id), ]
                out <- c(as.numeric(cc$id), as.numeric(cc$nobs))
                writeLines(as.character(out), outputfiles[3])

                cat("please upload the files\n\t", paste(outputfiles, collapse = "\n\t"), "\nto the Coursera web site\n", sep = "")
                return(invisible())
        }
        assign("complete.testscript", complete.testscript, globalenv())
})

local({
        checkSanity <- function() {
                if(!file.exists("specdata"))
                        stop("directory 'specdata' not found; please change your working directory")
                if(!file.exists("getmonitor.R"))
                        stop("file 'getmonitor.R' not found; please change your working directory or name your code file accordingly")
                if(!file.exists("complete.R"))
                        stop("file 'complete.R' not found; please change your working directory or name your code file accordingly")
                if(!file.exists("corr.R"))
                        stop("file 'corr.R' not found; please change your working directory or name your code file accordingly")
                source("getmonitor.R", local = TRUE)
                if(!exists("getmonitor"))
                        stop("function 'getmonitor' cannot be found")
                source("complete.R", local = TRUE)
                if(!exists("complete"))
                        stop("function 'complete' cannot be found")
                source("corr.R", local = TRUE)
                if(!exists("corr"))
                        stop("function 'corr' cannot be found")
        }
        corr.testscript <- function() {
                checkSanity()
                outputfiles <- sprintf("corr-testoutput%d.txt", 1:3)
                op <- options(); options(scipen = 4); on.exit(options(op))

                source("getmonitor.R", local = TRUE)
                source("complete.R", local = TRUE)
                source("corr.R", local = TRUE)

                ## Run all
                cr <- corr("specdata")
                cr <- sort(cr)
                set.seed(868)
                out <- round(cr[sample(length(cr), 5)], 4)
                writeLines(as.character(out), outputfiles[1])

                ## Threshold
                cr <- corr("specdata", 129)
                cr <- sort(cr)
                n <- length(cr)
                set.seed(197)
                out <- c(n, round(cr[sample(n, 5)], 4))
                writeLines(as.character(out), outputfiles[2])

                ## High Threshold
                cr <- corr("specdata", 2000)
                n <- length(cr)
                cr <- corr("specdata", 1000)
                cr <- sort(cr)
                writeLines(as.character(c(n, round(cr, 4))), outputfiles[3])

                cat("please upload the files\n\t", paste(outputfiles, collapse = "\n\t"), "\nto the Coursera web site\n", sep = "")
                return(invisible())
        }
        assign("corr.testscript", corr.testscript, globalenv())
})