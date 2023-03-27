from dataclasses import dataclass
from typing import List
from Model.card import Card

@dataclass
class CardStack():
    cards: List[Card]

    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    def pop_card(self, cardId: int) -> Card:
        pass