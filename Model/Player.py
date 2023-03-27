from dataclasses import dataclass
from typing import List

from Model.token_array import TokenArray
from Model.rank import Hand
from Model.Patron import Patron
from Model.victory_point import VictoryPoint


@dataclass
class Player():
    hand: Hand
    reserved: Hand
    tokens: TokenArray
    victoryPoints: VictoryPoint
    patrons: List[Patron]
