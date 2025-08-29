from card import Card, card_from_num
from deck import Deck, draw_all_unknowns
from poker_input import hand_from_string

if __name__ == "__main__":
    h1 = hand_from_string("?2 As ?3 Kc Kh ?0 ?1 3s ?4")
    rd1 = hand_from_string("5h 6c Jc Ac Ah")
    draw_all_unknowns([h1], rd1)
    expected = hand_from_string("Jc As Ac Kc Kh 5h 6c 3s Ah")
    assert h1 == expected, f"Expected {expected} but got {h1}"
    # we should be able to fill in multiple hands
    # (including the same one again)
    h2 = hand_from_string("?5 As ?3 Kc Qd ?0 ?6 3s ?4")
    h3 = hand_from_string("?2 As ?3 Kc Kh ?0 ?6 3s ?4")
    h4 = hand_from_string("?5 As ?3 Kc Qd ?0 ?1 3s ?4")
    rd2 = hand_from_string("9s Jd 2h Ad 3h 5c 6c")

    draw_all_unknowns([h1, h2, h3, h4], rd2)
    
    ex1 = hand_from_string("2h As Ad Kc Kh 9s Jd 3s 3h")
    ex2 = hand_from_string("5c As Ad Kc Qd 9s 6c 3s 3h")
    ex3 = hand_from_string("2h As Ad Kc Kh 9s 6c 3s 3h")
    ex4 = hand_from_string("5c As Ad Kc Qd 9s Jd 3s 3h")
    for (h,e) in [(h1, ex1), (h2, ex2), (h3, ex3), (h4, ex4)]:
        assert h == e, f"Expected {e} but got {h}"
        pass
    print("All tests passed for draw_all_unknowns")
    pass
