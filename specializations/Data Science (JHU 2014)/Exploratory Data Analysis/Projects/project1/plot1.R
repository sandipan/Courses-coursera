# read the text file (renamed as hpc.txt)
hpc <- read.table("hpc.txt", header=TRUE, sep=";")
hpc$Date <- strptime(hpc$Date, '%d/%m/%Y')
hpc$Date <- as.Date(hpc$Date)
shpc <- subset(hpc, hpc$Date >= as.Date("2007-02-01") & hpc$Date <= as.Date("2007-02-02"))

# plot
shpc$Global_active_power <- as.numeric(as.character(shpc$Global_active_power))
png(filename = "plot1.png", width = 480, height = 480)
hist(shpc$Global_active_power, col="red", xlab="Global Active Power (kilowatts)", main="Global Active Power")
dev.off()