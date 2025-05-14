setwd("E:/Academics/Coursera/Data Cleaning/")
acs <- read.csv("getdata-data-ss06pid.csv")
sort(names(acs))
#head(acs)
library(sqldf)
sqldf("select pwgtp1 from acs where AGEP < 50")
identical(unique(acs$AGEP), sqldf("select distinct AGEP from acs")[,1])

page <- readLines("http://biostat.jhsph.edu/~jleek/contact.html")
page[c(10,20,30,100)]
nchar(page[c(10,20,30,100)])

d <- read.fwf("getdata-wksst8110.for", widths = c(-1, 9, -5, 8, -5, 8, -5, 8, -5, 8), header = FALSE, sep = "\t", skip = 4)
head(d)
d[,3] <- as.character(d[,3])
d[,3] <- as.numeric(substr(d[,3], 1, 4))
#d[,3] <- as.numeric(substr(d[,3], 1, 4)) - as.numeric(substr(d[,3], 5, 8))
sum(d[,3])

# github callback url: http://localhost:4567/callback

library(httr)
library(jsonlite)

#"https://api.github.com/users/jtleek/repos"

# 1. Find OAuth settings for github:
#    http://developer.github.com/v3/oauth/
oauth_endpoints("github")

# 2. Register an application at https://github.com/settings/applications
#    Insert your values below - if secret is omitted, it will look it up in
#    the GITHUB_CONSUMER_SECRET environmental variable.
#
#    Use http://localhost:1410 as the callback url

#Client ID: 1b8ef82086d54b72e360
#Client Secret: a367589f4571aeeacee8860e17ca88b8c955bf6f

#myapp <- oauth_app("github", "56b637a5baffac62cad9")
myapp <- oauth_app("github", "caa987d7a8f534f73bcd", "1bf375be71bbb7970cac6aec3d5f1642c89d7588")

# 3. Get OAuth credentials
github_token <- oauth2.0_token(oauth_endpoints("github"), myapp)
#github_token <- "b04a970bf622e0f78515030c5d20d747c9f5dbb0"

# 4. Use API
#req <- GET("https://api.github.com/rate_limit", config(token = github_token))
req <- GET("https://api.github.com/users/jtleek/repos", config(token = github_token))
#req <- GET("/repos/:jtleek/:repo", config(token = github_token))
stop_for_status(req)
out <- content(req)
#times <- c()
for (i in 1:(length(out))) {
	#print(paste(i, out[[i]]$name, out[[i]]$created_at))
	if (out[[i]]$name == "datasharing") {
		print(out[[i]]$created_at)
	}
	#times <- c(times, out[[i]]$created_at)
}
#print(times)
#min(times)
#do.call("rbind", lapply(content(req), as.data.frame))

