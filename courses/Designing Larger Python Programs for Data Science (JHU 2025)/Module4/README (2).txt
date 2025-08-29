Now you are ready to put the whole program together! Open
the file poker.py, where you will write the code to do
the Monte Carlo simulations (estimating probability by
random drawing of cards) for poker hands with shared
unknown cards.

As we have typically done, you need to run
setup.sh to bring in the files you did in previous labs.

In particular, you should write the simulate
function, which takes two parameters: input_fname
is the name of the input file (in exactly the format
that read_input will read for you).  The second
parameter is num_draws, which is how many
random draws you are doing.

We have left some comments in the simulate function
to guide you, but will expand on the details of what
you need to do here.
  1. First you need to read the input from the file
     named input_fname.  You have already written the code
     to do this in the read_input function.  Recall that
     this function returns a list of Decks.
  2. Create a list to count how many times each hand wins, with
     one more element for if there was a tie (so if there are two
     hands, you should have three elements: [hand 0 wins, hand 1 wins, ties]).
     Initialize all its values to 0. 
  3. Build the remaining deck.  You already wrote a function to
     do this in deck.py (build_remaining_deck), but recall that
     this takes a list of hands and builds a deck with all cards
     that remain after the ones in the given hands have been drawn.
  4. Do each Monte Carlo trial (repeat num_draws times).
     Note that we wrote a for loop for you to repeat this num_draws
     times.  For each draw you need to
      o Shuffle the deck of remaining cards (recall you already wrote
        shuffle in the Deck class)
      o Assign unknown cards from the shuffled deck (you just wrote
        draw_all_unknowns, which does the work for this)
      o Use compare_hands (we wrote it for you at the top of
        this file) to figure out which hand won. We made
        this function so that compare_hands(hand1, hand2)
        will
           return 1 if hand1 wins against hand2,
           return 0 if hand1 ties with hand2
           return -1 if hand1 loses against hand2
         This function considers tie breakers, and only
         declares a tie if both hands are the same
         rank and have the same values for all 5 cards.

        Note that with potentially more than two hands,
        you will need to do a comparison that looks a lot like
        finding the maximum value in a list,  compare_hands instead of >.

        Note that we only consider the hand a tie if there
        is a tie for the best outcome.  If, for example there is
        Hand 0: flush As 9s 8s 5s 4s
        Hand 1: pair  As Ah 9s 8s 5s
        Hand 2: pair  As Ac 9s 8s 5s
        then Hand 0 wins (and it does not count as a tie).
        One way to handle this is to have a variable (like is_tie)
        which you set to True when you find a tie with the best
        hand, and set to False whenever there is something better
        than the current best hand (meaning no longer a tie).

      o Increment the win count for the winning hand (or for the
        "ties" element of the list if there was a tie).
  5. After you do all your trials, you just need to print your results
     (we provide print_results---so call that with your list of results)


As this assignment also relies on randomness, we can't give
you a single right answer to compare against.  However, we
can give you an expected range of answers like we did before.
You can run the enclosed check.sh script (find it in the list
of files on the left of VSCode, right click, and do "Run Code").