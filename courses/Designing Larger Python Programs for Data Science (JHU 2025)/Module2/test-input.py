from card import Card, card_from_num
from deck import Deck
from poker_input import hand_from_string, read_input


def test_hand_from_string():
    test_cases = [["As", "Kh", "4d", "Qc"],
                  ["2d", "3d", "4c", "5h", "9c", "0s"],
                  ["5c"]]
    for tc in test_cases:
        hstr=" ".join(tc)
        h = hand_from_string(hstr)
        expected = Deck([Card(s[0],s[1]) for s in tc])
        assert h == expected, f"hand_from_string({hstr}) gave {h} but expected {expected}"
        pass
    try:
        r=hand_from_string("As K Qc")
        assert False, f'hand_from_string("As K Qc") should raise ValueError but gave {r}'
    except ValueError:
        pass
    except Exception as e:
        assert False, f'hand_from_string("As K Qc") should raise ValueError but raised {type(e)}'
        pass
    try:
        r=hand_from_string("As Kcc Qc")
        assert False, f'hand_from_string("As Kcc Qc") should raise ValueError but gave {r}'
    except ValueError:
        pass
    except Exception as e:
        assert False, f'hand_from_string("As Kcc Qc") should raise ValueError but raised {type(e)}'
        pass
    pass

def test_read_input():
    hands = read_input("test.txt")
    data=[["Kh", "Qh", "As", "4c", "2c"],
          ["Ac", "Qc", "As", "4c", "2c"],
          ["Qh", "0s", "9h", "8d", "8s", "7d", "6c"],
          ["Qh", "Jc", "0s", "9h", "9d", "5h", "4h"]]
    expected=[Deck([Card(s[0],s[1]) for s in hand_str]) for hand_str in data]
    assert len(hands) == len(expected), f"Read wrong number of hands: expected {len(expected)}, but had {len(hands)}"
    for i in range(0, len(hands)):
        assert hands[i] == expected[i], f"Hand {i} is incorrect. Expected {expected[i]} but got {hands[i]}"
        pass
    pass

if __name__ == "__main__":
    print("Testing hand_from_string")
    test_hand_from_string()
    print("Testing read_input")
    test_read_input()
    print("Tests passed")
    pass
    
