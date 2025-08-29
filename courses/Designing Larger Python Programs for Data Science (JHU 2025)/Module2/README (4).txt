The next part of the project that you will do is write some of the code to
evaluate a hand. Remember that you have already written test cases for this
code. That means you have already thought about various corner cases that might
come up and will have a nice suite of tests ready to go when you finish your
code. 

Your ultimate goal in this step is to write a function that, when passed a hand
of cards, determines its poker ranking. 

There are two major steps: 1) figuring out what ranking each hand has
(straight, flush, etc.), and 2) figuring out which five cards make up the hand
(picking out the five cards that made the flush or the two pairs and
tiebreaker).

At this point, you might be thinking that there is going to be a lot of code to
write with all the different possible arrangements of cards and different
possible hand rankings. However, there are a few important things that will
make this managable: 
  (1) We will start by sorting the cards into descending order by value. This
      makes it much easier to find straights (cards in order), and you will
      have "N of a kinds" grouped together.  
  (2) The code to find "N of a kind" is basically the same for 4, 3, and 2 (so
      we can abstract it out into a function).  
  (3) Full house and two pair are just three of a kind and a pair (so we
      already have that code) with another pair (so we can just write a
      function to find a "secondary pair"). That is, in the hand
      Kh Kd Kc 0h 0d
      we will call the 10s (0h and 0d) the "Secondary pair"---its a pair,
      but secondary in importance to the three kings.  Likewise, is
      9s 9h 8d 4h 4c
      we will call the 4s (4h and 4c) the "Secondary pair".   
  (4) By limiting hands to 5 to 7 cards, we can assume:
      - If there is a flush, it will occur in at most one suit. (i.e., you
      won't have As Ah Kh Qs 8s 7h 4s 3s 3h 2h, which has two different
      flushes). 
      - If there is an ace-high straight, there is not also an ace-low
      straight. 


Before you start, you need to run the included "setup.sh" script which will
link your previous poker files into this lab assignment.  If you look in the
left side of VSCode (where the files are listed) and find "setup.sh"
(it should have a green $_ icon before its name).  Then you can right click
setup.sh and in the menu that pops up, "Run Code" should be the first item.
Click Run Code.  You should see card.py, deck.py, and poker_input.py appear
in the list of files on the left.


