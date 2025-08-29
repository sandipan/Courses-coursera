from card import Card, card_from_num
from deck import Deck
from poker_input import hand_from_string

if __name__ == "__main__":
    d = hand_from_string("?2 As ?3 Kc Kh ?0 ?1 3s ?4")
    d.fill_unknown_card(0,Card('5','h'))
    d.fill_unknown_card(1,Card('6','c'))
    d.fill_unknown_card(2,Card('J','c'))
    d.fill_unknown_card(3,Card('A','c'))
    d.fill_unknown_card(4,Card('A','h'))
    expected = hand_from_string("Jc As Ac Kc Kh 5h 6c 3s Ah")
    assert d == expected, f"Expected {expected} but got {d}"
    # we should be able to fill them in with different values
    # and have everything still work
    d.fill_unknown_card(0,Card('9','s'))
    d.fill_unknown_card(1,Card('J','d'))
    d.fill_unknown_card(2,Card('2','h'))
    d.fill_unknown_card(3,Card('A','d'))
    d.fill_unknown_card(4,Card('3','h'))
    expected = hand_from_string("2h As Ad Kc Kh 9s Jd 3s 3h")
    assert d == expected, f"Expected {expected} but got {d}"
    print("All tests passed for fill unknown cards")
    pass
