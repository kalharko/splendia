from dataclasses import dataclass
from typing import List
from enum import Enum
from django.db import models


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
class TokenArray(models.Model):
    """This class represents a token inventory.
    py:class:: Class documentation ?
    """
    tokens: List[int] = models.ForeignKey(int, on_delete=models.CASCADE)

    def __init__(self, value: List[int] = None) -> None:
        self.tokens = value if value else [0, 0, 0, 0, 0, 0]

    def withdraw_token(self, color: Color, amount: int) -> None:
        if self.tokens[color] > amount:
            self.tokens[color] -= amount
            return
        else:
            return Exception("Not enough tokens")

    def withdraw_tokens(self, amount: List[int]) -> None:
        "TODO : write the function"
        pass

    def deposit_token(self, color: Color, amount: int) -> None:
        "TODO : write the function"
        pass

    def deposit_tokens(self, amount: List[int]) -> None:
        "TODO : write the function"
        pass

    def nb_of_tokens(self):
        return sum(self.tokens)

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
        assert other.tokens[-1] == 0
        assert self.can_pay(other)

        self.tokens = [x - y for x, y in zip(self.tokens, other.tokens)]
        for i in range(5):
            if self.tokens[i] < 0:
                self.tokens[-1] += self.tokens[i]
                self.tokens[i] = 0
        return self
