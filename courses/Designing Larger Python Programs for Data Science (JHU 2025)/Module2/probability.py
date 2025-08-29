from poker_input import read_input
from deck import build_remaining_deck, Deck
from evaluate import evaluate_hand

# The hand types we have, in the order
# they should appear in your output
hand_types = [
    "high card",
    "pair",
    "two pair",
    "three of a kind",
    "straight",
    "flush",
    "full house",
    "four of a kind",
    "straight flush",
]


# This gives you a dictionary with
# each type of hand, with a count of 0
def make_zero_counts():
    return {ht: 0 for ht in hand_types}


# Print out the header row
# The first column has a header of "Cards"
# and each other row has a header for the corresponding
# hand ranking, in order from lowest to highest
def print_header_row():
    print("Cards", end="")
    for ht in hand_types:
        print(f",{ht}", end="")
        pass
    print()
    pass


def probabilities_from_file(fname, n_times, total_cards):
    # You should write this code
    # pass
    hands = read_input(fname)
    print_header_row()
    for hand in hands:
        remaining_deck = build_remaining_deck([hand])
        count = make_zero_counts()
        for _ in range(n_times):
            # remaining_deck = build_remaining_deck([hand])
            remaining_deck.shuffle()
            work_deck = Deck(hand.cards)
            while len(work_deck.cards) < total_cards:
                c = remaining_deck.draw()
                work_deck.add_card(c)
            _, ranking = evaluate_hand(work_deck)
            count[ranking] += 1
        print(hand, end="")
        for rank in count:
            print(f",{count[rank]}", end="")
            pass
        print()
        pass


if __name__ == "__main__":
    probabilities_from_file("input.txt", 10000, 7)
    pass
