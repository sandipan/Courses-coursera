
# PageRank
In this notebook, you'll build on your knowledge of eigenvectors and eigenvalues by exploring the PageRank algorithm.
The notebook is in two parts, the first is a worksheet to get you up to speed with how the algorithm works - here we will look at a micro-internet with fewer than 10 websites and see what it does and what can go wrong.
The second is an assessment which will test your application of eigentheory to this problem by writing code and calculating the page rank of a large network representing a sub-section of the internet.

## Part 1 - Worksheet
### Introduction

PageRank (developed by Larry Page and Sergey Brin) revolutionized web search by generating a
ranked list of web pages based on the underlying connectivity of the web. The PageRank algorithm is
based on an ideal random web surfer who, when reaching a page, goes to the next page by clicking on a
link. The surfer has equal probability of clicking any link on the page and, when reaching a page with no
links, has equal probability of moving to any other page by typing in its URL. In addition, the surfer may
occasionally choose to type in a random URL instead of following the links on a page. The PageRank is
the ranked order of the pages from the most to the least probable page the surfer will be viewing.



```python
# Before we begin, let's load the libraries.
%pylab notebook
import numpy as np
import numpy.linalg as la
from readonly.PageRankFunctions import *
np.set_printoptions(suppress=True)
```

    Populating the interactive namespace from numpy and matplotlib


### PageRank as a linear algebra problem
Let's imagine a micro-internet, with just 6 websites (**A**vocado, **B**ullseye, **C**atBabel, **D**romeda, **e**Tings, and **F**aceSpace).
Each website links to some of the others, and this forms a network as shown,

![A Micro-Internet](readonly/internet.png "A Micro-Internet")

The design principle of PageRank is that important websites will be linked to by important websites.
This somewhat recursive principle will form the basis of our thinking.

Imagine we have 100 *Procrastinating Pat*s on our micro-internet, each viewing a single website at a time.
Each minute the Pats follow a link on their website to another site on the micro-internet.
After a while, the websites that are most linked to will have more Pats visiting them, and in the long run, each minute for every Pat that leaves a website, another will enter keeping the total numbers of Pats on each website constant.
The PageRank is simply the ranking of websites by how many Pats they have on them at the end of this process.

We represent the number of Pats on each website with the vector,
$$\mathbf{r} = \begin{bmatrix} r_A \\ r_B \\ r_C \\ r_D \\ r_E \\ r_F \end{bmatrix}$$
And say that the number of Pats on each website in minute $i+1$ is related to those at minute $i$ by the matrix transformation

$$ \mathbf{r}^{(i+1)} = L \,\mathbf{r}^{(i)}$$
with the matrix $L$ taking the form,
$$ L = \begin{bmatrix}
L_{A→A} & L_{B→A} & L_{C→A} & L_{D→A} & L_{E→A} & L_{F→A} \\
L_{A→B} & L_{B→B} & L_{C→B} & L_{D→B} & L_{E→B} & L_{F→B} \\
L_{A→C} & L_{B→C} & L_{C→C} & L_{D→C} & L_{E→C} & L_{F→C} \\
L_{A→D} & L_{B→D} & L_{C→D} & L_{D→D} & L_{E→D} & L_{F→D} \\
L_{A→E} & L_{B→E} & L_{C→E} & L_{D→E} & L_{E→E} & L_{F→E} \\
L_{A→F} & L_{B→F} & L_{C→F} & L_{D→F} & L_{E→F} & L_{F→F} \\
\end{bmatrix}
$$
where the columns represent the probability of leaving a website for any other website, and sum to one.
The rows determine how likely you are to enter a website from any other, though these need not add to one.
The long time behaviour of this system is when $ \mathbf{r}^{(i+1)} = \mathbf{r}^{(i)}$, so we'll drop the superscripts here, and that allows us to write,
$$ L \,\mathbf{r} = \mathbf{r}$$

which is an eigenvalue equation for the matrix $L$, with eigenvalue 1 (this is guaranteed by the probabalistic structure of the matrix $L$).

Complete the matrix $L$ below, we've left out the column for which websites the *FaceSpace* website (F) links to.
Remember, this is the probability to click on another website from this one, so each column should add to one (by scaling by the number of links).


