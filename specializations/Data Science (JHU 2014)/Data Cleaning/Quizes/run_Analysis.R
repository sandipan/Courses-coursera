#setwd("C:/Users/pd/Desktop/sandipan/UCI HAR Dataset")

# Merges the training and the test sets to create one data set.
nFeatures = 561
X_train = read.table("train/X_train.txt", sep="", col.names=1:nFeatures, fill=FALSE, strip.white=TRUE)
X_test = read.table("test/X_test.txt", sep="", col.names=1:nFeatures, fill=FALSE, strip.white=TRUE)
X = rbind(X_train, X_test)
names(X) <- paste("F", 1:nFeatures, sep="_")
y_train = read.table("train/y_train.txt")
y_test = read.table("test/y_test.txt")
y = rbind(y_train, y_test)
names(y) <- "activity_id"
subject_train = read.table("train/subject_train.txt")
subject_test = read.table("test/subject_test.txt")
subject = rbind(subject_train, subject_test)
names(subject) <- "subject"
# Extracts only the measurements on the mean and standard deviation for each measurement. 
features = read.table("features.txt")
features = features[grepl("mean\\(\\)", features[,2]) | grepl("std\\(\\)", features[,2]),]
names(features) = c("id", "name")
X_ms = X[,features$id]
X_ms$subject = subject$subject

# Uses descriptive activity names to name the activities in the data set
activity_labels = read.table("activity_labels.txt")
names(activity_labels) <- c("activity_id", "name")

# Appropriately labels the data set with descriptive activity names. 
library(arules)
X_ms$activity <- decode(y, activity_labels$name)[[1]]

# Creates a second, independent tidy data set with the average of each variable for each activity and each subject. 
#tapply(X_ms[,1], X_ms$activity, mean)
library(data.table)
Xms <- data.table(X_ms)
out = Xms[, lapply(.SD, mean), by=c("subject","activity")]
out = out[order(out$subject),]
write.table(out, "second.txt", row.names=FALSE)
