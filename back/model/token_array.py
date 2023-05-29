from dataclasses import dataclass
from typing import List
from enum import Enum

from utils.exception import NotEnoughTokens


class Color(Enum):
    """This enum describes the splendor game token colors.
    """

    WHITE = 0
    BLUE = 1
    GREEN = 2
    RED = 3
    BLACK = 4
    GOLD = 5


@dataclass
class TokenArray():
    """This class describes a splendor game token array.

    Attributes:
    _tokens (List[int]): The number of tokens for each color.
    """
    _tokens: List[int]

    def __hash__(self):
        """Magic operator for the function hash(TokenArray)

        Returns:
            hash : hash
            """

        return hash(tuple(self._tokens))

    def __init__(self, value: List[int] = None) -> None:
        """The constructor for the TokenArray class.

        Args:
            value (List[int]): The number of tokens for each color.
            """
        assert isinstance(value, list) or value is None
        assert value is None or len(value) == 6

        self._tokens = value if value else [0, 0, 0, 0, 0, 0]

    def withdraw_token(self, color: Color, amount: int) -> None or NotEnoughTokens:
        """Withdraws a given amount of tokens of a given color.

        Args:
            color (Color): The color of the tokens to withdraw.
            amount (int): The amount of tokens to withdraw.

        Returns:
            None or NotEnoughTokens: None if the withdrawal was successful, NotEnoughTokens otherwise.
            """
        assert isinstance(color, Color)
        assert isinstance(amount, int)

        if self._tokens[color.value] > amount:
            self._tokens[color.value] -= amount
            return
        else:
            return NotEnoughTokens()

    def withdraw_tokens(self, tokens) -> None or NotEnoughTokens:
        """Withdraws a given amount of tokens of a given color.

        Args:
            tokens (TokenArray): The tokens to withdraw.

        Returns:
            None or NotEnoughTokens: None if the withdrawal was successful, NotEnoughTokens otherwise.
            """
        assert isinstance(tokens, TokenArray)

        if not self.can_withdraw(tokens):
            return NotEnoughTokens()
        else:
            self._tokens = [x - y for x,
                            y in zip(self._tokens, tokens.get_tokens())]

    def deposit_token(self, color: Color, amount: int) -> None:
        """Deposits a given amount of tokens of a given color.

        Args:
            color (Color): The color of the tokens to deposit.
            amount (int): The amount of tokens to deposit.
            """
        assert isinstance(color, Color)
        assert isinstance(amount, int)

        self._tokens[color.value] += amount

    def deposit_tokens(self, tokens) -> None:
        """Deposits tokens.

        Args:
            tokens (TokenArray): The tokens to deposit.
            """
        assert isinstance(tokens, TokenArray)

        self._tokens = [x + y for x,
                        y in zip(self._tokens, tokens.get_tokens())]

    def nb_of_tokens(self):
        """Returns the number of tokens.

        Returns:
            int: The number of tokens.
            """

        return sum(self._tokens)

    def can_withdraw(self, other: 'TokenArray') -> bool:
        """Checks if the token array can withdraw a given token array.

        Args:
            other (TokenArray): The token array to withdraw.

        Returns:
            bool: True if the withdrawal is possible, False otherwise.
            """
        assert isinstance(other, TokenArray)

        comparison = [x >= y for x, y in zip(self._tokens, other.get_tokens())]
        return comparison == [True for x in range(len(comparison))]

    def can_pay(self, other: 'TokenArray') -> bool:
        """Checks if the token array can pay a given token array.

        Args:
            other (TokenArray): The token array to pay.

        Returns:
            bool: True if the payment is possible, False otherwise.
            """
        assert other.get_tokens()[Color.GOLD.value] == 0
        assert isinstance(other, TokenArray)

        # can pay without gold
        comparison = [x >= y for x, y in zip(
            self._tokens, other.get_tokens()[:-1])]
        if comparison == [True for x in range(len(comparison))]:
            return True

        # can pay with gold
        gold_needed = -sum([x - y if x - y < 0 else 0 for x,
                           y in zip(self._tokens, other.get_tokens()[:-1])])
        if gold_needed <= self._tokens[-1]:
            return True
        return False

    def pay(self, other: 'TokenArray') -> 'TokenArray':
        """Pays a given token array.

        Args:
            other (TokenArray): The token array to pay.

        Returns:
            TokenArray: The tokens to deposit.
            """
        assert isinstance(other, TokenArray)
        assert other.get_tokens()[Color.GOLD.value] == 0
        assert self.can_pay(other)

        before = self.get_tokens()
        self._tokens = [x - y for x,
                        y in zip(self._tokens, other.get_tokens())]

        for i in range(5):
            if self._tokens[i] < 0:
                self._tokens[-1] += self._tokens[i]
                self._tokens[i] = 0
        after = self.get_tokens()
        to_deposit = [x - y for x, y in zip(before, after)]

        return TokenArray(to_deposit)

    def __iadd__(self, other: 'TokenArray') -> 'TokenArray':
        """Adds a given token array to the current token array.

        Args:
            other (TokenArray): The token array to add.

        Returns:
            TokenArray: The current token array.
            """
        assert isinstance(other, TokenArray)

        self._tokens = [x + y for x,
                        y in zip(self._tokens, other.get_tokens())]
        return self

    def __isub__(self, other: 'TokenArray') -> 'TokenArray':
        """Substracts a given token array to the current token array.

        Args:
            other (TokenArray): The token array to substract.

        Returns:
            TokenArray: The current token array.
            """
        assert isinstance(other, TokenArray)

        self._tokens = [x - y for x,
                        y in zip(self._tokens, other.get_tokens())]
        return self

    def __add__(self, other: 'TokenArray') -> 'TokenArray':
        """Adds a given token array to the current token array.

        Args:
            other (TokenArray): The token array to add.

        Returns:
            TokenArray: The current token array.
            """
        assert isinstance(other, TokenArray)

        return TokenArray([x + y for x, y in zip(self._tokens, other.get_tokens())])

    def __sub__(self, other: 'TokenArray') -> 'TokenArray':
        """Substracts a given token array to the current token array.

        Args:
            other (TokenArray): The token array to substract.

        Returns:
            TokenArray: The current token array.
            """
        assert isinstance(other, TokenArray)

        return TokenArray([x - y for x, y in zip(self._tokens, other.get_tokens())])

    def __ge__(self, other: 'TokenArray') -> bool:
        """Checks if the current token array is greater or equal to a given token array.

        Args:
            other (TokenArray): The token array to compare.

        Returns:
            bool: True if the current token array is greater or equal to the given token array, False otherwise.
            """
        assert isinstance(other, TokenArray)

        comparison = [x >= y for x, y in zip(self._tokens, other.get_tokens())]
        return comparison == [True for x in range(len(comparison))]

    def __le__(self, other: 'TokenArray') -> bool:
        """Checks if the current token array is less or equal to a given token array.

        Args:
            other (TokenArray): The token array to compare.

        Returns:
            bool: True if the current token array is less or equal to the given token array, False otherwise.
            """
        assert isinstance(other, TokenArray)

        comparison = [x <= y for x, y in zip(self._tokens, other.get_tokens())]
        return comparison == [True for x in range(len(comparison))]

    def get_tokens(self) -> list[int]:
        """Returns the tokens.

        Returns:
            list[int]: The tokens.
            """

        return self._tokens

    def __str__(self) -> str:
        return str(self._tokens)
