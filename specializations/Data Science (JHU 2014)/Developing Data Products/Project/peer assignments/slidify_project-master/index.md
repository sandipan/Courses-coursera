---
title       : Body Mass Index Calculator
subtitle    : A measurement of body fat based on height and weight 
author      : Huko Jack
framework   : io2012        # {io2012, html5slides, shower, dzslides, ...}
highlighter : highlight.js  # {highlight.js, prettify, highlight}
hitheme     : tomorrow      # 
widgets     : [mathjax]     # {mathjax, quiz, bootstrap}
mode        : selfcontained # {standalone, draft}
logo        : 1.png

---

## Overview

Obesity is a leading preventable cause of death worldwide, with increasing rates 
in adults and children. Authorities view it as one of the most serious public 
health problems of the 21st century. 

### Key facts:

1. Worldwide obesity has nearly doubled since 1980.
2. In 2008, more than 1.4 billion adults, 20 and older, were overweight. Of these over 200 million men and nearly 300 million women were obese.
3. 35% of adults aged 20 and over were overweight in 2008, and 11% were obese.
4. 65% of the world's population live in countries where overweight and obesity kills more people than underweight.
5. More than 40 million children under the age of five were overweight in 2011.

* Data from [The European Association for the Study of Obesity](http://easo.org/)

---

## Body Mass Index Calculator

We created an app to check body mass index and obesity status according to World 
Health Organization Classification$^1$. You can find this app here:

* [Body Mass Index Calculator](https://hukojack.shinyapps.io/course_project/)

This app:

* calculates body mass index using height, weight and sex information.
* prints how far from normal boundaries is it.
* prints state classification according to World Health Organization Database.
* draws a plot with obtained BMI, comparing to normal BMI. It also shows the boundaries that corresponds obesity/underveight classification.

$^1$ BMI Classification. Global Database on Body Mass Index. World Health Organization. 2006. 

---

## Output example - plot

![plot of chunk r_code](assets/fig/r_code.png) 


---

## Output example - summary

You Body Mass Index is:
```
[1] 32.0
```

How far from normal is it?
```
[1] "You BMI is 7.0 points higher than upper normal boundary."
```

Classification according to World Health Organization Database:
```
[1] "Overweight"
```
