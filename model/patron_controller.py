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

        patron_list: List[Patron] = []
        for row in noble_df.itertuples():
            #print(row)
            white = row[1]
            blue = row[2]
            green = row[3]
            red = row[4]
            black = row[5]
            gold = 0
            victory_point = VictoryPoint(3)
            token_array = TokenArray([white, blue, green, red, black, gold])
            patron_list.append(Patron(token_array, victory_point))
        return patron_list