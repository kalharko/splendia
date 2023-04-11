from typing import List
from api.models import Card
from django.db import models


class CardStack(models.Model):
    cards: List[Card] = models.ManyToManyField(Card)

    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    def pop_card(self, cardId: int) -> Card:
        for i in range(len(self.cards)):
            if self.cards[i].card_id == cardId:
                return self.cards.pop(i)
        return None

    def get_size(self):
        return len(self.cards)
