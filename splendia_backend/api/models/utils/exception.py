

class TooManyReservedCardsException(Exception):
    "Raised when a players tries to reserve a card but already has 3"


class CardIdNotFoundException(Exception):
    "Raised when a hand does not contian the requested card"


class NotEnoughTokensException(Exception):
    "Raised when there are not enough tokens in the bank to complete a transaction"


class NotEnoughTokensToTakeTwoException(Exception):
    "Raised when tries to take 2 tokens of the same color when there are less than four of them in the bank"


class PlayerCanNotPayException(Exception):
    "Raised when a player can not pay"


class BrokenTokenArray(Exception):
    "Raised when a TokenArray has negative number of tokens after substraction"
