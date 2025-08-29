As before, start by copying what you did in the previous assignment to use
as a starting point for this assignment: run setup.sh by right clicking
it from the file list on the left and choosing "Run Code".

Now you are ready to read the category lists. If you look in the file animal.txt,
you will see that it contains

cat
dog
bat
chicken
worm
dragon
frog
fruit fly
butterfly
mouse

These are the possible replacements we have provided for the "animal" category (blanks
that are _animal).

For this assignment, there are a few things that need to happen, and we recommend breaking
them down into their own functions and testing each before you move on.

First, we recommend writing a function readWordList(categoryname).   This function
takes a category name (like "animal"), appends ".txt" to it, and reads the appropriate file.
It then returns a list with the possible words for that category, such as

["cat", "dog", "bat", "chicken", "worm", "dragon", "frog", "fruit fly", "butterfly", "mouse"]

Note that if you iterate over the lines in the file, each one will have a newline
on the end ("\n") that you will need to take off as you put them into the list.

Once you have written this, test it out and make sure you are happy with the results.


The next step we recommend is to write a function buildCategories which takes a list
of categories (like ["animal", "place", "food"]) and returns a dictionary which maps
each cateogry name to the list of words for that category, like

 { "animal" : ["cat", "dog", "bat", "chicken", "worm", "dragon",
               "frog", "fruit fly", "butterfly", "mouse"],
   "place"  : ["castle", "cave", "pond", "tower", "house", "forest",
               "city", "space station", "theater", "hotel", "dive bar"],
   "food"   : ["pizza", "cupcake", "pineapple", "chocolate cookie",
               "gyro", "lamb kebab", "falafel", "roast duck"] }

Note that this can be a great use of a dictionary comprehension (though
you can certainly do it without one).  As always, test this function out before
you move on!


Now you are ready to modify the randomStory function to make use of the categories.
Recall that the randomStory function takes a second parameter (which you have not
been using so far), wordTypes.   Now is the time to use it.  Inside of your randomStory
function, you can pass wordTypes to buildCategories to make the dictionary you will need
for word replacement.  Next, you can modify the part of your code that handles word
blanks (currently it just appends something like [ word animal ] to the output) to choose
an appropriate replacement.  Note that in doing so, you have already written the code
to find the category name (like "animal") and should have that readily available.

Also note that random.choice(lst) is a useful Python function which will choose a random
element from a list.  You will want to import random if you wish to use this function.

Note that we cannot provide you with one correct output to compare against,
as your program makes random choices---there are many possible correct outputs.
However, we have provided example_output.txt which shows what the output
looks like for one random selection.
