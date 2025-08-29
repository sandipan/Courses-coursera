from card import Card, card_from_num, letter_from_value, ACE, KING, QUEEN, JACK
from deck import Deck
from poker_input import hand_from_string


def find_flush(hand):
    """Find flush suit if exists or return None."""
    # pass
    count = {"c": 0, "h": 0, "s": 0, "d": 0}
    for card in hand.cards:
        count[card.suit] += 1
    for suit in count:
        if count[suit] >= 5:
            return suit
    return None


def count_values(hand):
    """Make a dictionary of cards values to count of their occurrences."""
    # pass
    counts = {}
    for card in hand.cards:
        counts[card.value] = counts.get(card.value, 0) + 1
    return counts


def get_max_count(hand, counts):
    """Use counts dict and return a tuple (value with most n of-a-kind, n)."""
    # pass
    n, value = max([(count, value) for (value, count) in counts.items()])
    return (value, n)


def find_secondary_pair(hand, counts, val):
    """Find index of second pair or return None for no sec pair."""
    # pass
    for index, card in enumerate(hand.cards):
        if counts.get(card.value, 0) >= 2 and card.value != val:
            # print("here", hand, counts, card, val, index)
            return index
    return None


def get_kind_index(hand, value):
    """Get first index of value in hand or return None if no such value exists"""
    # pass
    for index, card in enumerate(hand.cards):
        if card.value == value:
            return index
    return -1


def build_of_a_kind(hand, n, ind):
    """Build hand with n of-a-kind starting at ind."""
    # pass
    # ans = [
    #    Card(letter_from_value(hand.cards[ind].value), suit)
    #    for suit in ["s", "h", "d", "c"]
    # ]
    cards = hand.cards[:]
    ans = cards[ind : ind + n]
    del_ind = list(range(ind, ind + n))
    if n <= 3:
        ind2 = find_secondary_pair(hand, count_values(hand), cards[ind].value)
        if ind2 is not None:
            ans += hand.cards[ind2 : ind2 + 2]
            del_ind += list(range(ind2, ind2 + 2))
    n = len(ans)
    if n < 5:
        remaining = cards
        # del remaining[del_ind]
        remaining = [i for j, i in enumerate(remaining) if j not in del_ind]
        remaining = sorted(remaining, reverse=True)
        ans += remaining[: 5 - n]
    return Deck(ans)


def add_pair(hand, pair_index, ans, ans_index):
    """Add secondary pair (for full house or two pair).

    Pair to add is at index pair_index in hand and added to ans index ans_index.
    """
    # Note that ans already has 5 cards (from build_of_a_kind), so you are replacing
    # the existing cards in answer, rather than appending to it
    #
    # Also note that for two pairs (when answer_index=2), you need
    # to ensure the 5th card is correct (the highest valued card in hand,
    # which is not in either of the two pairs)

    pass


def is_n_length_straight_at(hand, ind, fs, n):
    """Helper for is_straight_at: determine if straight of n at ind."""
    # return False
    """
    cards = hand.cards[:]
    if ind + n > len(cards):
        return False
    found = 1
    for i in range(ind, len(cards) - 1):
        diff = cards[i].value - cards[i + 1].value
        if diff not in [0, 1]:
            return False
        else:
            found += diff
            if fs is None or cards[i].suit == fs:
                found += diff
        if found == n:
            return True
    return False
    """
    cards = hand.cards
    if not (0 <= ind < len(cards)):
        return False

    start = cards[ind]

    # If we require a suit (straight flush), the starting card must match it.
    if fs is not None and start.suit != fs:
        return False

    needed = n - 1
    target = start.value - 1  # next rank we need (strictly consecutive downward)

    # scan forward; duplicates are fine, suits only matter if fs is set
    for j in range(ind + 1, len(cards)):
        if needed == 0:
            return True

        c = cards[j]

        if c.value > target:
            # still above the next needed rank; just skip duplicates/higher ranks
            continue

        if c.value == target:
            # rank matches; accept only if suit is appropriate (or we don't care)
            if fs is None or c.suit == fs:
                needed -= 1
                target -= 1
            # if suit doesn't match (straight flush), keep scanning:
            continue

        # c.value < target  -> we've passed the needed rank; impossible to complete
        return False

    return needed == 0