```python
# Replace the ??? here with the probability of clicking a link to each website when leaving Website F (FaceSpace).
L = np.array([[0,   1/2, 1/3, 0, 0,   0 ],
              [1/3, 0,   0,   0, 1/2, 0 ],
              [1/3, 1/2, 0,   1, 0,   1/2 ],
              [1/3, 0,   1/3, 0, 1/2, 1/2 ],
              [0,   0,   0,   0, 0,   0 ],
              [0,   0,   1/3, 0, 0,   0 ]])
```

In principle, we could use a linear algebra library, as below, to calculate the eigenvalues and vectors.
And this would work for a small system. But this gets unmanagable for large systems.
And since we only care about the principal eigenvector (the one with the largest eigenvalue, which will be 1 in this case), we can use the *power iteration method* which will scale better, and is faster for large systems.

Use the code below to peek at the PageRank for this micro-internet.


```python
eVals, eVecs = la.eig(L) # Gets the eigenvalues and vectors
order = np.absolute(eVals).argsort()[::-1] # Orders them by their eigenvalues
eVals = eVals[order]
eVecs = eVecs[:,order]

r = eVecs[:, 0] # Sets r to be the principal eigenvector
100 * np.real(r / np.sum(r)) # Make this eigenvector sum to one, then multiply by 100 Procrastinating Pats
```




    array([ 16.        ,   5.33333333,  40.        ,  25.33333333,
             0.        ,  13.33333333])



We can see from this list, the number of Procrastinating Pats that we expect to find on each website after long times.
Putting them in order of *popularity* (based on this metric), the PageRank of this micro-internet is:

**C**atBabel, **D**romeda, **A**vocado, **F**aceSpace, **B**ullseye, **e**Tings

Referring back to the micro-internet diagram, is this what you would have expected?
Convince yourself that based on which pages seem important given which others link to them, that this is a sensible ranking.

Let's now try to get the same result using the Power-Iteration method that was covered in the video.
This method will be much better at dealing with large systems.

First let's set up our initial vector, $\mathbf{r}^{(0)}$, so that we have our 100 Procrastinating Pats equally distributed on each of our 6 websites.


```python
r = 100 * np.ones(6) / 6 # Sets up this vector (6 entries of 1/6 × 100 each)
r # Shows it's value
```




    array([ 16.66666667,  16.66666667,  16.66666667,  16.66666667,
            16.66666667,  16.66666667])



Next, let's update the vector to the next minute, with the matrix $L$.
Run the following cell multiple times, until the answer stabilises.


```python
r = L @ r # Apply matrix L to r
r # Show it's value
# Re-run this cell multiple times to converge to the correct answer.
```




    array([ 13.88888889,  13.88888889,  38.88888889,  27.77777778,
             0.        ,   5.55555556])



We can automate applying this matrix multiple times as follows,


```python
r = 100 * np.ones(6) / 6 # Sets up this vector (6 entries of 1/6 × 100 each)
for i in np.arange(100) : # Repeat 100 times
    r = L @ r
r
```




    array([ 16.        ,   5.33333333,  40.        ,  25.33333333,
             0.        ,  13.33333333])



Or even better, we can keep running until we get to the required tolerance.


```python
r = 100 * np.ones(6) / 6 # Sets up this vector (6 entries of 1/6 × 100 each)
lastR = r
r = L @ r
i = 0
while la.norm(lastR - r) > 0.01 :
    lastR = r
    r = L @ r
    i += 1
print(str(i) + " iterations to convergence.")
r
```

    18 iterations to convergence.





    array([ 16.00149917,   5.33252025,  39.99916911,  25.3324738 ,
             0.        ,  13.33433767])



See how the PageRank order is established fairly quickly, and the vector converges on the value we calculated earlier after a few tens of repeats.

Congratulations! You've just calculated your first PageRank!

### Damping Parameter
The system we just studied converged fairly quickly to the correct answer.
Let's consider an extension to our micro-internet where things start to go wrong.

Say a new website is added to the micro-internet: *Geoff's* Website.
This website is linked to by *FaceSpace* and only links to itself.
![An Expanded Micro-Internet](readonly/internet2.png "An Expanded Micro-Internet")

Intuitively, only *FaceSpace*, which is in the bottom half of the page rank, links to this website amongst the two others it links to,
so we might expect *Geoff's* site to have a correspondingly low PageRank score.

