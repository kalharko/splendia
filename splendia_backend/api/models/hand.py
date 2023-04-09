from dataclasses import dataclass

from api.models import CardStack
from api.models import TokenArray
from models.utils.exception import CardIdNotFound
from api.models import Card
from typing import List


@dataclass
class Hand(CardStack):

    def get_card_price(self, cardId: int) -> TokenArray:
        for card in self.cards:
            if card.id == cardId:
                return card.id
        return CardIdNotFound()

    def compute_hand_bonuses(self) -> TokenArray:
        out = TokenArray()
        for card in self.cards:
            out += card.bonus
        return out
