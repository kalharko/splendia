from dataclasses import dataclass
from typing import List

from model.rank import Card, Rank
from model.utils import retrieve_and_parse_cards


@dataclass
class ShopController():
    ranks: List[Rank]

    def __init__(self) -> None:
        self.ranks = []
        all_cards = retrieve_and_parse_cards()
        self.ranks.append(Rank([x for x in all_cards if x.card_id <40], 1))
        self.ranks.append(Rank([x for x in all_cards if 40 <= x.card_id <70], 1))
        self.ranks.append(Rank([x for x in all_cards if 70 <= x.card_id], 1))

    def get_card_price(self, cardId: int) -> Card:
        for rank in self.ranks:
            if type(price:=rank.get_card_price(cardId)) == type(TokenArray()):
                return price
        return None

    def withdraw_card(self, cardId: int) -> Card:
        for rank in self.ranks:
            if type(card:=rank.withdraw_card(cardId)) == type(Card()):
                return card
        return None
