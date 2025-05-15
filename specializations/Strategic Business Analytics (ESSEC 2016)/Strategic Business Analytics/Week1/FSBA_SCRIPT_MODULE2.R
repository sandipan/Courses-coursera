############################################################
#     Foundation to Strategic Business Analytics           #
#       Module 2 - Finding groups within data        			 #
#                                                  				 #
#                                                          #
# 	Author: Nicolas Glady & Pauline Glikman                #
#                   ESSEC BUSINESS SCHOOL                  #
############################################################

############################################################
# Disclaimer: this script is used to produce the examples  #
#  presented during the course Strategic Business          #
#  Analytics. The author is not responsible in any way     #
#  for any problem encountered during this code execution. #
############################################################

############################################################
####        EXAMPLE N°1 - STOCK KEEPING UNIT            ####
############################################################
# Set your directory to the folder where you have downloaded the SKU dataset
setwd('C:/courses/Coursera/Current/Strategic Business Analytics/Week1')

# To clean up the memory of your current R session run the following line
rm(list=ls(all=TRUE))

# Let's load our dataset
data=read.table('DATA_2.01_SKU.csv', header = T,sep=',') # The function read.table enables us to read flat files such as .csv files

# Now let's have a look at our variables and see some summary statistics
str(data) # The str() function shows the structure of your dataset and details the type of variables that it contains
summary(data) # The summary() function provides for each variable in your dataset the minimum, mean, maximum and quartiles

# Let's plot our data to see if we can identify groups visually 
plot(data$CV, data$ADS, main = "SKU Example", ylab="Average Daily Sales", xlab= "Coefficient of Variation")
abline(v=0.2, col = "red") # we can draw a vertical line by using the abline function and passing it the v argument
abline(h=4, col="red") # we can draw a horizontal line by using the abline function and passing it the h argument
text(0.15,9.7, "Horses", col = "red") # we can add some text to our plot by using the text() function, here to label the group "Horses"
text(0.65,9, "Wild Bulls", col = "red") # and group "Wild Bulls"
text(0.8,2, "Crickets", col = "red") # and group "Crickets"


# Let's find groups using hierarchical clustering and check if we obtain similar results
testdata=data  # To keep our dataset safe, let's create a copy of it called "testdata"
testdata = scale(testdata) # To keep our dataset safe, let's create a copy of it called "testdata"

d = dist(testdata, method = "euclidean") # the dist() function computes the distances of all the observations in our dataset
hcward = hclust(d, method="ward.D") # hclust() function performs hiearchical clustering, we pass it the distances, and we set the method argument to "ward.D"

#data$groups<-cutree(hcward,k=3) # assign our points to our k=3 clusters 
data$groups<-cutree(hcward,k=2) # assign our points to our k=2 clusters 

# The lattice library provides a complete set of functions for producing advanced plots.
#install.packages("lattice") #install the lattice package by using the install.packages() function
library(lattice) # load the lattice package by using the library() function and passing it the name of the package you wish to load
xyplot(ADS~ CV,main = "After Clustering", type="p",group=groups,data=data, # define the groups to be differentiated 
       auto.key=list(title="Group", space = "left", cex=1.0, just = 0.95), # to produce the legend we use the auto.key= list() 
       par.settings = list(superpose.line=list(pch = 0:18, cex=1)), # the par.settings argument allows us to pass a list of display settings
       col=c('blue','green','red')) # finally we choose the colour of our plotted points per group


###########################################################
####     EXAMPLE N°2 - HUMAN RESSOURCES ANALYTICS      ####
###########################################################

# Set your directory to the folder where you have downloaded the HR dataset 

# To clean up the memory of your current R session run the following line
rm(list=ls(all=TRUE))

# Let's load our dataset and call it data
data=read.table('DATA_2.02_HR.csv',header = T,sep=',') # The function read.table enables us to read flat files such as .csv files

# Now let's have a look at our variables and see some summary statistics
str(data) # The str() function shows the structure of your dataset and details the type of variables that it contains
summary(data) # The summary() function provides for each variable in your dataset the minimum, mean, maximum and quartiles

plot(data$NP, data$LPE)
plot(data$LPE, data$NP)

# Now let's normalize our variables
testdata=data # To keep our dataset safe, let's create a copy of it called "testdata"
testdata = scale(testdata) # the scale function automatically performs data normalization on all your variables

testdata = testdata[,1:3]

d = dist(testdata, method = "euclidean") # the dist() function computes the distances of all the observations in our dataset
hcward = hclust(d, method="ward.D") # hclust() function performs hiearchical clustering, we pass it the distances, and we set the method argument to "ward.D"

#data$groups = cutree(hcward,k=4) # assign our points to our k=4 clusters 
data$groups = cutree(hcward,k=2) # assign our points to our k=4 clusters 

aggdata = aggregate(.~ groups, data=data, FUN=mean) # The aggregate() function presents a summary of a statistic, broken down by one or more groups. Here we compute the mean of each variable for each group. 