Build the new $L$ matrix for the expanded micro-internet, and use Power-Iteration on the Procrastinating Pat vector.
See what happens…


```python
 # We'll call this one L2, to distinguish it from the previous L.
L2 = np.array([[0,   1/2, 1/3, 0, 0,   0, 0 ],
               [1/3, 0,   0,   0, 1/2, 0, 0 ],
               [1/3, 1/2, 0,   1, 0,   1/3, 0 ],
               [1/3, 0,   1/3, 0, 1/2, 1/3, 0 ],
               [0,   0,   0,   0, 0,   0, 0 ],
               [0,   0,   1/3, 0, 0,   0, 0 ],
               [0,   0,   0,   0, 0,   1/3, 1 ]])
```


```python
r = 100 * np.ones(7) / 7 # Sets up this vector (6 entries of 1/6 × 100 each)
lastR = r
r = L2 @ r
i = 0
while la.norm(lastR - r) > 0.01 :
    lastR = r
    r = L2 @ r
    i += 1
print(str(i) + " iterations to convergence.")
r
```

    131 iterations to convergence.





    array([  0.03046998,   0.01064323,   0.07126612,   0.04423198,
             0.        ,   0.02489342,  99.81849527])



That's no good! *Geoff* seems to be taking all the traffic on the micro-internet, and somehow coming at the top of the PageRank.
This behaviour can be understood, because once a Pat get's to *Geoff's* Website, they can't leave, as all links head back to Geoff.

To combat this, we can add a small probability that the Procrastinating Pats don't follow any link on a webpage, but instead visit a website on the micro-internet at random.
We'll say the probability of them following a link is $d$ and the probability of choosing a random website is therefore $1-d$.
We can use a new matrix to work out where the Pat's visit each minute.
$$ M = d \, L + \frac{1-d}{n} \, J $$
where $J$ is an $n\times n$ matrix where every element is one.

If $d$ is one, we have the case we had previously, whereas if $d$ is zero, we will always visit a random webpage and therefore all webpages will be equally likely and equally ranked.
For this extension to work best, $1-d$ should be somewhat small - though we won't go into a discussion about exactly how small.

Let's retry this PageRank with this extension.


```python
d = 0.5 # Feel free to play with this parameter after running the code once.
M = d * L2 + (1-d)/7 * np.ones([7, 7]) # np.ones() is the J matrix, with ones for each entry.
```


```python
r = 100 * np.ones(7) / 7 # Sets up this vector (6 entries of 1/6 × 100 each)
lastR = r
r = M @ r
i = 0
while la.norm(lastR - r) > 0.01 :
    lastR = r
    r = M @ r
    i += 1
print(str(i) + " iterations to convergence.")
r
```

    8 iterations to convergence.





    array([ 13.68217054,  11.20902965,  22.41964343,  16.7593433 ,
             7.14285714,  10.87976354,  17.90719239])



This is certainly better, the PageRank gives sensible numbers for the Procrastinating Pats that end up on each webpage.
This method still predicts Geoff has a high ranking webpage however.
This could be seen as a consequence of using a small network. We could also get around the problem by not counting self-links when producing the L matrix (an if a website has no outgoing links, make it link to all websites equally).
We won't look further down this route, as this is in the realm of improvements to PageRank, rather than eigenproblems.

You are now in a good position, having gained an understanding of PageRank, to produce your own code to calculate the PageRank of a website with thousands of entries.

Good Luck!

## Part 2 - Assessment
In this assessment, you will be asked to produce a function that can calculate the PageRank for an arbitrarily large probability matrix.
This, the final assignment of the course, will give less guidance than previous assessments.
You will be expected to utilise code from earlier in the worksheet and re-purpose it to your needs.

### How to submit
Edit the code in the cell below to complete the assignment.
Once you are finished and happy with it, press the *Submit Assignment* button at the top of this notebook.

Please don't change any of the function names, as these will be checked by the grading script.


```python
# PACKAGE
# Here are the imports again, just in case you need them.
# There is no need to edit or submit this cell.
import numpy as np
import numpy.linalg as la
from readonly.PageRankFunctions import *
np.set_printoptions(suppress=True)
```


