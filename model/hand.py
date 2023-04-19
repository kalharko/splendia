from dataclasses import dataclass

from model.card_stack import CardStack
from model.token_array import TokenArray
from model.utils.exception import CardIdNotFound
from model.card import Card
from typing import List


@dataclass
class Hand(CardStack):
    cards: List[Card]

    def get_card_price(self, cardId: int) -> TokenArray:
        for card in self.cards:
            if card.card_id == cardId:
                return card.price
        return CardIdNotFound()

    def compute_hand_bonuses(self) -> TokenArray:
        out = TokenArray()
        for card in self.cards:
            out += card.bonus
        return out

    def compute_victory_points(self) -> int:
        out = 0
        for card in self.cards:
            out += card.victoryPoint
        return out
