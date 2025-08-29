So far, we have dealt with one poker hand in isolation:
trying to determine what the chances of various outcomes are.
Now, we want to shift slightly to a different question:
given some set of hands, what are the chances of each hand winning.

In some versions of poker, we could just finish this up,
by reading a description of multiple hands, e.g.

As Kh 0c
Qs Js 8h
Ac 8s 8c 

and knowing how many more cards we will draw (e.g., draw to 5 cards per
hand, or draw to 7 cards per hand).  The presense of the other
hands influences the probabilities some---for example, the first
hand above (As, Kh, 0c) is less likely to draw a straight as
Qs and Js are already used up, so there are fewer Queens and Jacks
in the deck.   However, we pretty much have all the code to do that:
read_input reads multiple hands and returns them as a list of Decks,
build_remaining_deck takes a list of hands and gives back the
deck of cards left---so we could pass it all those hands at once.
Then we could draw from that deck into each hand (similarly to what
you did before).  You already have hand evaluation logic, and
would just need to compare the rankings/break ties, and count
winners.  You will put all that together in the next step of this project,
but first we want to support one more feature in our input.

In many poker variants (including the popular "Texas Hold'Em"),
there are cards which are shared between hands.   For example,
in Texas Hold'Em, each player has 2 cards of their own,
then 5 more cards that are shared bewteeen all hands.
To support this possibility, we are now going to *explicitly*
represent unknown cards in our input file, with ?0, ?1,
?2 etc.   Anytime ?0 appears it will be the *same* card
as any other ?0.  ?0 will be a *different* card from ?1,
?2 etc (though all ?1s will be the same as all other ?1s, etc)

Accordingly, if we wanted to represent our simple input above,
with 3 knowns cards, and 4 unknown but distinct cards per hand
(draw to 7 total cards like before), we could write:

As Kh 0c ?0 ?1 ?2 ?3
Qs Js 8h ?4 ?5 ?6 ?7
Ac 8s 8c ?8 ?9 ?10 ?11

Note that in the above example, we are not sharing any cards
between hands: all the ?nums are distinct.  However, we can now write
something like this:

As Kh ?0 ?1 ?2 ?3 ?4
Qs Js ?0 ?1 ?2 ?3 ?4
Ac 8s ?0 ?1 ?2 ?3 ?4

The above represents a Texas Hold'Em hand where whoever is evaluating
the probabilities knows all private cards, but the 5 shared cards are unknown.
Such a situation might come up for the TV announcer in a televised game.

We could have a slightly different input to represent this from the
perspective of a player:

As Kh ?0 ?1 ?2 ?3 ?4
?5 ?6 ?0 ?1 ?2 ?3 ?4
?7 ?8 ?0 ?1 ?2 ?3 ?4

Here, we only know one hand's (our own) private cards.  We know
that the other hands have their own private cards: there is only
one ?5, one ?6, one ?7, and one ?8 so those 4 cards are distinct.
But then all hands share ?0, ?1, ?2, ?3, and ?4.


Supporting this is going to require a few changes
(which we will explain in more detail below):
  1. The Card class in card.py will need to support
     an unknown (placeholder) card.
  2. hand_from_string in poker-input.py will need
     to support unknown cards
  3. The Deck class in deck.py will need a method
     to determine how many unknown cards need
     to be drawn for a hand
  4. The Deck class in deck.py will need a
     method to fill in all instances of a particular
     unknown card (e.g., ?0) with a specified
     card drawn from the deck (e.g. 9s)
  5. In deck.py (but outside of the Deck class)
     you will need to add a method which computes
     how many unknown cards to draw for a list
     of hands (list of Decks) and another method
     which takes a list of hands, the remaining deck,
     and draws (from the deck of remaining cards) the
     appropriate number of cards, filling in all unknown
     cards in all the hands.


Change 1: Make Card support a placeholder card.
-----------------------------------------------
First, open up card.py.  You need to make two
changes to this class:

   1.  Go to the constructor (__init__).  Now,
       we will allow value_letter to be '?'.
       When value_letter is '?', we will construct
       the card differently.  suit_letter will
       be interpreted as a string ('0', '1', etc)
       specifying the unknown card number
       Accordingly, we will add a new field
       
         unknown_card_num
       which you should make the constructor set
       to
           int(suit_letter)
       whenever value_letter is '?' and to
       None for a normal card (when value_letter
       is not '?').  When value_letter is
       not '?', after setting unknown_card_num
       to None, your constructor should do all
       the things it previously did (converting
       the value and suit to the internal
       representation etc).
       When the value_letter is '?'
       the constructor should only set
       unknown_card_num as described above
       and set value to 0 and suit to '?'
       Note that 0 and '?' were previously
       not valid values for these fields,
       but are the correct types (int
       and string respectively).
       

   2. In the __str__ function, you should check
      if value is 0.  If value is 0, the
      __str___ function should return
      should return f"?{unknown_card_num}"
      instead of what you currently return.
      If value is not 0, __str__
      should behave as it previously did.
  
      Note that we are checking if value is 0
      rather than if unknown_card_num is not
      None because later we will fill in
      the value and suit, but leave unknown_card_num
      alone.   When we have specified an actual
      value and suit (e.g., 'A' and 's'), we will
      want to use those (e.g. 'As') for the string
      representation.   However, we want to leave
      unknown_card_num as is, so we can fill
      the card in with different values on
      multiple draws.
      

