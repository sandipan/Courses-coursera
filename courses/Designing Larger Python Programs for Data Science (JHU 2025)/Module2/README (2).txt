The next step in the poker project is to create a class for a Deck, which
contains a list of Cards. This class can be used to represent either a deck of
cards or a hand. 

Before you start, you need to run the included "setup.sh" script which will
link your card.py into this lab assignment.  If you look in the left side of
VSCode (where the files are listed) and find "setup.sh"
(it should have a green $_ icon before its name).  Then you can right click
setup.sh and in the menu that pops up, "Run Code" should be the first item.
Click Run Code.  You should see card.py appear in the list of files on
the left.

Now, open deck.py, and write the following inside the Deck class:

  - a docstring describing the class
  - __init__ method, which initializes the cards (self.cards) field to either
       o An empty list, if the parameters cards is None
       o A *copy* of the passed in list of cards otherwise
         Recall that you can copy a list with [:], like
         self.cards = cards[:]
       Note: you should name the field exactly cards, otherwise our
       provided __eq__ method will not work.  You may also run into
       other grading problems if you change this field name
  - __str__ method, which should make a string containing each two-character
    string representing a card, each separated by a space, for example,
    'As 0c 8h'.   Note that if c is a Card, you can call str(c) to use
    the __str__ method you wrote in Card to convert c to a string (in exactly
    the format you need here)
  - __repr__ method, which has a 'Deck( )' around the string representation,
    for example, 'Deck(As 0c 8h)'.  As with Card's __repr__ method, you should
    use str(self) to avoid duplicating code.
  - add_card method, which takes a card as a parameter and adds that card to
    the cards list.  
  - contains method, which takes a card as a parameter and returns True if the
    deck contains that card and False otherwise. Recall that you wrote the
    __eq__ method for Card, so the == operator will use that.  
  - shuffle method, which should put the cards into a random order. There are
    many ways to do this, so choose one that appeals to you! (Check out the
    Python module random.) 
  - assert_full method, which uses the 'assert [expr]' statement to make sure
    the deck contains exactly one of every card. (You may want to make use of contains
    and card_from_num.)  
  - draw method, which takes the first card in the Deck and both puts it at the
    end of the deck and returns that card. (Consider the list methods pop and
    append.)  
  - sort method, which sorts the cards list by value and suit, from greatest to
    least. (See list's method sort or the built-in sorted function, both of
    which use the elements' < operator (which you defined in Card as __lt__)
    and have a reverse option.) 

Other 'public' function (meaning this function is contained in deck.py, but it
is not a method of Deck) 
  - build_remaining_deck function, which takes a list of Decks named "hands"
  and builds a deck that has all 52 cards except for those found in hands and
  returns the answer Deck. Note that each Deck in hands may contain duplicate
  cards.

  This method will be used later after you read hand descriptions from
  an input file.  The idea here is that if hand 1 has As, Kc, 9d, 7c, 5h
  and hand 2 has 8s, 2c, 9d, 7c, 5h [note that the two hands share the
  last three cards], then the cards left in the deck---what can be drawn
  from for the next card in the game is

  Ac Ad Ah Kd Kh Ks Qc Qd Qh Qs Jc Jd Jh Js 0c 0d 0h 0s 9c 9h 9s 8c 8d 8h
  7d 7h 7s 6c 6d 6h 6s 5c 5d 5s 4c 4d 4h 4s 3c 4d 4c 4s 2d 2h 2s

  That is, all the cards except for As, Kc, 9d, 8s, 7c, 5h, 2c which were
  already used up by being in those two hands.

As you go, test your Deck class in test-deck.py. Note that we have provided import
statements that import your Deck from your deck module and Card and
card_from_num from your card module. Remember that the sooner you test
each method, the less debugging you have to do!  If you find that a method
has a problem before you write any other methods that use it, you can find
the problem much more quickly and easily because you have a good idea
where the problem is.
