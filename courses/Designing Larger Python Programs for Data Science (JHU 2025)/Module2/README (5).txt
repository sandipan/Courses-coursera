Now that you can evaluate poker hands, you are going to
compute the probability of each hand ranking (high
card, pair, two pair, etc) coming from a given hand.

In particular, you will take an input that represents
part of a hand (like "Ac 8h 3c 2h") and a total number of
cards that will be drawn (e.g., 7), and compute the probabilities
of each outcome based on randomly drawing the remaining
cards (in this example, 3 more).

Before you start, run the "setup.sh" script to link
in the files you did on previous assignments (just as
you have done in other recent labs).

Now, open up probability.py, and notice that we have provided
a list of the hand rankings (hand_types) at the top of the file.

We have also provided make_zero_counts, which makes a dictionary
that maps each hand ranking to 0.

The last thing we provided is print_header_row, which prints
out a comma-separated row with column headers.  The first
column is "Card" (which is the specified cards, and
then each other column has a header which is the name
of the hand ranking in that column (e.g., "pair").

You should write the function probabilities_from_file,
which takes three parameters:
   1. fname is the name of the file to read.
      For example, "input.txt"
      Note that you previously wrote read_input,
      which exactly handles this file format.
   2. n_times is the number of random draws to perform.
      We will explain below what needs to be done for
      each random draw.
   3. total_cards is how many cards should be in
      the hand before evaluating the hand.  In our
      the example we started with, we discussed
      having 7 cards total, and gave an example
      of starting with 4 cards (so we would draw three
      random cards)

Your probabilities_from_file function should do the following:
  1. Read the input file to get a list of Decks
     Recall that read_input will read one hand per line in
     the file, and return a list of Decks
  2. print the header row, using the print_header_row
     function we provided
  3. For each hand read from the input, compute
     the probabilities of each outcome and print them out.
     This is comprised of the following steps:
        3a. Determine the remaining deck of cards to draw
            from (i.e., all of the cards that are not in
            *this* input hand).  Recall that you
            previously wrote build_remaining_deck
            in deck.py. Note you should only pass
            in a one element list with the current hand,
            not all hands, as we are considering each hand
            separately here.
        3b. Create a dictionary which makes each hand ranking
            to 0 using the provided make_zero_counts function.
            You will use this dictionary to count how many
            times you end up with each ranking for this hand.
        3c. Do n_times random draws, counting the results
            each time.  For each random draw you should
              3c1. Shuffle the remaining deck
              3c2. Make a Deck which is a copy of the current
                   hand.  Recall that if you pass Deck's
                   constructor a list of cards, it is supposed
                   to copy them.  So if your hand is in the variable
                   h, you can do
                     h2 = Deck(h.cards)
                   We'll call this copy your "work Deck"
              3c3. Draw from the remaining deck (recall: the draw
                   method in Deck) into your work Deck until
                   your work Deck has total_cards cards in it
              3c4. Evaluate work Deck with your evaluate_hand
                   function
              3c5. Update your dictionary of counts based
                   on the ranking that you got from evaluating
                   this work Deck (i.e., count that you have
                   seen one more of that ranking).
        3d.  Print a row with the results from this hand.
             The row should start with the cards in the hand.
             Then, there should be one column for each ranking
             with the count of how many times your work
             Decks evaluated to that ranking.
             Hint: This will be somewhat similar to print_header_row,
             except you are printing Decks and counts instead
             of column names.

We have provided a __main__ which run this on input.txt with 10,000
draws per hand.  Unfortunately, because this involves randomness,
we can't give you an exact answer to match---we expect some variation.
When we run our own code twice in a row, we get slightly different
answers:

Running it one time:
--------------------
Cards,high card,pair,two pair,three of a kind,straight,flush,full house,four of a kind,straight flush
As Ks Qs Js,908,2040,986,177,1130,4061,52,3,643
8s 8c 7c 6s,0,3515,3858,885,1129,169,411,27,6
Kc 0c 7c 4c,1205,2594,1040,207,96,4813,39,4,2
As Jh 0d 8c,2490,4498,1517,294,1159,0,41,1,0
As Ah Ks Kh,0,0,7358,1132,38,184,1237,48,3

Running it another time:
------------------------
Cards,high card,pair,two pair,three of a kind,straight,flush,full house,four of a kind,straight flush
As Ks Qs Js,836,2066,1016,190,1141,4078,39,3,631
8s 8c 7c 6s,0,3450,3919,925,1044,182,449,28,3
Kc 0c 7c 4c,1225,2644,1047,205,100,4735,37,1,6
As Jh 0d 8c,2414,4660,1549,261,1080,0,35,1,0
As Ah Ks Kh,0,0,7392,1171,37,168,1181,50,1


While we could take some steps to control the randomness[*],
this still would not be enough to ensure you get the exact
same answer: any difference in how you do things might
cause the answer to be slightly different.

Instead, we have run our code many times, computing the minimum
and maximum values we observed for each column.  We will
consider things correct if they are "close enough" to the results
we got.  In particular, we ran our simulation 200 times,
and will consider each value if close enough if it is above
0.95 * the minimum value we got and below 1.05 * the maximum
value we got (so +/-5% of the smallest/largest values we saw).

You can run the enclosed "check.sh" script (find it on the left
side of VSCode, right click it, and choose "Run Code") which will run your
code, and then check each entry to see if it is within these ranges.
If anything is out of our exepcted ranges, this script will let you know.
If everything is ok, the script will print a message telling you
everything was fine.

[*] The random number generation is actually "psuedo-random"
    which means that its a mathematical function that looks
    random to people.  You can "seed" the random number
    generator, giving it a starting number to work from,
    which causes it to produce the same sequence of "random"
    numbers.