```python
# GRADED FUNCTION
# Complete this function to provide the PageRank for an arbitrarily sized internet.
# I.e. the principal eigenvector of the damped system, using the power iteration method.
# (Normalisation doesn't matter here)
# The functions inputs are the linkMatrix, and d the damping parameter - as defined in this worksheet.
def pageRank(linkMatrix, d) :
    n = linkMatrix.shape[0]
    M = d * linkMatrix + (1-d)/n * np.ones([n, n]) # np.ones() is the J matrix, with ones for each entry.
    r = np.ones(n) / n #100 * np.ones(n) / n # Sets up this vector (6 entries of 1/6 × 100 each)
    lastR = r
    r = M @ r
    i = 0
    while la.norm(lastR - r) > 0.00001 :
        lastR = r
        r = M @ r
        i += 1
    print(str(i) + " iterations to convergence.")
    r
    return 100 * r
```

## Test your code before submission
To test the code you've written above, run the cell (select the cell above, then press the play button [ ▶| ] or press shift-enter).
You can then use the code below to test out your function.
You don't need to submit this cell; you can edit and run it as much as you like.


```python
# Use the following function to generate internets of different sizes.
generate_internet(5)
```

    /opt/conda/lib/python3.6/site-packages/numpy/core/numeric.py:301: FutureWarning: in the future, full([5, 5], array([0, 1, 2, 3, 4])) will return an array of dtype('int64')
      format(shape, fill_value, array(fill_value).dtype), FutureWarning)





    array([[ 1. ,  0.2,  0.2,  0. ,  0.2],
           [ 0. ,  0.2,  0.2,  0. ,  0.2],
           [ 0. ,  0.2,  0.2,  0. ,  0.2],
           [ 0. ,  0.2,  0.2,  0.5,  0.2],
           [ 0. ,  0.2,  0.2,  0.5,  0.2]])




```python
# Test your PageRank method against the built in "eig" method.
# You should see yours is a lot faster for large internets
L = generate_internet(10)
```

    /opt/conda/lib/python3.6/site-packages/numpy/core/numeric.py:301: FutureWarning: in the future, full([10, 10], array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])) will return an array of dtype('int64')
      format(shape, fill_value, array(fill_value).dtype), FutureWarning)



```python
pageRank(L, 1)
```

    14 iterations to convergence.





    array([  5.63382633,  14.0841178 ,   4.22531559,   2.81685314,
            16.90162611,  11.26772804,   2.81685314,  16.90176739,
             2.81685314,  22.53505931])




```python
# Do note, this is calculating the eigenvalues of the link matrix, L,
# without any damping. It may give different results that your pageRank function.
# If you wish, you could modify this cell to include damping.
# (There is no credit for this though)
eVals, eVecs = la.eig(L) # Gets the eigenvalues and vectors
order = np.absolute(eVals).argsort()[::-1] # Orders them by their eigenvalues
eVals = eVals[order]
eVecs = eVecs[:,order]

r = eVecs[:, 0]
100 * np.real(r / np.sum(r))
```




    array([  5.63380282,  14.08450703,   4.22535212,   2.81690141,
            16.90140845,  11.26760563,   2.81690141,  16.90140845,
             2.81690141,  22.53521126])




```python
# You may wish to view the PageRank graphically.
# This code will draw a bar chart, for each (numbered) website on the generated internet,
# The height of each bar will be the score in the PageRank.
# Run this code to see the PageRank for each internet you generate.
# Hopefully you should see what you might expect
# - there are a few clusters of important websites, but most on the internet are rubbish!
%pylab notebook
r = pageRank(generate_internet(100), 0.9)
plt.bar(arange(r.shape[0]), r);
```

    Populating the interactive namespace from numpy and matplotlib
    48 iterations to convergence.


    /opt/conda/lib/python3.6/site-packages/numpy/core/numeric.py:301: FutureWarning: in the future, full([100, 100], array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16,
           17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
           34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
           51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67,
           68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84,
           85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99])) will return an array of dtype('int64')
      format(shape, fill_value, array(fill_value).dtype), FutureWarning)



    <IPython.core.display.Javascript object>