def is_ace_low_straight_at(hand, ind, fs):
    """Helper for is_straight_at: determine if ace-low straight at ind."""
    # return False
    cards = hand.cards
    if not (0 <= ind < len(cards)):
        return False

    ace = cards[ind]

    # Step 1: Must start with Ace of correct suit
    if ace.value != 14:  # Ace is usually 14 in high->low
        return False
    if fs is not None and ace.suit != fs:
        return False

    # Step 2: Find a 5 of correct suit
    for i2, c in enumerate(cards):
        if c.value == 5:
            if fs is None or c.suit == fs:
                # Step 3: Check 5-4-3-2 from this 5
                if is_n_length_straight_at(hand, i2, fs, 4):
                    return True

    return False


def copy_straight(hand, ind, fs, ace_low=False):
    """Provided function: return answer straight at ind in hand."""
    ans = Deck()
    last_card = None
    target_len = 5
    assert not fs or hand.cards[ind].suit == fs
    if ace_low:
        assert hand.cards[ind].value == ACE
        last_card = hand.cards[ind]
        target_len = 4
        to_find = 5
        ind += 1
        pass
    else:
        # regular straight
        to_find = hand.cards[ind].value
        pass
    while len(ans.cards) < target_len:
        assert ind < len(hand.cards)
        if hand.cards[ind].value == to_find:
            if not fs or hand.cards[ind].suit == fs:
                ans.add_card(hand.cards[ind])
                to_find -= 1
                pass
            pass
        ind += 1
        pass
    if last_card is not None:
        ans.add_card(last_card)
        pass
    assert len(ans.cards) == 5
    return ans


def find_straight(hand, fs):
    """Provided funtion: look for a straight (or straight flush) in hand.

    If fs is not None, find any straight. Otherwise, find straight flush.
    Call the student's is_straight_at for each index.
    If found, copy_straight returns cards used for straight.
    """
    for i in range(0, len(hand.cards) - 4):
        if is_n_length_straight_at(hand, i, fs, 5):
            # straight
            return copy_straight(hand, i, fs)
        pass
    for i in range(0, len(hand.cards) - 4):
        if is_ace_low_straight_at(hand, i, fs):
            # ace-low straight
            return copy_straight(hand, i, fs, True)
        pass
    return None


def build_flush(hand, fs):
    """Provided function: build hand with flush suit fs."""
    ans = Deck()
    i = 0
    while len(ans.cards) < 5:
        assert i < len(hand.cards)
        if hand.cards[i].suit == fs:
            ans.add_card(hand.cards[i])
            pass
        i += 1
        pass
    return ans


def evaluate_hand(hand_unsorted):
    """Provided function: evaluate hand, and return tuple (hand, ranking)."""
    # copy the hand and sort it
    hand = Deck(hand_unsorted.cards)
    hand.sort()
    assert (
        len(hand.cards) >= 5
    ), f"A hand requires at least 5 cards but {hand} has {len(hand.cards)}"
    assert (
        len(hand.cards) <= 7
    ), f"A hand requires at most 7 cards but {hand} has {len(hand.cards)}"
    # straight flush
    fs = find_flush(hand)
    straight = find_straight(hand, fs)
    if fs and straight:
        return straight, "straight flush"
    # four of a kind
    val_counts = count_values(hand)
    v, n = get_max_count(hand, val_counts)
    assert n <= 4
    ind = get_kind_index(hand, v)
    if n == 4:
        return build_of_a_kind(hand, 4, ind), "four of a kind"
    # full house
    sec_pair = find_secondary_pair(hand, val_counts, v)
    if n == 3 and sec_pair is not None:
        ans = build_of_a_kind(hand, 3, ind)
        add_pair(hand, sec_pair, ans, 3)
        return ans, "full house"
    # flush
    if fs:
        return build_flush(hand, fs), "flush"
    # straight
    if straight:
        return straight, "straight"
    # three of a kind
    if n == 3:
        return build_of_a_kind(hand, 3, ind), "three of a kind"
    # two pair
    if n == 2 and sec_pair is not None:
        ans = build_of_a_kind(hand, 2, ind)
        add_pair(hand, sec_pair, ans, 2)
        return ans, "two pair"
    # pair
    if n == 2:
        return build_of_a_kind(hand, 2, ind), "pair"
    # high card
    ans = Deck()
    ans.cards = hand.cards[0:5]
    return ans, "high card"


