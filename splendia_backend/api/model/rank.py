from dataclasses import dataclass
from typing import List

from model.card import Card
from model.token_array import TokenArray
from model.deck import Deck
from model.hand import Hand
from django.db import models


@dataclass
class Rank(models.Model):
    level: int = models.IntegerField()
    hand: Hand = models.OneToOneField(Hand, on_delete=models.CASCADE)
    deck: Deck = models.OneToOneField(Deck, on_delete=models.CASCADE)

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
