from dataclasses import dataclass
from typing import List
from model.card import Card


@dataclass
class CardStack():
    cards: List[Card]

    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    def pop_card(self, cardId: int) -> Card:
        for i in range(len(self.cards)):
            if self.cards[i].card_id == cardId:
                return self.cards.pop(i)
        return None

    def get_size(self):
        return len(self.cards)
