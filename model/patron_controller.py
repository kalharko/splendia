from dataclasses import dataclass
from typing import List
import random

from model.rank import Hand
from model.patron import Patron
from model.victory_point import VictoryPoint
from model.token_array import TokenArray
from model.utils.singleton import SingletonMeta
import pandas as pd
from model.utils.parsing import retrieve_and_parse_patrons

@dataclass
class PatronController(metaclass=SingletonMeta):
    patrons: List[Patron]

    def __init__(self, nbPlayer: int) -> None:
        patrons = retrieve_and_parse_patrons()
        random.shuffle(patrons)
        self.patrons = patrons[:nbPlayer + 1]

    def update(self, hand: Hand) -> Patron:
        return self.withdraw(hand)

    def withdraw(self, hand: Hand) -> Patron:
        token_player = hand.compute_hand_bonuses()
        for patron in self.patrons:
            if token_player.can_buy(patron.requirements):
                patron_temp = patron
                self.patrons.remove(patron)
                return patron_temp
        return None
