from dataclasses import dataclass
from typing import List
from model.card import Card
from django.db import models


@dataclass
class CardStack(models.Model):
    cards: List[Card] = models.ForeignKey(Card, on_delete=models.CASCADE)

    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    def pop_card(self, cardId: int) -> Card:
        for i in range(len(self.cards)):
            if self.cards[i].card_id == cardId:
                return self.cards.pop(i)
        return None

    def get_size(self):
        return len(self.cards)
