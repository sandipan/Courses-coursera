For the next set of assignments, you will be working on building a program that
estimates the chances of each hand winning in poker in a situation described by
an input file. 

In this portion of the project, you are going write the Card class, as well as
any additional variables or helper functions you might need. Specifically, a
Card will represent information about a card's value and suit, as well as
convert that information to a human-readable format with a pair of letters that
describe a card. For example, the 2 of hearts would have the textual
representation '2h', where the first character is one of (2, 3, 4, 5, 6, 7, 8,
9, 0, J, Q, K, A) for the value, and the second character is one of (s, h, d,
c) for the suit. 

We note that we are going to have the Card class use an internal representation
of values (numbers from 2 to 14) that is easy to work with and an external
representation (letters like A, K, etc) that are easy for humans to read and
write. Any time the value is "inside" Card it should be represented by an
integer in the range 2-14. Values coming in from "outside" need to get
converted. For example, the constructor will take 'A' for Ace, and need to
convert it to 14. Any time a value goes back "outside" of Card, it should get
converted back to human readable letters (14 goes back to 'A'). Note how much
easier these internal representations are for things like "less than" to order
cards. Here is a quick table to help clarify:

 External Value Representation   |   Internal Value Representation
 --------------------------------+----------------------------------
             'A'                 |            14
             'K'                 |            13
             'Q'                 |            12
             'J'                 |            11 
             '0'                 |            10
             '9'                 |             9
             '8'                 |             8
             '7'                 |             7
             '6'                 |             6
             '5'                 |             5
             '4'                 |             4
             '3'                 |             3
             '2'                 |             2

Note the external values are strings, and the internal values are integers.

Also note that the external value for the "10" of a suit is '0' (so that it is
a single character like the others), but the internal value is 10, not 0.
That way 10 will be properly ordered between 9 and jack.

In card.py, write:

Some helper functions outside the Class:

  - value_from_letter: convert from external representation of value (string)
    to internal representation of value (int).  This should raise a ValueError
    if the passed in string is not a valid external representation.

  - check_suit: check that the passed in suit is valid.  This method should
     raise ValueError if the passed in suit is not one of 'c', 'd', 'h', 's'

  - letter_from_value: convert from the internal representation of value (int)
    to the external representation of value (string). We do not specify the error
    behavior of this method for values outside the range 2-14.  That should never
    come up, as Card should ensure that its internal values are only in the valid range.

We do not care what error message you use with the ValueError, but if you make it
descriptive of the problem, it may help you later on. 

We have provided you with test-card.py which has *some* testing code
in it, but also a lot of places that you should write more.  We have
provided some testing code at the start for value_from_letter,
check_suit, and letter_from_value.  We *strongly* recommend that you
test the above helpers before you proceed to the Card class.  If you are confident
these work correctly, they will make several of the methods in Card much easier.



Card class
  - A docstring describing the class.

  - The __init__ method to construct a card from given value and suit letters.
    This constructor is responsible for a few tasks:
       1.  Checking that both value_letter and suit_letter are each length 1.
           If they are not, the constructor should raise ValueError.
       2.  Converting the value_letter from the external representation (string)
           to the internal representation (int), and storing the int in a field
           named "value".  Note that you must name the field exactly "value"
           (e.g., self.value = something).  The grader needs to be able to
           examine this field directly.
           You should be able to use value_from_letter to do the hard work
           of this conversion.  If value_letter is not a valid external representation,
           the constructor should give a ValueError to the caller.  As value_from_letter
           already raises this exception, the constructor does not need to do anything
           special:  it should just let value_from_letter handle the error checking,
           and let the exception propogate out to the caller
       3.  Use check_suit to determine if the passed in suit is valid.
           Note that check_suit will raise ValueError if the suit is invalid,
           as with invalid values, the constructor should just let that exception
           propogate to the caller.
       4.  If the suit is valid, the constructor should store it in a field named
           suit (i.e., self.suit = suit_letter).  As with the value field,
           please be sure to name this field exactly "suit" so our graders
           can examine it directly.
   
  - __str__ method to make a string representation of the card with two
    characters, for example, 'As'.  Note that letter_from_value should
    be quite useful in converting self.value back to an external representation.
    
  - __repr__ method that prints 'Card( )' around the string representation, for
    example, 'Card(As)'.  Note that you can avoid duplicating code by using
    str(self) to convert this Card to its string representation using the
    __str__ method you wrote above.   (We dont call self.__str__(), instead
    we do str(self) using the built-in str function, which calls __str__
    appropriately).
    
  - __eq__ (equal to) method, which takes a parameter other.  other should
    be a Card.  This method should return  True if
    self and other have the same value and same suit and False otherwise.
    Note that we generally do not call __eq__ directly, instead when
    we do a == b, the == operator will use the __eq__ function defined for
    the appropriate type to determine how to perform the equality comparison.


  - __lt__ (less than) method, which takes a parameter other and returns True
    if self is less than other and False otherwise. If the cards have the same
    value, determine which suit is "less than": c < d < h < s.
    Note that the internal representation of the value makes the ordering natural:
    you can just directly compare self.value < other.value.   Also notice
    that the ordering of the suits is alphabetical, so you can just compare
    self.suit < other.suit and get the proper ordering (i.e. 'c' < 'd' < 'h' < 's'
    using the built-in string comparison).
    As with __eq__ and ==, we generally do not call __lt__ directly,
    instead a < b will use the appropriate __lt__ to evaluate the < operation.


