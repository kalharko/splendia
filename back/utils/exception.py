class TooMuchReservedCards(Exception):

    """Raised when a players tries to reserve a card but already has 3"""

    def __init__(self):
        super().__init__("Player tried to reserve a card but they already have 3.")


class CardIdNotFound(Exception):
    """Raised when a hand does not contain the requested card"""

    def __init__(self, cardId: int):
        super().__init__("The card with the id " + str(cardId) + " was not found.")


class NotEnoughTokens(Exception):
    """Raised when there are not enough tokens in a TokenArray to complete a transaction"""

    def __init__(self):
        super().__init__("They are not enough token in a token array to complete a transaction.")


class TooMuchBankTokens(Exception):
    """Raised when there are too much tokens in the bank to complete a transaction"""

    def __init__(self):
        super().__init__("They are too many tokens in the bank to complete a transaction.")


class NotEnoughTokensToTakeTwo(Exception):
    """Raised when tries to take 2 tokens of the same color when there are less than four of them in the bank"""

    def __init__(self):
        super().__init__("They are not enough tokens in the bank to take 2 of the same color.")


class PlayerCanNotPay(Exception):
    """Raised when a player can not pay"""

    def __init__(self):
        super().__init__("The player can not play.")


class BrokenTokenArray(Exception):
    """Raised when a TokenArray has negative number of tokens after subtraction"""

    def __init__(self):
        super().__init__("A token array has a negative amounts of tokens after a substraction.")


class InvalidTakeTokenAction(Exception):
    """Raised when an invalid take token action is tried"""

    def __init__(self):
        super().__init__("An invalid action to take tokens was tried.")


class EmptyDeck(Exception):
    """Raised when a deck is empty and can not be drawn from"""

    def __init__(self):
        super().__init__("It is impossible to draw a card due to the deck being empty.")


class InvalidRejectTokenAction(Exception):
    """Raised when a reject token action is invalid"""

    def __init__(self):
        super().__init__("A reject token action is invalid.")


class InvalidNbPlayer(Exception):
    """Raised when a number of players is rejected"""

    def __init__(self, nbPlayer: int):
        super().__init__("The number of players is invalid. It should be between 2 and 4. " +
                         str(nbPlayer) + " was given instead.")
