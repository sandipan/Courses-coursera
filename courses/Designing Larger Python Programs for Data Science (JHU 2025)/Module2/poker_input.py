# import statements here
from deck import Deck
from card import Card, card_from_num


def hand_from_string(s):
    cards = []
    # write code here to fill in cards
    lets = s.split()
    for let in lets:
        if len(let) != 2:
            raise ValueError("Each card should contain 2 letters")
        cards.append(Card(let[0], let[1]))
    return Deck(cards)


def read_input(fname):
    # pass
    hands = open(fname).read().splitlines()
    decks = []
    for hand in hands:
        decks.append(hand_from_string(hand))
    return decks
