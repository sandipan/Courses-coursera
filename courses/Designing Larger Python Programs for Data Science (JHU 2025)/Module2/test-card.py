from card import Card, card_from_num, value_from_letter, check_suit, letter_from_value

def test_check_suit():
    for s in "cdhs":
        check_suit(s)
        print(f"check_suit did not report any error for {s} (good)")
        pass
    for s in "2AQnbm!S4(":
        try:
            check_suit(s)
            assert False, f"check suit failed to throw ValueError for {s}"
        except ValueError:
            print(f"check suit correctly threw ValueError for {s} (good)")
        except Exception as e:
            assert False, f"check suit incorrectly threw {type(e)}:{e} instead of ValueError for {s}"
            pass
        pass    

def test_value_from_letter_valid():
    assert(value_from_letter('2')==2)
    assert(value_from_letter('3')==3)
    assert(value_from_letter('4')==4)
    assert(value_from_letter('5')==5)
    assert(value_from_letter('6')==6)
    assert(value_from_letter('7')==7)
    assert(value_from_letter('8')==8)
    assert(value_from_letter('9')==9)
    assert(value_from_letter('0')==10)
    assert(value_from_letter('J')==11)
    assert(value_from_letter('Q')==12)
    assert(value_from_letter('K')==13)
    assert(value_from_letter('A')==14)
    pass
def test_value_from_letter_errors():
    for letter in ['x', 'Y', 'Z', '!', '23', '#', 'AK', '1', 'a', 'k', 'q', 'j', 'o', 'O', ' ', '.', ',']:
        try:
            ans=value_from_letter(letter)
            assert False, f"value_from_letter({letter}) should raise ValueError but gave {ans}"
        except ValueError:
            print(f"value_from_letter({letter}) corrected raised ValueError (good)")
            pass
        except Exception as e:
            assert False,  f"value_from_letter({letter}) should raise ValueError but raised {type(e)}:{e}"
            pass
        pass
    pass

def test_letter_from_value():
    assert(letter_from_value(2)=='2')
    assert(letter_from_value(3)=='3')
    assert(letter_from_value(4)=='4')
    assert(letter_from_value(5)=='5')
    assert(letter_from_value(6)=='6')
    assert(letter_from_value(7)=='7')
    assert(letter_from_value(8)=='8')
    assert(letter_from_value(9)=='9')
    assert(letter_from_value(10)=='0')
    assert(letter_from_value(11)=='J')
    assert(letter_from_value(12)=='Q')
    assert(letter_from_value(13)=='K')
    assert(letter_from_value(14)=='A')
    pass
    

# write all of your test cases here, then run it as python3 test-card.py
def main():
    # Provided by use to test check_suit, value_from_letter, and letter_from_value
    test_check_suit()
    test_value_from_letter_valid()
    test_value_from_letter_errors()
    test_letter_from_value()
    # note: we dont need any error cases for letter_from_value since Card
    # only ever sets self.value to valid values

    # test constructor

    # test str and repr

    # test eq and lt

    # test card_from_num (try building a full deck)

    # error cases
    # invalid value

    
    # Here is an example of how to test
    # invalid inputs, as they throw exceptions
    try:
        c = Card('G','s')  # 'G' is an invalid value
        assert False, f"Card('G','s') incorrectly created {c}"
    except ValueError:
        print("Card('G','s') correctly raised ValueError")
    except Exception as e:
        assert False, f"Card('G','s') incorectly raised {type(e)}:{e} should be ValueError"
        pass
    
    # invalid suit

    # invalid inputs to card_from_num

    return 0


if __name__ == '__main__':
    main()
    pass
