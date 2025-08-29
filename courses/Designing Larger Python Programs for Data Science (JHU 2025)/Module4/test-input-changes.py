from card import Card, card_from_num
from deck import Deck
from poker_input import hand_from_string

def test_input_changes_valid():
    #check hand_from_string on valid inputs
    data = [ ("As Ks Qh", [(14, 's', None), (13, 's', None), (12, 'h', None)]), 
             ("As ?0 3c ?1", [(14, 's', None), (0, '?', 0), (3, 'c', None), (0, '?', 1)]),
             ("?0 ?1 ?2 ?3", [(0, '?', 0), (0, '?', 1), (0, '?', 2),(0, '?', 3)]),
             ("?0 ?11 3d ?12 Ac", [(0, '?', 0), (0, '?', 11), (3, 'd', None), (0, '?', 12),(14, 'c', None)])]
    for (hand_str,hand_vals) in data:
        hand = hand_from_string(hand_str)
        assert len(hand.cards) == len(hand_vals), "Different number of cards in hand {len(hand.cards)} from what was expected {len(hand_vals)} for {hand_str}"
        for i in range(0,len(hand.cards)):
            c=hand.cards[i]
            (ex_v, ex_s, ex_ucn) = hand_vals[i]
            assert c.value == ex_v
            assert c.suit == ex_s
            if ex_ucn is None:
                assert c.unknown_card_num is None
            else:
                assert c.unknown_card_num == ex_ucn
                pass
        pass
    pass
def test_input_changes_error_cases():
    # check hand_from_string on inputs that should generate errors
    # each of these should produce ValueError:
    hand_strs = ["As Kh Qs0 Jc", #Qs0 is not valid
                 "As K Qs Jc",   #K no suit is not valid
                 "As ? Qs Jc",   #? with no number is not valid
                 "As ?s Qs Jc",  #?s is not valid (should be detected in Card)
                 "?0 A Qs Jc"    #A without suit is not valid
                 ]
    for h in hand_strs:
        try:
            v= hand_from_string(h)
            assert False, f"hand_from_string({h}) should raise ValueError but gave {v}"
        except ValueError:
            pass
        except e:
            assert False, f"hand_from_string({h}) should raise ValueError but raised {e}"
            pass
        
    pass
if __name__ == "__main__":
    test_input_changes_valid()
    test_input_changes_error_cases()
    print("All tests passed for input changes")
    pass
