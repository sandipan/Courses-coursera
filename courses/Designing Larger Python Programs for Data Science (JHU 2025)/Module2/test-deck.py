from card import Card, card_from_num
from deck import Deck, build_remaining_deck


# this computes the permutations of the list
# and makes a dictionary mapping each permutation
# to 0.  We use it to count outcomes for shuffle
def build_perm_dict(lst):
    d = {}

    def helper(start, rest):
        if rest == []:
            start_str = " ".join(start)
            d[start_str] = 0
            return
        else:
            for x in rest:
                temp = start[:]
                temp.append(x)
                r2 = rest[:]
                r2.remove(x)
                helper(temp, r2)
                pass
            pass
        pass

    helper([], lst)
    return d


# we have provided you with some starting tests
# but we encourage you to add more!
def main():
    d = Deck()
    assert d.cards == []
    card_list = [
        Card("4", "d"),
        Card("A", "s"),
        Card("9", "h"),
        Card("3", "c"),
        Card("0", "d"),
    ]
    d2 = Deck(card_list)
    assert d2.cards == card_list, "d2 should have a copy of card_list for its cards"
    assert (
        d2.cards is not card_list
    ), "d2 should have a copy, but points at the same object"
    assert str(d2) == "4d As 9h 3c 0d"
    assert repr(d2) == "Deck(4d As 9h 3c 0d)"
    d.add_card(Card("Q", "h"))
    assert str(d) == "Qh"
    d2.add_card(Card("K", "d"))
    assert str(d2) == "4d As 9h 3c 0d Kd"
    d2.sort()
    assert str(d2) == "As Kd 0d 9h 4d 3c"
    d3 = Deck()
    for i in range(0, 52):
        c = card_from_num(i)
        d3.add_card(c)
        pass
    d3.assert_full()
    d.add_card(Card("7", "c"))
    d.add_card(Card("2", "s"))
    d.add_card(Card("A", "d"))
    perm_dict = build_perm_dict(["Qh", "7c", "2s", "Ad"])
    # shuffle cards and see how many times we get
    # each arrangment
    # we do it 1000 * (number of outcomes) times
    # so we expect close to 1000 of each ordering
    for i in range(0, len(perm_dict) * 1000):
        d.shuffle()
        s = str(d)
        assert s in perm_dict, f"shuffle resulted in an invalid deck: {s}"
        perm_dict[s] += 1
        pass
    # we'll consider it good enough if each ordering came up between
    # 700 and 1300 times (+/- 30% of ideal).
    for p in perm_dict:
        assert perm_dict[p] >= 700, f"Very few ({perm_dict[p]}) occurences of {p}"
        assert perm_dict[p] <= 1300, f"Very many ({perm_dict[p]}) occurences of {p}"
        pass
    print("Passed test cases for deck.py")
    return 0


if __name__ == "__main__":
    main()
    pass
