from dataclasses import dataclass
from typing import List
from enum import Enum


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
