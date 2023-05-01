class TooMuchReservedCards(Exception):
    "Raised when a players tries to reserve a card but already has 3"

    def __init__(self):
        super().__init__()


class CardIdNotFound(Exception):
    "Raised when a hand does not contain the requested card"

    def __init__(self):
        super().__init__()


class NotEnoughTokens(Exception):
    "Raised when there are not enough tokens in a TokenArray to complete a transaction"

    def __init__(self):
        super().__init__()


class TooMuchBankTokens(Exception):
    "Raised when there are too much tokens in the bank to complete a transaction"

    def __init__(self):
        super().__init__()


class NotEnoughTokensToTakeTwo(Exception):
    "Raised when tries to take 2 tokens of the same color when there are less than four of them in the bank"

    def __init__(self):
        super().__init__()


class PlayerCanNotPay(Exception):
    "Raised when a player can not pay"

    def __init__(self):
        super().__init__()


class BrokenTokenArray(Exception):
    "Raised when a TokenArray has negative number of tokens after subtraction"

    def __init__(self):
        super().__init__()


class InvalidTakeTokenAction(Exception):
    "Raised when an invalid take token action is tried"

    def __init__(self):
        super().__init__()


class EmptyDeck(Exception):
    "Raised when a deck is empty and can not be drawn from"

    def __init__(self):
        super().__init__()


class InvalidRejectTokenAction(Exception):
    "Raised when a reject token action is invalid"

    def __init__(self):
        super().__init__()
