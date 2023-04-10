from typing import List

from api.models import Card
from api.models import TokenArray
from api.models import Deck
from api.models import Hand
from django.db import models


class Rank(models.Model):
    level: int = models.IntegerField(blank=True)
    hand: Hand = models.OneToOneField(Hand, on_delete=models.CASCADE, blank=True)
    deck: Deck = models.OneToOneField(Deck, on_delete=models.CASCADE, blank=True)

    def __init__(self, cards: List[Card], level: int) -> None:
        self.level = level
        self.hand = Hand([])
        self.deck = Deck(cards)

        for i in range(4):
            self.hand.add_card(self.deck.draw())

    def get_card_price(self, cardId: int) -> TokenArray:
        for card in self.hand.cards:
            if card.card_id == cardId:
                return card.price
        return None

    def withdraw_card(self, cardId: int) -> Card:
        if isinstance((card := self.hand.pop_card(cardId)), Card):
            self.hand.add_card(self.deck.draw())
            return card
        return None
