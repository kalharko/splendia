from dataclasses import dataclass
from typing import List

from model.rank import Card, Rank


@dataclass
class ShopController():
    ranks: List[Rank]

    def __init__(self) -> None:
        with open("Model/data/cards.csv", 'r') as file:
            file = file.readlines()
        self.ranks[0].load(file[3:43])
        self.ranks[1].load(file[43:73])
        self.ranks[2].load(file[73:-1])

    def get_card_price(self, cardId: int) -> Card:
        pass

    def withdraw_card(self, cardId: int) -> Card:
        pass
