from typing import List

from api.models import Card, Rank
from api.models import TokenArray
from .utils.parsing import retrieve_and_parse_cards
from api.models.utils.singleton_model import SingletonModel
from django.db import models


class ShopController(SingletonModel):
    ranks: List[Rank] = models.ManyToManyField(Rank, blank=True)

    def __init__(self) -> None:
        self.ranks = []
        all_cards = retrieve_and_parse_cards()
        self.ranks.append(Rank([x for x in all_cards if x.card_id < 40], 1))
        self.ranks.append(Rank([x for x in all_cards if 40 <= x.card_id < 70], 2))
        self.ranks.append(Rank([x for x in all_cards if 70 <= x.card_id], 3))

    def get_card_price(self, cardId: int) -> Card:
        for rank in self.ranks:
            if isinstance((price := rank.get_card_price(cardId)), TokenArray):
                return price
        return None

    def withdraw_card(self, cardId: int) -> Card:
        for rank in self.ranks:
            if isinstance((card := rank.withdraw_card(cardId)), Card):
                return card
        return None
