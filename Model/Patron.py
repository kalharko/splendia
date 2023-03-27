from dataclasses import dataclass
from model.token_array import TokenArray
from model.victory_point import VictoryPoint


@dataclass
class Patron():
    requirements: TokenArray()
    victoryPoints: VictoryPoint