Test these changes before you proceed with the provided
test-card-changes.py

Change 2: Make hand_from_string support placeholders
----------------------------------------------------

Next, open poker_input.py, and go to hand_from_string.
This function needs a few small changes.  As it is,
it will work just fine for '?0' through '?9'.
However, it should currently require that card descriptions
be exactly 2 characters, so it will give an error
for ?10, ?11, etc.  We want those to be legal, so we need
to fix that.    Now, the error checking should be

 - if the first character is not a '?', the description
   must be exactly 2 characters
 - otherwise, it must be at least 2 characters

You will also need to change the code where you split the string
into the value_letter and suit_letter (to pass to the Card constructor),
as this likely assumes exactly two characters.  Remember that you can slice
a string like
    mystr[1:]
to get everything except the first character---that will be exactly
what you want, whether its actually a suit letter ('s', 'c', etc) or
an unknown card number ('0', '1', '2', ... '10', '11', etc).

Test these changes before you proceed with the provided
test-input-changes.py
      

Change 3: Find how many unknown cards we need to draw
-----------------------------------------------------

For your next task, open deck.py.  Inside of the
Deck class, add this method:

   def max_unknown_card_num(self):

This method should iterate over the cards in this
deck (self.cards) and find the largest unknown_card_num,
which it should return.   If there are no unknown
cards, this method should return -1.
Note that when you write this method,
you should be aware that some cards will have
unknown_card_num set to None.  You will need
to check if unknown_card_num is None or
not before trying to compare it to an integer
If it is None, you can't compare it to an integer.
If it is not None, you should.

When you are finished with this change, test
your changes with test-max_unknown_card_num.py

Change 4: Fill in all instances of a specific unknown card
----------------------------------------------------------

Your next task is also in deck.py.   Add this method
inside of the Deck class:

    def fill_unknown_card(self, num, actual_card):

Here, num is the unknown card number (like 0, 1, 2) which specifies
which unknown card is being filled in (so if num is 1, you are filling
in all ?1 cards---which means they have unknown_card_num==1).
The other two parameter specifies the actual card to (as
drawn from the remaining deck) to fill in the placeholder from.

Note that you should NOT do this:
    self.cards[ind] = actual_card
    
which will appear to work if you only fill in the deck once,
but will not work if you fill in the deck many times.

Instead, you need to iterate over the cards in this hand
(self.cards) and for each one that has the appropriate
unknown_card_num, you need to change its value and suit
to the value and suit of actual_card.

When you are finished with this change, test your changes with
the provided test-fill_unknown_card.py

We will briefly note that the approach we have taken favors
simplicity over efficiency.   We are searching through
every card in all the hands for each unknown card we draw.
In this case, we don't care so much about efficiency---there
will be maybe 12 to 15 cards, with 5 to 10 unknown cards.
If we did care about efficiency, we could build a data
structure which tracks which unknown cards are in which hands.
Then we could access the appropriate cards directly,
without searching all the cards.

Change 5: Draw and fill all unknown cards in a list of hands
-------------------------------------------------------------

Your last task in this assignment also takes place
inside of deck.py.  However, this function should
be *outside* the deck class (e.g., after build_remaining_deck,
which is also outside of the Deck cass).

Here, you should write

 def draw_all_unknowns(hands, remaining_deck)

This function takes two parameters.  The first (hands) is a list
of Decks, which is all the hands of cards in the current game.
These hands have unknown cards which need to be filled in.
The second parameter (remaining_deck) is the deck with the remaining
cards (which are not in hands).  When you use this method
in the next part of the project, remaining_deck will come
from calling build_remaining_deck(hands), then shuffling that deck.
However, by taking it as a parameter here, we can easily control
what cards are in the reamining deck to simplify testing.

This method needs to do a few things, but you have already written
the code to do the actual work for each of those things in the
previous steps.

First, you need to find out how many unknown cards you need to draw.
You have written max_unknown_card_num, which will take one Deck (i.e.,
one hand) and figure out the maximum unknown card number in it.   However,
you need to find the maximum unknown card number across all the Decks
in hands.  You should be able to write a small loop over hands using
max_unknown_card_num to compute the maximum unknown card number over
all the hands.

Note that you need to draw one more card than the maximum unknown card
number in all the hands.  So if if the maximum unknown card number is 2,
you need 3 cards: ?0, ?1, and ?2.  If it is -1, you do not need
to draw any cards.

Next, you need to iterate over the number of cards you need to draw.
For each card you need to draw, you should draw a card from
the remaining_deck (recall: you already have a method in Deck to do this).
Then, for each hand (a Deck) in the list of hands, you should use
the fill_unknown_card method you wrote earlier to fill in all the
placeholder cards in that hand with the one that you drew.

When you finish that, test with test-draw_all_unknowns.py



