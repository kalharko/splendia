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
    tokens: List[int]

    def __init__(self, value: List[int] = None) -> None:
        self.tokens = value if value else [0, 0, 0, 0, 0, 0]

    def withdraw_token(self, color: Color, amount: int) -> None:
        if self.tokens[color] > amount:
            self.tokens[color] -= amount
            return
        else:
            return Exception("Not enough tokens")

    def withdraw_tokens(self, tokens) -> None: #tokens : TokenArray
        if not self.can_withdraw(tokens):
            return NotEnoughTokens()
        else:
            self.tokens = [x - y for x, y in zip(self.tokens, tokens.tokens)]

    def deposit_token(self, color: Color, amount: int) -> None:
        "TODO : write the function"
        pass

    def deposit_tokens(self, tokens) -> None: #tokens : TokenArray
        self.tokens = [x + y for x, y in zip(self.tokens, tokens.tokens)]
        pass

    def nb_of_tokens(self):
        return sum(self.tokens)

    def can_withdraw(self, other) -> bool: #tokens : TokenArray
        comparison = [x >= y for x, y in zip(self.tokens, other.tokens)]
        return comparison == [True for x in range(len(comparison))]

    def can_pay(self, other: 'TokenArray') -> bool:
        assert other.tokens[-1] == 0

        # can pay without gold
        comparison = [x >= y for x, y in zip(self.tokens, other.tokens[:-1])]
        if comparison == [True for x in range(len(comparison))]:
            return True

        # can pay with gold
        gold_needed = -sum([x - y if x - y < 0 else 0 for x, y in zip(self.tokens, other.tokens[:-1])])
        if gold_needed <= self.tokens[-1]:
            return True
        return False

    def __iadd__(self, other):
        self.tokens = [x + y for x, y in zip(self.tokens, other.tokens)]
        return self

    def __isub__(self, other):
        assert isinstance(other, TokenArray)
        self.tokens = [x - y for x, y in zip(self.tokens, other.tokens)]
        return self

    def __add__(self, other):
        assert isinstance(other, TokenArray)
        return TokenArray([x + y for x, y in zip(self.tokens, other.tokens)])

    def __sub__(self, other):
        assert isinstance(other, TokenArray)
        return TokenArray([x - y for x, y in zip(self.tokens, other.tokens)])

    def __ge__(self, other):
        assert isinstance(other, TokenArray)
        comparison = [x >= y for x, y in zip(self.tokens, other.tokens)]
        return comparison == [True for x in range(len(comparison))]

    def __le__(self, other):
        assert isinstance(other, TokenArray)
        comparison = [x <= y for x, y in zip(self.tokens, other.tokens)]
        return comparison == [True for x in range(len(comparison))]

    def __isub__(self, other):
        assert isinstance(other, TokenArray)
        assert other.tokens[-1] == 0
        assert self.can_pay(other)

        self.tokens = [x - y for x, y in zip(self.tokens, other.tokens)]
        for i in range(5):
            if self.tokens[i] < 0:
                self.tokens[-1] += self.tokens[i]
                self.tokens[i] = 0
        return self
