Reproducible Research Assignment 1
========================================================

Introduction
------------

It is now possible to collect a large amount of data about personal movement using activity monitoring devices such as a Fitbit, Nike Fuelband, or Jawbone Up. These type of devices are part of the "quantified self" movement - a group of enthusiasts who take measurements about themselves regularly to improve their health, to find patterns in their behavior, or because they are tech geeks. But these data remain under-utilized both because the raw data are hard to obtain and there is a lack of statistical methods and software for processing and interpreting the data.

This assignment makes use of data from a personal activity monitoring device. This device collects data at 5 minute intervals through out the day. The data consists of two months of data from an anonymous individual collected during the months of October and November, 2012 and include the number of steps taken in 5 minute intervals each day.

Data
-----

The data for this assignment can be downloaded from the course web site:

*Dataset: Activity monitoring data [52K]

The variables included in this dataset are:

*steps: Number of steps taking in a 5-minute interval (missing values are coded as NA)
*date: The date on which the measurement was taken in YYYY-MM-DD format
*interval: Identifier for the 5-minute interval in which measurement was taken

The dataset is stored in a comma-separated-value (CSV) file and there are a total of 17,568 observations in this dataset.

Assignment
----------

This assignment will be described in multiple parts. You will need to write a report that answers the questions detailed below. Ultimately, you will need to complete the entire assignment in a single R markdown document that can be processed by knitr and be transformed into an HTML file.

Throughout your report make sure you always include the code that you used to generate the output you present. When writing code chunks in the R markdown document, always use echo = TRUE so that someone else will be able to read the code. This assignment will be evaluated via peer assessment so it is essential that your peer evaluators be able to review the code for your analysis.

For the plotting aspects of this assignment, feel free to use any plotting system in R (i.e., base, lattice, ggplot2)

Fork/clone the GitHub repository created for this assignment. You will submit this assignment by pushing your completed files into your forked repository on GitHub. The assignment submission will consist of the URL to your GitHub repository and the SHA-1 commit ID for your repository state.

NOTE: The GitHub repository also contains the dataset for the assignment so you do not have to download the data separately.

Loading and preprocessing the data
----------------------------------
Show any code that is needed to

* Load the data (i.e. read.csv())
* Process/transform the data (if necessary) into a format suitable for your analysis


```r
activity <- read.csv("activity.csv")
names(activity)
```

```
## [1] "steps"    "date"     "interval"
```

```r
head(activity)
```

```
##   steps       date interval
## 1    NA 2012-10-01        0
## 2    NA 2012-10-01        5
## 3    NA 2012-10-01       10
## 4    NA 2012-10-01       15
## 5    NA 2012-10-01       20
## 6    NA 2012-10-01       25
```

```r
#remove all NA's
activity_no_na <- activity[!is.na(activity$steps),]
head(activity_no_na)
```

```
##     steps       date interval
## 289     0 2012-10-02        0
## 290     0 2012-10-02        5
## 291     0 2012-10-02       10
## 292     0 2012-10-02       15
## 293     0 2012-10-02       20
## 294     0 2012-10-02       25
```

What is mean total number of steps taken per day?
-------------------------------------------------
For this part of the assignment, you can ignore the missing values in the dataset.

* Make a histogram of the total number of steps taken each day
* Calculate and report the mean and median total number of steps taken per day


```r
number_of_steps <- tapply(activity_no_na$steps, activity_no_na$date, sum)
number_of_steps <- number_of_steps[!is.na(number_of_steps)]
hist(number_of_steps, col=rainbow(10))
```

![plot of chunk unnamed-chunk-2](figure/unnamed-chunk-2.png) 

```r
mean(number_of_steps)
```

```
## [1] 10766
```

```r
median(number_of_steps)
```

```
## [1] 10765
```

```r
summary(number_of_steps)
```

```
##    Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
##      41    8840   10800   10800   13300   21200
```

What is the average daily activity pattern?
-------------------------------------------
*Make a time series plot (i.e. type = "l") of the 5-minute interval (x-axis) and the average number of steps taken, averaged across all days (y-axis)
*Which 5-minute interval, on average across all the days in the dataset, contains the maximum number of steps?


