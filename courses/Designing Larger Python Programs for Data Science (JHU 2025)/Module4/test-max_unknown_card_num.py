from card import Card, card_from_num
from deck import Deck
from poker_input import hand_from_string

if __name__ == "__main__":
    test_data= [("As ?0 Ac ?1", 1),
                ("As Kh Ac Qc", -1),
                ("As ?1 Ac ?0", 1),
                ("As Kc 4h ?0", 0),
                ("?4 Ac ?1 Kc 6s ?0 ?2", 4),
                ("Ah Kh ?3 ?5 3h 4s ?10", 10)
                ]
    for h_str, mv in test_data:
        d = hand_from_string(h_str)
        mucn = d.max_unknown_card_num() 
        assert mucn == mv, f"max_unknown_card_num({d}) was {mucn} but should be {mv}"
        pass
    print("All tests passed for max_unknown_card_num")
    pass
