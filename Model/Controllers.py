from dataclasses import dataclass
from typing import List

from Model.Cards import Rank
from Model.Bank import Bank
from Model.Patron import Patron
from Model.Player import Player


@dataclass
class BankController():
    bank: Bank


@dataclass
class PatronController():
    patrons: List[Patron]


@dataclass
class PlayerController():
    players: List[Player]


@dataclass
class ShopController():
    ranks: List[Rank]
