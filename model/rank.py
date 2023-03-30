from dataclasses import dataclass
from typing import List

from model.card import Card
from model.token_array import TokenArray
from model.deck import Deck
from model.hand import Hand


@dataclass
class Rank():
    level: int
    hand: Hand
    deck: Deck

    def __init__(self, cards: List[Card], level: int) -> None:
        self.level = level
        self.hand = Hand([])
        self.deck = Deck(cards)

        for i in range(3):
            self.hand.add_card(self.deck.draw())

    def get_card_price(self, cardId: int) -> TokenArray:
        for card in self.hand.cards:
            if card.id == cardId:
                return card.price
        return None

    def withdraw_card(self, cardId: int) -> Card:
        if isinstance((card := self.hand.pop_card(cardId)), Card):
            self.hand.add_card(self.deck.draw())
            return card
        return None
