

class TooMuchReservedCards(Exception):
    "Raised when a players tries to reserve a card but already has 3"


class CardIdNotFound(Exception):
    "Raised when a hand does not contain the requested card"


class NotEnoughTokens(Exception):
    "Raised when there are not enough tokens in a TokenArray to complete a transaction"


class TooMuchBankTokens(Exception):
    "Raised when there are too much tokens in the bank to complete a transaction"


class NotEnoughTokensToTakeTwo(Exception):
    "Raised when tries to take 2 tokens of the same color when there are less than four of them in the bank"


class PlayerCanNotPay(Exception):
    "Raised when a player can not pay"


class BrokenTokenArray(Exception):
    "Raised when a TokenArray has negative number of tokens after subtraction"
