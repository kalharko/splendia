from dataclasses import dataclass
from typing import List

from model.rank import Card, Rank
from model.utils import retrieve_and_parse_cards


@dataclass
class ShopController():
    ranks: List[Rank]

    def __init__(self) -> None:
        all_cards = retrieve_and_parse_cards()
        self.ranks.append(Rank([x for x in all_cards if x.id <40]))
        self.ranks.append(Rank([x for x in all_cards if 40 <= x.id <70]))
        self.ranks.append(Rank([x for x in all_cards if 70 <= x.id]))

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
