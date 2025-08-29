Now, you are going to write the code that reads hands of cards from a
file. We'll use the Deck class you worked with in a previous part to represent
a hand of cards (a hand of cards is just a much smaller deck of cards--they are
both just sets of cards). Each line of the file will give the cards in a hand.

For example, if you had input like 

Kh Qh As 4c 2c
Ac Qc As 4c 2c
Qh 0s 9h 8d 8s 7d 6c
Qh Jc 0s 9h 9d 5h 4h

The function you will write would parse that into a list of hands

[Deck(Kh Qh As 4c 2c), Deck(Ac Qc As 4c 2c), Deck(Qh 0s 9h 8d 8s 7d 6c),
 Deck(Qh Jc 0s 9h 9d 5h 4h)]

Before you start, you need to run the included "setup.sh" script which will
link your card.py and deck.py into this lab assignment.  If you look in the
left side of VSCode (where the files are listed) and find "setup.sh"
(it should have a green $_ icon before its name).  Then you can right click
setup.sh and in the menu that pops up, "Run Code" should be the first item.
Click Run Code.  You should see card.py and deck.py appear in the list of
files on the left.


Now, in poker_input.py, write the following two functions:

  - hand_from_string which takes a string and returns a Deck.  This
    function is responsible for taking a string that is one hand
    (like 'Kh Qh As 4c 2c') and turning it into a deck of cards.
    Note that:
       1. The card will always be separated by 1 or more spaces.
          The "split" method in string may be useful.
       2. Each card's description should be exactly two letters.
          If it is not 2 letters, the code should raise ValueError
       3. The letters are exactly what Card's constructor requires
          (a value letter and a suit letter).   Card's constructor
          already provides appropriate error checking.  If Card's
          constructor raises a ValueError, hand_from_string should
          just allow it to propogate out to inform the calling function(s)
          of the problem.

  - read_input function, which takes as parameters a string for the file
    name. It reads input from the file (one hand per line) and returns a list
    of hands (Decks) that it read in. 

As always, test your code in test-input.py until you are satisfied
with its functionality.
