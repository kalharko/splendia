from dataclasses import dataclass

from model.card_stack import CardStack
from model.token_array import TokenArray


@dataclass
class Hand(CardStack):

    def get_card_price(self, cardId: int) -> TokenArray:
        for card in self.cards:
            if card.id == cardId:
                return card.id
        return None

    def compute_hand_bonuses(self) -> TokenArray:
        out = TokenArray()
        for card in self.cards:
            out += card.bonus
        return out

