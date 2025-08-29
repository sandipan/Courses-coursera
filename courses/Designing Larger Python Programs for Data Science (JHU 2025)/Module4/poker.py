import sys
from poker_input import read_input
from deck import build_remaining_deck, draw_all_unknowns
from evaluate import evaluate_hand

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
hand_rankings = {hand_types[i]: i for i in range(0, len(hand_types))}


# compare two hands, including tie breakers
# if hand1 wins against hand2, returns 1
# if hand1 ties with hand 2, returns 0
# if hand1 loses to hand 2, returns -1
def compare_hands(hand1, hand2):
    five1, ev1 = evaluate_hand(hand1)
    five2, ev2 = evaluate_hand(hand2)
    assert ev1 in hand_rankings, f"Invalid hand evaluation: {ev1}"
    assert ev2 in hand_rankings, f"Invalid hand evaluation: {ev2}"
    rank1 = hand_rankings[ev1]
    rank2 = hand_rankings[ev2]
    if rank1 > rank2:
        return 1
    if rank1 < rank2:
        return -1
    # break ties.  Python list < does exactly what
    # we need
    assert len(five1.cards) == len(five2.cards)
    for i in range(0, len(five1.cards)):
        if five1.cards[i].value > five2.cards[i].value:
            return 1
        if five1.cards[i].value < five2.cards[i].value:
            return -1
        pass
    return 0


# provided
def print_results(wins, n):
    for i in range(0, len(wins) - 1):
        print("Hand {} won {} / {} times".format(i, wins[i], n))
        pass
    print("and there were {} ties".format(wins[len(wins) - 1]))
    pass


def simulate(input_fname, num_draws):
    # read from file
    decks = read_input(input_fname)
    # create initial results a list of
    # all zeros, of length (number of hands + 1)
    results = [0] * (len(decks) + 1)
    # build the remaining deck (use build_remaining_deck)
    remaining_deck = build_remaining_deck(decks)

    # do monte carlos
    for draw_count in range(num_draws):
        # shuffle the remaining deck
        # (use shuffle in Deck class)
        remaining_deck.shuffle()
        # draw all unknown cards (use
        # draw_all_unknowns from deck.py)
        draw_all_unknowns(decks, remaining_deck)
        # compare all the hands to determine
        # who wins or tie for best
        # use the compare_hands function above
        # to compare one hand to one other hand
        w_ind = 0
        winner = hand = decks[w_ind]
        is_tie = False
        i = 1
        for other in decks[1:]:
            res = compare_hands(winner, other)
            is_tie = True if res == 0 else False
            if res == -1:
                winner, w_ind = other, i
            i += 1
        # increment the count of the winner
        # (or tie)
        if is_tie:
            results[-1] += 1
        else:
            results[w_ind] += 1
        pass
    # print results (use the print_results
    # function above)
    print_results(results, num_draws)
    pass


if __name__ == "__main__":
    for i in range(0, 10):
        fname = f"input{i}.txt"
        print(f"Results from {fname}:")
        print("-" * 20)
        simulate(fname, 10000)
        print("-" * 20)
        pass
    pass
