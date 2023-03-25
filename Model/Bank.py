from dataclasses import dataclass
from typing import List



@dataclass
class TokenArray():
    tokens: List[int]




@dataclass
class Bank():
    tokens: TokenArray
