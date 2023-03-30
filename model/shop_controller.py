from dataclasses import dataclass
from typing import List

from model.rank import Card, Rank
from model.token_array import TokenArray
from model.utils.parsing import retrieve_and_parse_cards
from model.utils.singleton import SingletonMeta


@dataclass
class ShopController(metaclass=SingletonMeta):
    ranks: List[Rank]

    def __init__(self) -> None:
        self.ranks = []
        all_cards = retrieve_and_parse_cards()
        self.ranks.append(Rank([x for x in all_cards if x.card_id < 40], 1))
        self.ranks.append(Rank([x for x in all_cards if 40 <= x.card_id < 70], 1))
        self.ranks.append(Rank([x for x in all_cards if 70 <= x.card_id], 1))

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
