setwd("C:/Users/SANDIPAN DEY/Desktop/coursera/Reproducible Research/assignment1")


#Loading and preprocessing the data
#Show any code that is needed to
#1.Load the data (i.e. read.csv())
#2.Process/transform the data (if necessary) into a format suitable for your analysis
activity <- read.csv("activity.csv")
names(activity)
head(activity)
#remove all NA's
activity_no_na <- activity[!is.na(activity$steps),]
head(activity_no_na)

#What is mean total number of steps taken per day?
#For this part of the assignment, you can ignore the missing values in the dataset.
#1.Make a histogram of the total number of steps taken each day
#2.Calculate and report the mean and median total number of steps taken per day
number_of_steps <- tapply(activity_no_na$steps, activity_no_na$date, sum)
number_of_steps <- number_of_steps[!is.na(number_of_steps)]
hist(number_of_steps, col=rainbow(10))
mean(number_of_steps)
median(number_of_steps)
summary(number_of_steps)

#What is the average daily activity pattern?
#1.Make a time series plot (i.e. type = "l") of the 5-minute interval (x-axis) and the average number of steps taken, averaged across all days (y-axis)
#2.Which 5-minute interval, on average across all the days in the dataset, contains the maximum number of steps?activity <- read.csv("activity.csv")
mean_steps_interval <- tapply(activity_no_na$steps, activity_no_na$interval, mean)
plot(mean_steps_interval, type="l")
max(mean_steps_interval)
which.max(mean_steps_interval)

#Imputing missing values
#Note that there are a number of days/intervals where there are missing values (coded as NA). The presence of missing days may introduce bias into some calculations or summaries of the data.
#1.Calculate and report the total number of missing values in the dataset (i.e. the total number of rows with NAs)
#2.Devise a strategy for filling in all of the missing values in the dataset. The strategy does not need to be sophisticated. For example, you could use the mean/median for that day, or the mean for that 5-minute interval, etc.
#3.Create a new dataset that is equal to the original dataset but with the missing data filled in.
#4.Make a histogram of the total number of steps taken each day and Calculate and report the mean and median total number of steps taken per day. Do these values differ from the estimates from the first part of the assignment? What is the impact of imputing missing data on the estimates of the total daily number of steps?
nrow(activity[is.na(activity),])
nrow(activity[is.na(activity$steps),])
intervals <- unique(activity$interval)
new_activity <- activity
for (int in intervals) {
  num_missing <- nrow(new_activity[new_activity$interval == int & is.na(new_activity$steps),])
  if (num_missing > 0) {
    new_activity[new_activity$interval == int & is.na(new_activity$steps),]$steps <- rep(mean_steps_interval[as.character(int)], num_missing)
  }
}
head(new_activity)
new_number_of_steps <- tapply(new_activity$steps, new_activity$date, sum)
hist(new_number_of_steps, col=rainbow(10))
mean(new_number_of_steps)
median(new_number_of_steps)
summary(new_number_of_steps)
sum(number_of_steps)
sum(new_number_of_steps)

#Are there differences in activity patterns between weekdays and weekends?
#For this part the weekdays() function may be of some help here. Use the dataset with the filled-in missing values for this part.
#1.Create a new factor variable in the dataset with two levels - "weekday" and "weekend" indicating whether a given date is a weekday or weekend day.
#2.Make a panel plot containing a time series plot (i.e. type = "l") of the 5-minute interval (x-axis) and the average number of steps taken, averaged across all weekday days or weekend days (y-axis). The plot should look something like the following, which was creating using simulated data:
new_activity$weekday_or_weekend <- ifelse(weekdays(as.Date(new_activity$date)) %in% c("Saturday", "Sunday"), "weekend", "weekday")  
new_activity_weekday <- new_activity[new_activity$weekday_or_weekend == "weekday",]
mean_steps_weekday <- tapply(new_activity_weekday$steps, new_activity_weekday$interval, mean)
new_activity_weekend <- new_activity[new_activity$weekday_or_weekend == "weekend",]
mean_steps_weekend <- tapply(new_activity_weekend$steps, new_activity_weekend$interval, mean)
par(mfrow=c(2,1))
plot(mean_steps_weekday, type="l", xlab="intervals")
plot(mean_steps_weekend, type="l", xlab="intervals")
#library (lattice)
#xyplot (mean_steps_weekday, data=new_activity, type="o",
#        layout=c(1, 2), as.table=T) #, xlab="Time (secs)", ylab="Price")


