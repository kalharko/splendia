from typing import List
import random
from api.models import Hand
from api.models import Patron
from api.models import VictoryPoint
from api.models import TokenArray
from api.models.utils.singleton_model import SingletonModel
import pandas as pd
from django.db import models

class GameManagerManager(models.Manager):
    def create_patron_controller(self, nbPlayer: int):
        patron_controller = self.create()
        patrons = patron_controller.initialize_patrons()
        patron_controller.index_patrons = [i for i in range(len(patrons))]
        random.shuffle(index_patrons)
        self.patrons = [patrons[i] for i in index_patrons[:nbPlayer + 1]]

class PatronController(SingletonModel):
    patrons: List[Patron] = models.ManyToManyField(Patron, blank=True)

    def __init__(self, nbPlayer: int) -> None:
        patrons = self.initialize_patrons()
        index_patrons = [i for i in range(len(patrons))]
        random.shuffle(index_patrons)
        self.patrons = [patrons[i] for i in index_patrons[:nbPlayer + 1]]

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

    def initialize_patrons(self) -> List[Patron]:
        noble_df = pd.read_csv('model/data/patrons.csv')

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
