from dataclasses import dataclass
from Model.token_array import TokenArray
from Model.victory_point import VictoryPoint


@dataclass
class Patron():
    requirements: TokenArray()
    victoryPoints: VictoryPoint
