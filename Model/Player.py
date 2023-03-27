from dataclasses import dataclass
from typing import List

from model.token_array import TokenArray
from model.rank import Hand
from model.patron import Patron
from model.victory_point import VictoryPoint


@dataclass
class Player():
    hand: Hand
    reserved: Hand
    tokens: TokenArray
    victoryPoints: VictoryPoint
    patrons: List[Patron]
