from dataclasses import dataclass
from Model.TokenArray import TokenArray
from Model.VictoryPoint import VictoryPoint


@dataclass
class Patron():
    requirements: TokenArray()
    victoryPoints: VictoryPoint
