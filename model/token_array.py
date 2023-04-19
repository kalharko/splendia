from dataclasses import dataclass
from typing import List
from enum import Enum

from model.utils.exception import NotEnoughTokens


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
    """This class represents a token inventory.
    py:class:: Class documentation ?
    """
    _tokens: List[int]

    def __init__(self, value: List[int] = None) -> None:
        assert isinstance(value, list) or value == None
        assert value == None or len(value) == 6
        self._tokens = value if value else [0, 0, 0, 0, 0, 0]

    def withdraw_token(self, color: Color, amount: int) -> None:
        if self._tokens[color.value] > amount:
            self._tokens[color.value] -= amount
            return
        else:
            return NotEnoughTokens()

    def withdraw_tokens(self, tokens) -> None: #tokens : TokenArray
        assert isinstance(tokens, TokenArray)
        if not self.can_withdraw(tokens):
            return NotEnoughTokens()
        else:
            self._tokens = [x - y for x, y in zip(self._tokens, tokens.get_tokens())]

    def deposit_token(self, color: Color, amount: int) -> None:
        self._tokens[color.value] += amount

    def deposit_tokens(self, tokens) -> None: #tokens : TokenArray
        assert isinstance(tokens, TokenArray)
        self._tokens = [x + y for x, y in zip(self._tokens, tokens.get_tokens())]

    def nb_of_tokens(self):
        return sum(self._tokens)

    def can_withdraw(self, other) -> bool: #tokens : TokenArray
        assert isinstance(other, TokenArray)
        comparison = [x >= y for x, y in zip(self._tokens, other.get_tokens())]
        return comparison == [True for x in range(len(comparison))]

    def can_pay(self, other: 'TokenArray') -> bool:
        assert other.get_tokens()[Color.GOLD.value] == 0
        assert isinstance(other, TokenArray)

        # can pay without gold
        comparison = [x >= y for x, y in zip(self._tokens, other.get_tokens()[:-1])]
        if comparison == [True for x in range(len(comparison))]:
            return True

        # can pay with gold
        gold_needed = -sum([x - y if x - y < 0 else 0 for x, y in zip(self._tokens, other.get_tokens()[:-1])])
        if gold_needed <= self._tokens[-1]:
            return True
        return False

    def pay(self, other: 'TokenArray') -> None: #other: TokenArray
        assert isinstance(other, TokenArray)
        assert other.get_tokens()[Color.GOLD.value] == 0
        assert self.can_pay(other)

        self._tokens = [x - y for x, y in zip(self._tokens, other.get_tokens())]
        for i in range(5):
            if self._tokens[i] < 0:
                self._tokens[-1] += self._tokens[i]
                self._tokens[i] = 0
        return self

    def __iadd__(self, other):
        self._tokens = [x + y for x, y in zip(self._tokens, other.get_tokens())]
        return self

    def __isub__(self, other):
        assert isinstance(other, TokenArray)
        self._tokens = [x - y for x, y in zip(self._tokens, other.get_tokens())]
        return self

    def __add__(self, other):
        assert isinstance(other, TokenArray)
        return TokenArray([x + y for x, y in zip(self._tokens, other.get_tokens())])

    def __sub__(self, other):
        assert isinstance(other, TokenArray)
        return TokenArray([x - y for x, y in zip(self._tokens, other.get_tokens())])

    def __ge__(self, other):
        assert isinstance(other, TokenArray)
        comparison = [x >= y for x, y in zip(self._tokens, other.get_tokens())]
        return comparison == [True for x in range(len(comparison))]

    def __le__(self, other):
        assert isinstance(other, TokenArray)
        comparison = [x <= y for x, y in zip(self._tokens, other.get_tokens())]
        return comparison == [True for x in range(len(comparison))]

    def get_tokens(self):
        return self._tokens