In eval.py, write:

  - find_flush function, which takes a hand (of type Deck) as a parameter and
    returns the suit of the flush if a flush is found and None otherwise. You
    may find it useful to use a dictionary to map each suit to the number of
    times that suit occurs in a hand.
    
  * At this point, you should run the provided test cases by executing
    your evaluate.py file.   The first several cases test for flushes,
    and should work.  You should expect to fail the test case for 'four of a kind'
    as you have not written that code yet.  When you pass the flush tests,
    move on and work on the next several functions.

  - count_values helper function, which takes a hand as a parameter and returns
    a dictionary which maps each card value to the number of cards in the hand
    with that value. For example, if a hand contains 3 kings, 1 queen, and 1
    five, you would return {13 : 3, 12 : 1, 5: 1}. Whether or not you want the
    dictionary to contain 0 entires for cards that are not in the hand is up to
    you. E.g. {14:0, 13:3, 12:1, 11:0, 10:0, 9:0, 8:0, 7:0, 6:0, 5:1, 4:0,
    3:0, 2:0} is also fine.
  - get_max_count function, which takes a hand and dictionary returned by
    count_values as parameters and returns that pair in the dictionary with the
    maximum count. If multiple card values tie for highest count, return the
    highest value card. 
  - get_kind_index function, which takes a hand and card value as parameters
    and returns the index in the hand of the card with that value. You may want
    to consider the zip function to iterate over a range and cards. If the card
    value does not exist, it should return -1.
  - build_of_a_kind function, which takes a hand, count of n, and an index as
    parameters. It builds the five-card Deck that makes up an n of-a-kind
    ranking by first adding the n cards starting at ind. Then it should fill
    the remaining cards (until there are five) with the highest remaining cards
    in the hand and return the five-card answer. It does not need to worry
    about secondary pairs--these will be added by the next function, add_pair.

  * At this point, you should be ready to run the next set of test cases
    in evaluate.py.  These will test for four of a kind, three of a kind,
    pair, and high card.   These should all work properly (and the ones
    for flush should continue to work properly).  You should expect to
    fail the test case for 'full house' as you have not yet written the
    code to handle that. 

  - find_secondary_pair function, which takes a hand, dictionary returned by
    count_values, and card value as parameters and looks for a secondary
    pair. If a pair exists that is not the passed-in card value, the function
    should return the index where the second pair occurs in the hand;
    otherwise, it should return -1. 
  - add_pair function, which takes a hand, secondary pair index, five-card
    answer Deck, and an answer index as parameters. It should add the secondary
    pair to the answer. If the answer index is 3 (as in a full house), it
    should add the secondary pair to be the last two cards. If the answer index
    is two (as in two pair), it should add the secondary pair to be the third
    and fourth cards, then select the next highest card to be the fifth. It
    returns the updated answer Deck.

  * When you have written these two functions, you should run the test
    cases in evaluate.py.  You should now pass the ones for full house and
    two pair (as well as all the previous ones).

  - is_n_length_straight_at function, which takes a hand, an index, and the (potential)
    flush suit and a number n (for how many cards are required in the straight).
    This function should return True if there is an appropriate straight starting
    at the specified index, and False otherwise. We say "appropriate" because
    we may or may not the straight to be in a specific suit (for a straight flush).
    If the fs (flush suit) is not None, only a straight flush in that suit should be
    considered. We recommend abstracting out two helper functions: 

    Note that for a "normal" straight, n will be 5 (as you need 5 cards).
    We specify this as a parameter, because you will want to call this function
    with n=4 when looking for the 5 4 3 2 that could make up an ace-low straight.

    Hint: You may have multiple cards with the same value but still have a
    straight:  
      As Ac Ks Kc Qh Jh 0d
    has a straight, even though A K Q do not appear next to each other in our
    sorted order. 

    Hint: you can check if a card c is an appropriate suit with
      (fs is None or c.suit == fs)
    If fs is None (meaning we don't care about the card's suit),
    this evaluates to True because (fs is None) evaluates to True.
    If fs is not None---and we do care about the card's suit---this
    evaluates to True whenever c.suit is equal to fs.

    * At this point you should be able to pass the test cases for
      "normal" (not ace-low) straights.   We have broken these down
      into straights first and straight flushes second.  That way, if
      you want, you can write the logic just for straights without
      considering the flush suit, and test it first.  Then you can
      add the code for the flush suit.  You should expect to fail
      the test cases for ace-low straights, as you have not written
      that code yet.


    - is_ace_low_straight_at function which takes the hand, the index to start
    looking at and the (potential) flush suit (as above: None= any ace low
    straight, a suit means that you are looking for a straight flush in that suit)

    Note that there is an ace low straight at a particular index if:
       - There is an Ace of an appropriate suit at that index
         (see the hint above about checking if the suit is ok)
       - There is a 5 of an appropriate suit at some other index (
         lets call it i2)
       - is_n_length_straight(hand, i2, fs, 4) returns True
         That is, we can find 4 cards in a row of an appropriate suit,
         starting at i2---the index where we found a 5 of an appropriate
         suit.

     * After this you should pass all the provided test cases.

Provided:

  - find_straight function (and its helper function copy_straight), which takes
    a hand and flush suit and returns an answer Deck if a straight exists (or a
    straight flush if flush suit is not None) by calling the your
    is_n_length_straight_at and is_ace_low_straight_at functions.
  - build_flush function, which takes a hand and flush suit and returns the
    answer Deck of the flush
  - evaluate_hand function, which calls the functions you wrote to decide,
    according to the rules of poker, which five cards make up the best hand and
    what its ranking is. It returns a tuple of the answer Deck and a string for
    the ranking
  - __main__ code which runs several test cases
