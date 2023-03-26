from dataclasses import dataclass
from typing import List

from Model.TokenArray import TokenArray
from Model.Cards import Hand
from Model.Patron import Patron
from Model.VictoryPoint import VictoryPoint


@dataclass
class Player():
    hand: Hand
    reserved: Hand
    tokens: TokenArray
    victoryPoints: VictoryPoint
    patrons: List[Patron]
