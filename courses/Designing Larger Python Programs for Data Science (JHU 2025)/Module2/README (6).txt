In this lab, we are going to take a moment away from building
up our Poker project, and see how we can use a little data
analysis on what we've done lately.  You'll get to use your
Panda skills to analyze some data that comes out of your
probability evaluation code.

First take a look at 4card_mc.csv.  This file has
147 hands, each with 4 cards, with the output
of running our probability simulation (from the last
assignment) for 10,000 draws on each of these 147
hands.  These hands are all made from a "base"
three card hand, plus one more card:
 As Ks Kh one more card
 8c 7c 6s one more card
 Kc 0c 4c one more card

where we have covered all possible values of "one more
card" for each hand.   That is, once As Ks and Kh
are drawn from the deck, there are 49 (52-3) other
cards remaining, so we have listed all possible 49
As Ks Kh (one more card) hands, and similarly for the
49 hands for 8c 7c 6s (one more card) and the 49
Kc 0c 4c (one more card) hands.

Suppose for a moment that you did not have the probability
calculator you just wrote, but had the data in 4card_mc.csv
Further suppose that you had a 3 card hand of As Ks Kh
(or 8c 7c 6s or Kc 0c 4c), and were going to draw 7 cards total.
Could you use the information in 4card_mc.csv to compute the
probabilities of each hand outcome for that three card hand (even
though 4card_mc.csv has 4 card hands)?

You could take all the rows in 4card_mc.csv which have the three
cards you are interested in (e.g., all rows with As Ks Kh).  From the
way we constructed 4card_mc.csv, these rows cover all possible cases
for the 4th card.   Accordingly, if you sum down the columns (which
represent hand type outcomes), you would get how many times each outcome
happened over all the draws in 4card_mc.csv---pretty much the same
results as if you ran your probability simulation 49,000 (49 * 10,000)
times on the input As Ks Kh.

Does this sound like a task for Pandas?  It sure does!
Fortunately, you already know how to use Pandas to do almost everything you
need for this problem.

Start by opening up estimate.py.  You will see that we have written find_matches
for you, which we will discuss in just a moment.  We have declared two functions:
estimate_one_file and estimate_many_files for you to write, and have
put comments in them describing what you need to do.

As you hopefully recall from your previous learnings about Pandas,
if you can compute a Series of boolean values, you can use that series
to fileter the rows like

filetered_data = my_data[series_to_filter_by]

In this case, we want to filter based on whether a row's "Cards"
column contains all the cards we are looking for, e.g.,

 contains 'As' AND contains 'Ks' AND contains 'Kh'

find_matches works very similarly to functions you have seen before,
except for two new ideas.  The first is that we start with

matches = pd.Series(True, index = df.index)

This makes a Series of all True values for us to start with.
We pick True because True is the identity-element for AND.
"Identity-Element for AND " means that True AND X is always X.
Starting with a vector of all Trues lets our code be nice
and clean as we don't need to handle the first element specially.

Inside the loop, we AND the existing matches vector with

df['Cards'].str.contains(card)

You should be quite familiar with df['Cards'], which selects
the 'Cards' column from our data frame.  The .str.contains(card)
does exactly what it sounds like:  it treats this data
a string and sees if it contains card (which is also a string
in this case 'As', 'Ks', and 'Kh' on the different iterations
of the loop).

Overall, find_matches will return exactly the Series of booleans
you need to filter your data in estimate_one_file.

Your first tasks it to write estimate_one_file.  This function takes
the filename to read from (like '4card_mc.csv') and a list of card descriptions
(like ['As', 'Ks', 'Kh']---note these are strings, not Card objects).  It
should compute and return a Pandas data frame of the probabilities of each
hand type, estimated from the data it read in.
For example, if we evaluate
estimate_one_file('4card_mc.csv', ['As', 'Ks', 'Kh'])

then we get this result:
high card           0.000000
pair               36.602857
two pair           40.896735
three of a kind    12.468776
straight            1.322449
flush               3.354694
full house          4.811633
four of a kind      0.523469
straight flush      0.019388
dtype: float64

Note that these are probabilties, expressed as percents (there is a 36.6%
chance of ending up with a pair if you start with As Kh Ks).

You should be familiar (from Course 3) with most of the Pandas concepts required
to do this task.  One slightly new thing is that once you have filtered your
data and want to sum down the columns, you will need to pass numeric_only=True
to the sum method.  This specifies it should not try to "add in" the column
headers (like "pair" and "two pair").  So you will end up with something like:

    totals = filtered_data.sum(axis = 0, numeric_only = True)


When you have finished this function, try it out by evaluating
estimate_one_file('4card_mc.csv', ['As', 'Ks', 'Kh'])

and seeing if you get the results above.


With that done, it would be nice to compare the probability estimates
that come out of a few different ways to get the same result.

We already explained the contents of 4card_mc.csv, but there are also
three other data files we have provided:

3card_mc.csv:   This is the results of doing probability simulations
                on three card input hands (such as just simulating
                As Ks Kh directly with the code from the previous
                assignment).
true_probs.csv: This is the result of drawing all 49 *48 *47 *46  =
                5,085,024 possible permutations for the remaining
                4 cards to draw. We draw each permutation exactly
                once, evaluate it, and record its outcome.
                With this approach, we get exactly the true
                probabilties.
subset.csv:     This is the result of doing 4 card simulations
                (like As Ks Kh + one more card) for only a
                subset of the possible other cards, not all
                of them.  We provide it just to show you can
                get very good accuracy from estimating
                based on a random subset of the 4th card
                choices.

Note that you do not need to write any more code to proceess
any one of these files estimate_one_file can handle any
of them, as they are in the same format.  Instead,
you are going to write estimate_many_files, which
loops over a list of file names, such as
 ["4card_mc.csv", "3card_mc.csv", "true_probs.csv", "subset.csv"]
and for each of the files, uses the estimate_one_file you just wrote
to compute a Pandas data frame of probabilties based on the data in that
specific file.  You should put these Pandas data frames into a list
(in the same order as they appear in fname_list).  Once you have this
list of data frames, you can use pd.concat to merge them together
into one merged data frame.   You should already be familiar with
pd.concat from the previous course.  However, one new
feature you should use is that you can make the data frame have
the filenames as its column headers by passing keys=fname_list, like this:

    merged = pd.concat(estimates, axis=1, keys=fname_list)

At this point you can run your code and diff it against the
provided output.txt (either Alt-Shift-Z or go to the
Command Palette and find "Run Current File and Diff Output")

If you take a look at the output you produced (or
the contents of output.txt) you will see that all of
our probabilities are quite accurate, when compared
with the true probabilities from true_probs.csv.
That's great!
