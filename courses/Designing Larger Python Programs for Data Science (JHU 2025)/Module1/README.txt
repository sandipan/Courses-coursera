In this assignment, you are going to be starting to write a program
to generate a semi-random story, similar to the game "Mad Libs".
You will finish this program over four total lab assignments,
as the learning objective of these assignments is to see how to
break down a large programming task into smaller pieces.

If you have never played Mad Libs, the way that it works it that
one player has a story with blanks in it.  Each blank contains
a description of the kind of word that goes there (like "verb"
or "place" or "food").  The player with the story asks
the other players to name a word of that kind, and writes
it in the blank.  Once all blanks are filled in, the story
is read aloud.

Our random story will follow the same principle, except
that we will also keep track of everything we selected
in the past, and allow reference to it by number.

If you look at the first two lines of story.txt, you will see

Once upon a time there was a _animal.  The _0 lived in a very scary _place.
One day, the _0 left his _2 and went in search of a _food.  

Each _ indicates a blank, and whatever is after the blank indicates
how to fill it in.
  - If the blank is immediately followed by a number, then it
    means to re-use the (number)th selection, counting from 0.
    For example _0 to re-use the first selected word.
    Note that this type of blank is followed by any number of base-10 digits
    (0-9), and ended with anything that is not a digit.
    Multi-digit numbers, such as _10, _123, etc are possible.
    All blanks are counted in the numbering scheme, so if you
    we look at the blanks in the above story, we would see
    that they are counted as numbered in [] below each blank:
    _animal  _0 _place _0   _2  _food
      [0]    [1] [2]   [3]  [4]  [5]
   Accordingly, the _0 blanks would refer to whatever animal is selected
   and the _2 blank would refer to whatever place is selected.

  - If the blank is immediately followed by a word (made of letters), then it
    means to select a random word of that type.
    Note that this type of blank is followed by any number of letters
    (upper and or lower case (a-z, A-Z)).  Any non-alphabetic character
    ends the blank.  So _animal.  is the blank _animal followed
    by the literal character period. 


So for example, we might select "cat" for the first blank (_animal).
When we reach the second blank (_0) we re-use cat.  We
might select "castle" for the next blank (_place).  The following
two blanks will be "cat" (_0) and "castle" (_2) since those reference
words already chosen.  Note that _1 would have also chosen
"cat".  We might then pick "pizza" for the final blank.  Any character
which is not part of a blank is returned literally.  We would
then return this string as our "story":
    
Once upon a time there was a cat.  The cat lived in a very scary castle.
One day, the cat left his castle and went in search of a pizza.  

At a high-level, you are going to edit the file randomstory.py and write
the function

randomStory(storyFile, wordTypes)

The first parameter is the name of the story file (with the blanks in it).
The second is an iterable (e.g., list or set) which will name all the types
of words that must be selected (other than numbered back references).
In our example above, wordTypes would be ['animal', 'place', food'].
(However, for the full story.txt, the list would be
 ['animal', 'food', 'greeting', 'magiccreature', 'place', 'said', 'thing', 'time']

We are going to split this assignment into four parts.   One of the key learning
goals for this assignment is to see how to break down complex tasks into smaller
subparts.  Approaching problems this way can help you take what may seem
quite difficult, and split into problems which are all manageable.

In particular,

  For *this* assignment, you are going to just read the story template,
  and identify the blanks.  Specifically you are going to return (not print)
  a string that is just like the story template except that for each blank,
  you put the blank's tag (category name or number) inside of [].

  For example, if you have an input of

  The _animal went to the _place.  Then the _0 ate the _food.

  Then your program would return the string

  "The [ animal ] went to the [ place ].  Then the [ 0 ] ate the [ food ]."

Some novices may think "this is a waste of time.  All I did was change
_animal to [ animal ]".  However, what this accomplishes is that you
write the code to find the blanks and identify the category or number
in the blank.   You also can test it and see if it works, which
makes the remaining parts much easier: once you have a piece of code
you can run, it is easier to test things as you add and change parts of it.
Once you have tested this part and are confident in it, you can build on it and be
very certain that any other problems you encounter are not in this part
of the code.

The next assignment will be to modify this code to make a decision
for each blank: is it a word (category name) or a number (back reference)?

You will change your randomStory to put either "word" or "num" with each blank:

  "The [ word animal ] went to the [ word place ].  Then the [ num 0 ] ate the [ word food ]."

At this point, you might think "but that change is so small. Shouldn't I be doing more?"
We want to make small changes and test them.   If you can write just a few lines of code,
then test, you are in good shape: if something goes wrong, you know it is very likely
to just be in those few lines of code!


For the third assignment in this series, you will read in the category files
(the ones that list the possible words for animals, etc), and replace just the word
blanks---leaving the numeric blanks as they are in your previous assignment.  Your
program might then return

  "The cat went to the cave.  Then the [ num 0 ] ate the pizza."

This change will be bigger than the previous one, but still manageable.

In the final assignment in this series, you will handle the numeric back references,
making the [ num 0 ] be the same as the first blank ("cat"), and finishing
the random story program.


HINT for this assignments:  Many learners try to focus on whitespace
(e.g. split the input into words based on spaces, like "The" "cat"
"went" "to").  Splitting the input based on whitespace is problematic
for two reasons.  The first is that we want to keep the original spacing,
and many approaches will discard duplicate spaces (like "_place.  Then"
has two spaces between the period and the next word).  The second problem
is that blanks are not ended by whitespace.  They are ended by
any character that isn't the right type for the blank (non-letters
for word blanks and non-numbers for numeric blanks).

In fact, whitespace is pretty much irrelevant to this problem.
What matters is underscores (_).  Therefore, if you want to use the split()
method, you should think about .split('_').  We'll note there are many
approaches.  Geneveive likes to use .split('_') (which is what will be
presented in the videos).  Drew likes to just write a while loop
to iterate over each character of the input line.


Note that for this assignment, your randomStory function should still take two
parameters (storyFile and  wordTypes) even though you will not use wordTypes yet.

We have already put code if __name__ == "__main__" to call randomStory with
two story templates we provided ("story.txt" and "story2.txt"), and to
print the results (as well as a header to say where each story starts).
We have passed in the category names that you will need in later assignments,
even though your code does not use them now, as you will work from
the same randomstory.py file in later assignments.

We have give you an output.txt which is what your program should print when you
run the provided main code. As reminder, you can run your program and diff
the output against our provided output with Alt-Shift-Z, or by looking
in the Command Palette for "Run Current File and Diff Output".

When you are finished, submit this step for grading.
