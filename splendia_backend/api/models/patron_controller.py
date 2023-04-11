from typing import List
import random
from api.models import Hand
from api.models import Patron
from api.models import VictoryPoint
from api.models import TokenArray
from api.models.utils.singleton_model import SingletonModel
import pandas as pd
from django.db import models



class PatronController(SingletonModel):
    patrons: List[Patron] = models.ManyToManyField(Patron)

    def reset_data(self, nbPlayer: int) -> None:
        patrons = self.initialize_patrons()
        index_patrons = [i for i in range(len(patrons))]
        random.shuffle(index_patrons)
        self.patrons.set([patrons[i] for i in index_patrons[:nbPlayer + 1]])
        self.save()

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
        noble_df = pd.read_csv('splendia_backend/static/csv/patrons.csv')
        
        patron_list: List[Patron] = []
        for row in noble_df.itertuples():
            #print(row)
            white = row[1]
            blue = row[2]
            green = row[3]
            red = row[4]
            black = row[5]
            gold = 0
            victory_point = VictoryPoint.objects.create(value=3)
            token_array = TokenArray.objects.create_token_array([white, blue, green, red, black, gold])
            # patron_list.a(Patron(token_array, victory_point))
            patron_list.append(Patron.objects.create(requirements = token_array, victoryPoints=victory_point))
        
            
        return patron_list
