from card import Card

def test_card_changes():
    #  make ?0 ?1... ?20
    for i in range(0, 20):
        s = str(i)
        c = Card('?', s)
        assert c.value==0
        assert c.suit=='?'
        assert c.unknown_card_num == i
        assert str(c) == f"?{s}"
        # make sure that changing value/suit
        # results in correct string conversion
        c.value = 6
        c.suit = 's'
        assert str(c) == "6s"
        pass
    try:
        c = Card('?', 's')
        assert False, "Card('?', 's') should raise ValueError"
    except ValueError:
        pass
    except e:
        assert False, f"Card('?', 's') raised {e} not ValueError"
        pass
    # now some legal cards:
    values = [('A','s', 14), ('K', 'h', 13), ('0','c',10), ('2','d',2)] 
    for (vname, sname, vnum) in values:
        c = Card(vname,sname)
        assert c.value == vnum
        assert c.suit == sname
        assert c.unknown_card_num is None
        pass
    pass


if __name__ == "__main__":
    test_card_changes()
    print("All tests passed for Card changes")
    pass