Other 'public' function (function should be defined in card.py, but it is not a
method of Card): 
  - card_from_num function to take a number 0-51 (inclusive) and return a Card
    in the standard deck. You can do the math however you like, but calling
    card_from_num on 0-51 (inclusive) should build a full deck. If the argument
    is not in the range 0-51, you should raise a ValueError and print an error
    message.    There is an optional hint at the end of this README to help
    you if you are having trouble with this function.  




+==============================+
|Optional Hint on card_from_num|
+==============================+

This is an optional hint for card_from_num.  We hope you will think about it and
try it for a bit before consulting this hint.

We need to take a number 0 <= number <= 51 and turn it into a
suit (of which there are 4) and a value (of which there are 13).
We need to do this conversion in such a way that every card is produced
exactly once from the numbers in this range.  Accordingly, we want
to work out a formula that lets us do this easily.   We can come up
with a couple of different mappings, but if we do something like this:


 0   2c   13  2d   26  2h   39  2s   
 1   3c   14  3d   27  3h   40  3s   
 2   4c   15  4d   28  4h   41  4s   
 3   5c   16  5d   29  5h   42  5s   
 4   6c   17  6d   30  6h   43  6s   
 5   7c   18  7d   31  7h   44  7s   
 6   8c   19  8d   32  8h   45  8s   
 7   9c   20  9d   33  9h   46  9s   
 8   0c   21  0d   34  0h   47  0s   
 9   Jc   22  Jd   35  Jh   48  Js   
 10  Qc   23  Qd   36  Qh   49  Qs   
 11  Kc   24  Kd   37  Kh   50  Ks   
 12  Ac   25  Ad   38  Ah   51  As   

Once you have written down a concrete pattern, it is much easier to think through
how to work out a formula.  As always, break this analysis down into individual
questions and ask them one at a time.

What is the pattern of suits?
 0-12 is clubs
13-25 is diamonds
26-38 is hearts
39-51 is spades

Can you think about a way to use integer division (suit_num = num // something)
such that suit_num will be 0 for clubs, 1 for diamonds, 2 for hearts, and 3 for spades?
If so, then you can convert it into a letter by indexing the literal string "cdhs", like this:

suit_letter = "cdhs"[suit_num]

Now we need to handle the value.   Lets just take a look at all the cards that have
a value of 2 (regardless of suit):

 0   2c   13  2d   26  2h   39  2s   

What do you notice about the numbers 0, 13, 26, and 39?

Now let's look at the cards that have a value of 3 (regardless of suit):

 1   3c   14  3d   27  3h   40  3s

What do you notice about the numbers 1, 14, 27, and 40?

Now look through the rest of the values and see if you can find
a more general pattern.

With that pattern in mind, remember that the modulus operator (%)
gives the remainder when doing division.  E.g.,   7 % 5 is 2 because
when you divide 7 by 5 you get 1 with a remainder of 2.

Can you use modulus to get the following:

Modulus Formula Result         Desired value of card
         0                              '2'
         1                              '3'
         2                              '4'
         3                              '5'
         4                              '6'
         5                              '7'
         6                              '8'
         7                              '9'
         8                              '0'
         9                              'J'         
        10                              'Q'
        11                              'K'
        12                              'A'

If you and do this, you (hopefully) already wrote
a helper function letter_from_value which behaves like this:

Input to letter_from_value         Return of letter_from_value
         2                              '2'
         3                              '3'
         4                              '4'
         5                              '5'
         6                              '6'
         7                              '7'
         8                              '8'
         9                              '9'
        10                              '0'
        11                              'J'         
        12                              'Q'
        13                              'K'
        14                              'A'

If we put that all into one table, it can help you see
how you could do one mathematical operation to the modulus formula
result you came up with above to get the right value to pass to
letter_from_value.   You can then use letter_from_value to get
the proper letter to pass to the Card constructor:

Modulus Formula Result  Input to letter_from_value  Desired value of card
         0                       2                           '2'
         1                       3                           '3'
         2                       4                           '4'
         3                       5                           '5'
         4                       6                           '6'
         5                       7                           '7'
         6                       8                           '8'
         7                       9                           '9'
         8                      10                           '0'
         9                      11                           'J'         
        10                      12                           'Q'
        11                      13                           'K'
        12                      14                           'A'
