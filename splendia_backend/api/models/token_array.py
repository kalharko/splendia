from dataclasses import dataclass
from typing import List
from enum import Enum
from django.db import models
import json


class Color(Enum):
    """This enum describes the splendor game token colors.
    """

    WHITE = 0
    BLUE = 1
    GREEN = 2
    RED = 3
    BLACK = 4
    GOLD = 5

class TokenArrayManager(models.Manager):
    def create_token_array(self, value: List[int] = None):
        token_array = self.create(tokensJSON = "")
        token_array.set_tokens(value if value else [0, 0, 0, 0, 0, 0])
        return token_array


class TokenArray(models.Model):
    """This class represents a token inventory.
    py:class:: Class documentation ?
    """
    tokensJSON = models.JSONField(blank=True)
    objects = TokenArrayManager()

        
    def set_tokens(self, list: List[int]) -> None:
        self.tokens = json.dumps(list)
        
    def get_tokens(self) -> List[int]:
        return json.loads(self.tokens)

    def withdraw_token(self, color: Color, amount: int) -> None:
        tokens: List[int] = self.get_tokens()
        if tokens[color] > amount:
            tokens[color] -= amount
            self.set_tokens(tokens)
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
        return sum(self.get_tokens())

    def can_pay(self, other: 'TokenArray') -> bool:
        assert other.tokens[-1] == 0
        tokens: List[int] = self.get_tokens()

        # can pay without gold
        comparison = [x >= y for x, y in zip(tokens, other.tokens[:-1])]
        if comparison == [True for x in range(len(comparison))]:
            return True

        # can pay with gold
        gold_needed = -sum([x - y if x - y < 0 else 0 for x, y in zip(tokens, other.tokens[:-1])])
        if gold_needed <= tokens[-1]:
            return True
        return False

    """def __iadd__(self, other):
        tokens: List[int] = self.get_tokens()
        tokens = [x + y for x, y in zip(tokens, other.tokens)]
        self.set_tokens(tokens)
        return self"""

    """def __isub__(self, other):
        assert other.tokens[-1] == 0
        assert self.can_pay(other)

        tokens: List[int] = self.get_tokens()
        tokens = [x - y for x, y in zip(tokens, other.tokens)]
        for i in range(5):
            if self.tokens[i] < 0:
                self.tokens[-1] += self.tokens[i]
                self.tokens[i] = 0
        self.set_tokens(tokens)
        return self"""
