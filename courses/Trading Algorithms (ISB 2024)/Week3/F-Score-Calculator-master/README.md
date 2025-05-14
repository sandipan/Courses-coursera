# F-Score calculator
 A python program that pulls financial statement data of companies from a selected API and then calculates the f-score of each company for the specified year. 

## Inspiration 
I have always been interested in value investing having been an avid follower of Warren Buffet and Benjamin Graham. However having a technical way of thinking, I could never connect all the dots on how to evaluate if a company is over or undervalued. I have spent many nights educating myself about finance and valuation, I have never had any formal education in either. On one of these nights, I came across the Piotroski F-score. I was intrigued by the methodolgy and wanted to learn more about. So i found the original paper published by Professor Joseph Piotroski and set out to create a python based program that could analyze and visualize the results. 

## Design and Implementation 
The design of the program is very simple. It takes an excel file of short listed stock tickers, based on some screening criteria, checks if the financial statement are available from the api I am using, short lists them again based on information availability, retrieves the data, calulcates the required financial metrics from the data and then finally saves the company info along with the individual metrics and the calculated f-score in an excel file. I can then use this data however I please. 

## Results
I didn't get any conclusive results from the companies I have analyzed so far, this could be due to some issues that I will discuss later. Overall, this was a much needed lesson in reading and analyzing financial statements as well as re-sharpening my python skills since it had been a while since I programmed in python.  

## Final Thoughts 
I believe I can draw better conclusions if my data set includes a larger number of companies. For my initial runs I shortlisted about 300 tickers of which by the time I get to analysis, I only have 30 available. I also intend to make this part of a larger set of investment analysis tools that will include DCF analysis and various other valuation methods. I am interested in this as a part of a long term investing strategy that incorporates LEAPS. However, this is just a hobby and as life picks up it gets put on the sidelines. Keep tuned for updates. Criticism and suggestions are always welcomed.  
