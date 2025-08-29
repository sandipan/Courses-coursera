ACE = 14
KING = 13
QUEEN = 12
JACK = 11


def value_from_letter(let):
    # pass
    values = {"J": JACK, "Q": QUEEN, "K": KING, "A": ACE}
    # values.update({str(i):i for i in range(1,11)})
    value = -1
    if let in values:
        value = values[let]
    elif let.isdigit():
        value = int(let)
        if value == 0:
            value = 10
    if value < 2 or value > 14:
        raise ValueError("not a valid letter")
    return value


def check_suit(let):
    # pass
    if not let in {"s", "h", "d", "c"}:
        raise ValueError("not a valid suit")


def letter_from_value(val):
    # pass
    values = {JACK: "J", QUEEN: "Q", KING: "K", ACE: "A"}
    let = None
    if val in values:
        let = values[val]
    elif val >= 2 and val <= 10:
        val = val % 10
        let = str(val)
    else:
        raise ValueError("not a valid value")
    return let


class Card:

    def __init__(self, value_letter, suit_letter):
        self.unknown_card_num = int(suit_letter) if value_letter == "?" else None
        if self.unknown_card_num is None:
            if len(value_letter) != 1 or len(suit_letter) != 1:
                raise (ValueError("value / suit letter length should be 1"))
            check_suit(suit_letter)
            self.value = value_from_letter(value_letter)
            self.suit = suit_letter
        else:
            self.value, self.suit = 0, "?"

    def __str__(self):
        # pass
        return (
            letter_from_value(self.value) + self.suit
            if self.value != 0
            else f"?{self.unknown_card_num}"
        )

    def __repr__(self):
        # pass
        return f"Card({self.__str__()})"

    def __eq__(self, other):
        # pass
        return self.value == other.value and self.suit == other.suit

    def __lt__(self, other):
        # pass
        return self.value < other.value or (
            self.value == other.value and self.suit < other.suit
        )

    # pass


def card_from_num(num):
    # pass
    if num < 0 or num > 51:
        raise ValueError("num should be in the range 0-51")
    # suits = ["c", "d", "h", "s"]
    return Card(letter_from_value(num % 13 + 2), "cdhs"[num // 13])


# for num in range(52):
#    print(card_from_num(num))
