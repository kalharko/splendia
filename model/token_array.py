from dataclasses import dataclass
from typing import List
from enum import Enum

from model.utils.exception import BrokenTokenArray


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

    def can_buy(self, other: 'TokenArray') -> bool:
        for color_index in range(len(self.tokens)):
            if self.tokens[color_index] < other.tokens[color_index]:
                return False
        return True




    def __iadd__(self, other):
        self.tokens = [x + y for x, y in zip(self.tokens, other.tokens)]
        return self

    def __isub__(self, other):
        self.tokens = [x - y for x, y in zip(self.tokens, other.tokens[:-1])]
        for i in range(len(self.tokens) - 1):
            if self.tokens[i] < 0:
                self.tokens[5] += self.tokens[i]
                self.tokens[i] = 0
        if self.tokens[-1] < 0:
            raise BrokenTokenArray()
        return self

    def __ge__(self, other):
        distance = sum([x - y if x - y > 0 else 0 for x, y in zip(self.tokens, other.tokens[:-1])])
        return distance <= self.tokens[5]