aggdata = aggregate(.~ groups, data=data, FUN=median) # The aggregate() function presents a summary of a statistic, broken down by one or more groups. Here we compute the mean of each variable for each group. 

# One thing we would like to have is the proportion of our data that is in each cluster
proptemp=aggregate(S~ groups, data=data, FUN=length) # we create a variable called proptemp which computes the number of observations in each group (using the S variable, but you can take any.)
aggdata$proportion=(proptemp$S)/sum(proptemp$S) # proportion of observations in each group we compute the ratio between proptemp and the total number of observations
aggdata=aggdata[order(aggdata$proportion,decreasing=T),] # Let's order the groups from the larger to the smaller

# Let's see the output by calling our aggdata variable
aggdata

# As discussed in the videos, let's remove the Newborn variable, which is not really relevant and by being a dummy drives the clustering too much...
testdata=data[,1:5] # we create a new dataset, called "testdata" includes all the rows and the 5 first columns of our original dataset 

# We then rerun the code used above
testdata = scale(testdata) # We normalize again our original variables
d = dist(testdata, method = "euclidean") # We compute the distances between observations
hcward = hclust(d, method="ward.D") # Hiearchical Clustering using Ward criterion

data$groups = cutree(hcward,k=4) # Create segments for k=4
# Note that we re-use the original dataset "data" (where the variable Newborn is still present) and not "testdata" (where the variable Newborn has been removed)
# Hence we'll be able to produce summary statistics also for the Newborn variable regardless it wasn't included when doing the second version of the clustering

aggdata = aggregate(.~ groups, data=data, FUN=mean) # Aggregate the values again

proptemp=aggregate(S~ groups, data=data, FUN=length)  # Compute the number of observations per group
aggdata$proportion=(proptemp$S)/sum(proptemp$S) # Compute the proportion
aggdata=aggdata[order(aggdata$proportion,decreasing=T),] # Let's order the groups from the larger to the smaller

# Let's see the output by calling our aggdata variable
aggdata 

# To export the output of our result, we execute the following line using the write.table() function
# write.csv(aggdata, "HR_example_Numerical_Output.csv", row.names=FALSE)
# This allows to import the data in Excel for instance where we can prepare it for the presentation. E.g. change the name of the columns, use colours, etc.
# Instead of write.csv, you can also use write.csv2() if you encounter an error due to regional settings for separators


###########################################################
####        EXAMPLE N°3 - TELECOMMUNICATIONS           ####
###########################################################

# Set your directory to the folder where you have downloaded the Telco dataset 

# to clean up the memory of your current R session run the following line
rm(list=ls(all=TRUE))

# Let's load the data
data=read.table('DATA_2.03_Telco.csv', header = T,sep=',')# The function read.table enables us to read flat files such as .csv files

# Now let's have a look at our variables and see some summary statistics
str(data) # The str() function shows the structure of your dataset and details the type of variables that it contains
summary(data) # The summary() function provides for each variable in your dataset the minimum, mean, maximum and quartiles

# Now let's normalize our variables
testdata=data # To keep our dataset safe, let's create a copy of it called "testdata"
testdata = scale(testdata) # the scale function automatically performs data normalization on all your variables

d = dist(testdata, method = "euclidean") # the dist() function computes the distances of all the observations in our dataset
hcward = hclust(d, method="ward.D") # hclust() function performs hiearchical clustering, we pass it the distances, and we set the method argument to "ward.D"

data$groups=cutree(hcward,k=8) # assign our points to our k=8 clusters 
aggdata= aggregate(.~ groups, data=data, FUN=mean) # Aggregation by group and computation of the mean values
proptemp=aggregate(Calls~ groups, data=data, FUN=length) # Computation of the number of observations by group
aggdata$proportion=(proptemp$Calls)/sum(proptemp$Calls) # Computation of the proportion by group
aggdata=aggdata[order(aggdata$proportion,decreasing=T),] # Ordering from the largest group to the smallest


# Let's try again with 5 segments
data$groups= cutree(hcward,k=5) #Create segments for k=5
aggdata= aggregate(.~ groups, data=data, FUN=mean) # Aggregation by group and computation of the mean values
proptemp=aggregate(Calls~ groups, data=data, FUN=length) # Computation of the number of observations by group
aggdata$proportion=(proptemp$Calls)/sum(proptemp$Calls) # Computation of the proportion by group
aggdata=aggdata[order(aggdata$proportion,decreasing=T),] # Ordering from the largest group to the smallest

table(data$groups)

#write.csv(aggdata, file = "aggdataTelco5seg.csv", row.names=FALSE) # Let's save the output in a csv to work on it in Excel later

# Let's draw the radar chart with the function stars()
palette(rainbow(12, s = 0.6, v = 0.75)) # Select the colors to use
stars(aggdata[,2:(ncol(data))], len = 0.6, key.loc = c(11, 6),xlim=c(2,12),main = "Segments", draw.segments = TRUE,nrow = 2, cex = .75,labels=aggdata$groups)


