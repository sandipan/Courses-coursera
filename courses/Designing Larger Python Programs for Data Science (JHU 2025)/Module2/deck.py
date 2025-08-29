from card import Card, card_from_num
import random


class Deck:
    def __init__(self, cards=None):
        # Note: we want a default of cards = []
        # but mutable default arguments are bad.
        # so you should check if cards is None, and if so
        # self.cards be [], otherwise self.cards should be whatever
        # is passed in as cards
        # pass
        self.cards = cards[:] if cards is not None else []

    def __str__(self):
        # pass
        # print((" ".join(self.cards)).strip())
        return (" ".join([card.__str__() for card in self.cards])).strip()

    def __repr__(self):
        # pass
        return f"Deck({self.__str__()})"

    # Equality comparison:
    # check if self's cards are the same as other's cards
    def __eq__(self, other):
        return self.cards == other.cards

    def add_card(self, c):
        # pass
        self.cards.append(c)

    def contains(self, c):
        # pass
        for card in self.cards:
            if c == card:
                return card
        return None

    def shuffle(self):
        # pass
        random.shuffle(self.cards)

    def assert_full(self):
        # pass
        assert (
            all(self.contains(card_from_num(c)) for c in range(52))
            and len(self.cards) == 52
        )

    # takes card from from deck, appends it to end, and returns it
    def draw(self):
        # pass
        c = self.cards.pop(0)
        self.cards.append(c)
        return c

    # sorts high to low
    def sort(self):
        # pass
        self.cards = sorted(self.cards, reverse=True)

    # pass


# builds and returns complete deck except for cards in hands
def build_remaining_deck(hands):
    # pass
    all_cards = [card_from_num(c) for c in range(52)]
    existing = []
    for hand in hands:
        existing += hand.cards
    remaining = [card for card in all_cards if not card in existing]
    return Deck(remaining)


"""
print(build_remaining_deck(
    [
        Deck(
            [
                Card("4", "d"),
                Card("A", "s"),
                Card("9", "h"),
                Card("3", "c"),
                Card("0", "d"),
            ]
        ),
        Deck([Card("4", "c"), Card("A", "c")]),
    ]
))
"""