if __name__ == "__main__":

    def check(input_hand_str, expected5_cards_str, expected_ranking):
        input_hand = hand_from_string(input_hand_str)
        expected5_cards = hand_from_string(expected5_cards_str)
        deck, ranking = evaluate_hand(input_hand)
        assert (
            ranking == expected_ranking
        ), f"Evaluate was incorrect for {input_hand}: gave {ranking} but expected {expected_ranking}"
        assert (
            expected5_cards == deck
        ), f"Evaluate was incorrect for {input_hand}: gave {deck} but expected {expected5_cards} [ranking was {ranking}]"
        pass

    # write find_flush first, then test
    check("Ac Kc Qc 0c 9c 8c", "Ac Kc Qc 0c 9c", "flush")
    check("Ad Kc Qd 0d 9d 8d", "Ad Qd 0d 9d 8d", "flush")
    check("Ad Kh Qh 0h 9h 8h", "Kh Qh 0h 9h 8h", "flush")
    check("As Kh Qs 0s 9s 8s", "As Qs 0s 9s 8s", "flush")
    check("Ah Kh Qd Jh 0h 2h", "Ah Kh Jh 0h 2h", "flush")
    check("As 0s 7s 5s 2s", "As 0s 7s 5s 2s", "flush")
    check("Ac 0c 7c 5c 2c", "Ac 0c 7c 5c 2c", "flush")
    check("Ad 0d 7d 5d 2d", "Ad 0d 7d 5d 2d", "flush")
    check("Ah 0h 7h 5h 2h", "Ah 0h 7h 5h 2h", "flush")
    check("As Kc Qs Js 0s 2s", "As Qs Js 0s 2s", "flush")
    print("---Finished test cases for flush---")
    # write count_values, get_max_count, get_kind_index, and build_of_a_kind
    # then test 4 of a kind, 3 of a kind, pair, and high card
    check("8c 5c 5d 5h 5s 2h", "5s 5h 5d 5c 8c", "four of a kind")
    check("As Ac Ah Ad 0s", "As Ah Ad Ac 0s", "four of a kind")
    check("0s 3s 3c 3h 3d", "3s 3h 3d 3c 0s", "four of a kind")
    check("As Ac Ad Kh 4c", "As Ad Ac Kh 4c", "three of a kind")
    check("As Kc Kd Kh 4c", "Kh Kd Kc As 4c", "three of a kind")
    check("As Kc 9d 9h 9c", "9h 9d 9c As Kc", "three of a kind")
    check("As Ac Kh 9d 4s", "As Ac Kh 9d 4s", "pair")
    check("4c 9d 5c 6h Ad 0d 6c", "6h 6c Ad 0d 9d", "pair")
    check("0h 8s Jd 8c Kc", "8s 8c Kc Jd 0h", "pair")
    check("Kd 4h 7d 0s Js Qd 4s", "4s 4h Kd Qd Js", "pair")
    check("3d 7h 3h Ah 9c", "3h 3d Ah 9c 7h", "pair")
    check("As Ac Kc Qd 4d", "As Ac Kc Qd 4d", "pair")
    check("3s 9h 5h Qh 6s 7s", "Qh 9h 7s 6s 5h", "high card")
    check("As 5s 0c 2c 9s Qs", "As Qs 0c 9s 5s", "high card")
    check("9d 8c 7h 6c 3d", "9d 8c 7h 6c 3d", "high card")
    check("As 0d 9c 8d 7d", "As 0d 9c 8d 7d", "high card")
    check("As Ks Qh 0s 9d 8s", "As Ks Qh 0s 9d", "high card")
    check("As Ks Qs Js 4d", "As Ks Qs Js 4d", "high card")
    print("---Finished test cases for N-of-a-kind---")
    # write find_secondary_pair and add_pair then,
    # test full house and two pair
    check("As Qd Qc 7s 7h 7d", "7s 7h 7d Qd Qc", "full house")
    check("As 9d 9c 9s 4h 4d", "9s 9d 9c 4h 4d", "full house")
    check("As Ac Ad Ks Kh", "As Ad Ac Ks Kh", "full house")
    check("Kh Kd 0h 0d 6h 6c", "Kh Kd 0h 0d 6h", "two pair")
    check("As Kh Kd Qh Qc 0c", "Kh Kd Qh Qc As", "two pair")
    check("As Ah Kh Kd Qc", "As Ah Kh Kd Qc", "two pair")
    check("0d 6c 0h 8s Jd 8c", "0h 0d 8s 8c Jd", "two pair")
    check("Jh 8d 8h Ks 2s Qc 2h", "8h 8d 2s 2h Ks", "two pair")
    check("As Ac 4h 4d Ks 2h", "As Ac 4h 4d Ks", "two pair")
    check("As Kh Kc Qd Qc", "Kh Kc Qd Qc As", "two pair")
    check("As Ac Kh Qc Qd", "As Ac Qd Qc Kh", "two pair")
    check("Kh Kd 0h 0d 6h 6c", "Kh Kd 0h 0d 6h", "two pair")
    print("---Finished test cases for full house/2 pair---")
    # write is_n_length_straight_at then,
    # test "normal" (not ace-low) straights that aren't straight flushes
    check("9d 8c 7h 6c 5d", "9d 8c 7h 6c 5d", "straight")
    check("Ac Kh 9d 8c 7h 6c 5d", "9d 8c 7h 6c 5d", "straight")
    check("9d 8c 7h 6c 5d 4s", "9d 8c 7h 6c 5d", "straight")
    check("9d 8c 7h 6c 5d 3s 2s", "9d 8c 7h 6c 5d", "straight")
    check("9d 8c 8h 7c 6c 5s", "9d 8h 7c 6c 5s", "straight")
    check("As Ac Kh Qd Jc 0s", "As Kh Qd Jc 0s", "straight")
    print("---Finished test cases for basic straights---")
    # make sure is_n_length_straight_at handles fs then,
    # test "normal" (not ace-low) straight flushes
    check("9d 8h 7h 6h 5h 4h", "8h 7h 6h 5h 4h", "straight flush")
    check("9d 8c 7c 6c 5c 4c", "8c 7c 6c 5c 4c", "straight flush")
    check("9d 8c 8d 8h 7d 6d 5d", "9d 8d 7d 6d 5d", "straight flush")
    check("As Ks Qs Js 0s", "As Ks Qs Js 0s", "straight flush")
    check("As Kh Ks Qs Js 0s", "As Ks Qs Js 0s", "straight flush")
    check("Ad Kd Qd Jd 0h 0d 0c", "Ad Kd Qd Jd 0d", "straight flush")
    print("---Finished test cases for basic straight flushes---")
    # write is_ace_low_straight_at then,
    # test ace low straights + straight flushes
    check("As 5d 4h 3s 2c", "5d 4h 3s 2c As", "straight")
    check("As 0s 5c 4d 4c 3h 2s", "5c 4d 3h 2s As", "straight")
    check("Ad 6h 5d 4d 3d 2d", "5d 4d 3d 2d Ad", "straight flush")
    check("As Ad 6h 5d 4d 3d 2d", "5d 4d 3d 2d Ad", "straight flush")
    check("As Ad 5d 4s 4d 3d 2d", "5d 4d 3d 2d Ad", "straight flush")
    check("As Ad 5d 4d 4c 3d 2d", "5d 4d 3d 2d Ad", "straight flush")
    print("Passed all the test cases in __main__ for evaluate")

    check("5s 5h 5d 5c 3s 3h", "5s 5h 5d 5c 3s", "four of a kind")
    check("5s 5h 5d 5c 4d", "5s 5h 5d 5c 4d", "four of a kind")

    pass