```r
mean_steps_interval <- tapply(activity_no_na$steps, activity_no_na$interval, mean)
plot(mean_steps_interval, type="l")
```

![plot of chunk unnamed-chunk-3](figure/unnamed-chunk-3.png) 

```r
max(mean_steps_interval)
```

```
## [1] 206.2
```

```r
which.max(mean_steps_interval)
```

```
## 835 
## 104
```

Imputing missing values
-----------------------
Note that there are a number of days/intervals where there are missing values (coded as NA). The presence of missing days may introduce bias into some calculations or summaries of the data.

*Calculate and report the total number of missing values in the dataset (i.e. the total number of rows with NAs)
*Devise a strategy for filling in all of the missing values in the dataset. The strategy does not need to be sophisticated. For example, you could use the mean/median for that day, or the mean for that 5-minute interval, etc.
*Create a new dataset that is equal to the original dataset but with the missing data filled in.
*Make a histogram of the total number of steps taken each day and Calculate and report the mean and median total number of steps taken per day. Do these values differ from the estimates from the first part of the assignment? What is the impact of imputing missing data on the estimates of the total daily number of steps?


```r
nrow(activity[is.na(activity),])
```

```
## [1] 2304
```

```r
nrow(activity[is.na(activity$steps),])
```

```
## [1] 2304
```

```r
intervals <- unique(activity$interval)
new_activity <- activity
for (int in intervals) {
  num_missing <- nrow(new_activity[new_activity$interval == int & is.na(new_activity$steps),])
  if (num_missing > 0) {
    new_activity[new_activity$interval == int & is.na(new_activity$steps),]$steps <- rep(mean_steps_interval[as.character(int)], num_missing)
  }
}
head(new_activity)
```

```
##     steps       date interval
## 1 1.71698 2012-10-01        0
## 2 0.33962 2012-10-01        5
## 3 0.13208 2012-10-01       10
## 4 0.15094 2012-10-01       15
## 5 0.07547 2012-10-01       20
## 6 2.09434 2012-10-01       25
```

```r
new_number_of_steps <- tapply(new_activity$steps, new_activity$date, sum)
hist(new_number_of_steps, col=rainbow(10))
```

![plot of chunk unnamed-chunk-4](figure/unnamed-chunk-4.png) 

```r
mean(new_number_of_steps)
```

```
## [1] 10766
```

```r
median(new_number_of_steps)
```

```
## [1] 10766
```

```r
summary(new_number_of_steps)
```

```
##    Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
##      41    9820   10800   10800   12800   21200
```

```r
sum(number_of_steps)
```

```
## [1] 570608
```

```r
sum(new_number_of_steps)
```

```
## [1] 656738
```
Are there differences in activity patterns between weekdays and weekends?
-------------------------------------------------------------------------
For this part the weekdays() function may be of some help here. Use the dataset with the filled-in missing values for this part.

*Create a new factor variable in the dataset with two levels - "weekday" and "weekend" indicating whether a given date is a weekday or weekend day.
*Make a panel plot containing a time series plot (i.e. type = "l") of the 5-minute interval (x-axis) and the average number of steps taken, averaged across all weekday days or weekend days (y-axis). The plot should look something like the following, which was creating using simulated data:

```r
new_activity$weekday_or_weekend <- ifelse(weekdays(as.Date(new_activity$date)) %in% c("Saturday", "Sunday"), "weekend", "weekday")  
new_activity_weekday <- new_activity[new_activity$weekday_or_weekend == "weekday",]
mean_steps_weekday <- tapply(new_activity_weekday$steps, new_activity_weekday$interval, mean)
new_activity_weekend <- new_activity[new_activity$weekday_or_weekend == "weekend",]
mean_steps_weekend <- tapply(new_activity_weekend$steps, new_activity_weekend$interval, mean)
par(mfrow=c(2,1))
plot(mean_steps_weekday, type="l", xlab="intervals")
plot(mean_steps_weekend, type="l", xlab="intervals")
```

![plot of chunk unnamed-chunk-5](figure/unnamed-chunk-5.png) 

```r
#library (lattice)
#xyplot (mean_steps_weekday, data=new_activity, type="o",
#        layout=c(1, 2), as.table=T) #, xlab="Time (secs)", ylab="Price")
```
