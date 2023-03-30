from dataclasses import dataclass
from typing import List

from model.rank import Hand
from model.patron import Patron
from model.utils.singleton import SingletonMeta


@dataclass
class PatronController(metaclass=SingletonMeta):
    patrons: List[Patron]

    def __init__(self, nbPlayer: int) -> None:
        pass

    def withdraw(self, hand: Hand) -> Patron:
        pass