<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAyAAAAJYCAYAAACadoJwAAAgAElEQVR4Xu3dbcys61kX/L9IocYmvAotWCkEtCUiuFtAaBAoRjEtkAgR89gYGqtQXp4KAbWKtkQRghFRE6CKAgm7mogopX5oAEEMRZKuFgqkjwZoeQsShQ8KRqDKk8s9m7269lrrnnOO45w5r7l/d1Ixe51zXOf8jmNmrv993TPzO+KHAAECBAgQIECAAAECZxL4HWc6jsMQIECAAAECBAgQIEAgAoghIECAAAECBAgQIEDgbAICyNmoHYgAAQIECBAgQIAAAQHEDBAgQIAAAQIECBAgcDYBAeRs1A5EgAABAgQIECBAgIAAYgYIECBAgAABAgQIEDibgAByNmoHIkCAAAECBAgQIEBAADEDBAgQIECAAAECBAicTUAAORu1AxEgQIAAAQIECBAgIICYAQIECBAgQIAAAQIEziYggJyN2oEIECBAgAABAgQIEBBAzAABAgQIECBAgAABAmcTEEDORu1ABAgQIECAAAECBAgIIGaAAAECBAgQIECAAIGzCQggZ6N2IAIECBAgQIAAAQIEBBAzQIAAAQIECBAgQIDA2QQEkLNROxABAgQIECBAgAABAgKIGSBAgAABAgQIECBA4GwCAsjZqB2IAAECBAgQIECAAAEBxAwQIECAAAECBAgQIHA2AQHkbNQORIAAAQIECBAgQICAAGIGCBAgQIAAAQIECBA4m4AAcjZqByJAgAABAgQIECBAQAAxAwQIECBAgAABAgQInE1AADkbtQMRIECAAAECBAgQICCAmAECBAgQIECAAAECBM4mIICcjdqBCBAgQIAAAQIECBAQQMwAAQIECBAgQIAAAQJnExBAzkbtQAQIECBAgAABAgQICCBmgAABAgQIECBAgACBswkIIGejdiACBAgQIECAAAECBAQQM0CAAAECBAgQIECAwNkEBJCzUTsQAQIECBAgQIAAAQICiBkgQIAAAQIECBAgQOBsAgLI2agdiAABAgQIECBAgAABAcQMECBAgAABAgQIECBwNgEB5GzUDkSAAAECBAgQIECAgABiBggQIECAAAECBAgQOJuAAHI2agciQIAAAQIECBAgQEAAMQMECBAgQIAAAQIECJxNQAA5G7UDESBAgAABAgQIECAggJgBAgQIECBAgAABAgTOJiCAnI3a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N7smQIAAAQGkYwYEkNMDyPZdIT+T5K1J/kiSdxxKffThk7D+2eHPs0b6JICMaFm7WwEBZLets3ECBAjcegHvAamPgAByf8MvTPKeSd4lyVckefPhTeXb6tcmecvhZi9P8nVJ3pDkXxy+wHD7b9t3gTz38M3oI10SQEa0rN2tgACy29bZOAECBG69gABSHwEB5P6Gb0/yQQ/gfUmSb7nr316cZPvejw9P8j+TfHeSVyT56RPaI4CcgOYm+xMQQPbXMzsmQIAAgccEBJD6JAggdcPOCgJIp6ZaywoIIMu2xsYIECBA4AYBAaQ+IgJI3bCzggDSqanWsgICyLKtsTECBAgQEECmz4AAMp146AACyBCXxXsVEED22jn7JkCAAAFXQOozIIDUDTsrCCCdmmotKyCALNsaGyNAgAABV0Cmz4AAMp146AACyBCXxXsVEED22jn7JkCAAAFXQOozIIDUDTsrCCCdmmotKyCALNsaGyNAgAABV0Cmz4AAMp146AACyBCXxXsVEED22jn7JkCAAAFXQOozIIDUDTsrCCCdmmotKyCALNsaGyNAgAABV0Cmz4AAMp146AACyBCXxXsVEED22jn7JkCAAAFXQOozIIDUDTsrCCCdmmotKyCALNsaGyNAgAABV0Cmz4AAMp146AACyBCXxXsVEED22jn7JkCAAAFXQOozIIDUDTsrCCCdmmotKyCALNsaGyNAgAABV0Cmz4AAMp146AACyBCXxXsVEED22jn7JkCAAAFXQOozIIDUDTsrCCCdmmotKyCALNsaGyNAgAABV0Cmz4AAMp146AACyBCXxXsVEED22jn7JkCAAAFXQOozIIDUDTsrCCCdmmotKyCALNsaGyNAgAABV0Cmz4AAMp146AACyBCXxXsVEED22jn7JkCAAAFXQOozIIDUDTsrCCCdmmotKyCALNsaGyNAgAABV0Cmz4AAMp146AACyBCXxXsVEED22jn7JkCAAAFXQOozIIDUDTsrCCCdmmotKyCALNsaGyNAgAABV0Cmz4AAMp146AACyBCXxXsVEED22jn7JkCAAAFXQOozIIDUDTsrCCCdmmotKyCALNsaGyNAgAABV0Cmz4AAMp146AACyBCXxXsVEED22jn7JkCAAAFXQOozIIDUDTsrCCCdmmotKyCALNsaGyNAgAABV0Cmz4AAMp146AACyBCX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8vakvH279vYnIttJrp91BLaPidy+JGv7E4F/cp9tbW+o3D4+efvR13X6dtNO7vcmdD28Se2y/779ydz2ZXXbh3X8i0Mo2f7b458+t30zuh5etkcPOvr2oSvff/gW++0LCbc3I29vQv+LSX4lyR9O8l/0b7nmbd+Z9J5Jtl/Ebe+l2355un3gw/azfarg478sHXntG1m7HMg1bEgAuYYunn4ftt8m/OXDb+y2Px34hcOfF2xvwnvH6WXdcoLA9qL5iQ+pu/12fVuz/ejrhAZMKvmgAKKHk8Cbyr748L0f23sJ/meS7RcA25+0bl/i+viPHjZhN5f5Q0n+ZpLnJdk+RXALHlv/to9SfvzTBD2PNqMXy23f17J9aev9frZfmn7LCa99Hp/FplRvLoBUBd2eAAECBAgQIECAAIGjBQSQo6ksJECAAAECBAgQIECgKiCAVAXdngABAgQIECBAgACBowUEkKOpLCRAgAABAgQIECBAoCoggFQF3Z4AAQIECBAgQIAAgaMFBJCjqSwkQIAAAQIECBAgQKAqIIBUBd2eAAECBAgQIECAAIGjBQSQo6ksJECAAAECBAgQIECgKiCAVAXdngABAgQIECBAgACBowUEkKOpLCRAgAABAgQIECBAoCoggFQF3Z4AAQIECBAgQIAAgaMFBJCjqSwkQIAAAQIECBAgQKAqIIBUBd2eAAECBAgQIECAAIGjBQSQo6ksJECAAAECBAgQIECgKiCAVAXdngABAgQIECBAgACBowUEkKOpLCRAgAABAgQIECBAoCoggFQF3Z4AAQIECBAgQIAAgaMFBJCjqSwkQIAAAQIECBAgQKAqIIBUBd2eAAECBAgQIECAAIGjBQSQo6ksJECAAAECBAgQIECgKiCAVAXdngABAgQIECBAgACBowUEkKOpLCRAgAABAgQIECBAoCoggFQF3Z4AAQIECBAgQIAAgaMFBJCjqSwkQIAAAQIECBAgQKAqIIBUBd2eAAECBAgQIECAAIGjBQSQo6ksJECAAAECBAgQIECgKiCAVAXdngABAgQIECBAgACBowUEkKOpLCRAgAABAgQIECBAoCoggFQF3Z4AAQIECBAgQIAAgaMFBJCjqSwkQIAAAQIECBAgQKAqIIBUBd2eAAECBAgQIECAAIGjBQSQo6ksJECAAAECBAgQIECgKiCAVAXdngABAgQIECBAgACBowUEkKOpLCRAgAABAgQIECBAoCoggFQF3Z4AAQIECBAgQIAAgaMFBJCjqSwkQIAAAQIECBAgQKAqIIBUBd2eAAECBAgQIECAAIGjBQSQo6ksJECAAAECBAgQIECgKiCAVAXdngABAgQIECBAgACBowUEkKOpLCRAgAABAgQIECBAoCrw/wMuL1pHoXdQEgAAAABJRU5ErkJggg==" width="640">



```python

```
