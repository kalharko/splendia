from dataclasses import dataclass
from typing import List
from random import randrange

from model.card_stack import CardStack
from model.card import Card
from model.utils.exception import EmptyDeck


@dataclass
class Deck(CardStack):

    def __init__(self, cards: List[Card]):
        self.cards = cards

    def can_draw(self) -> bool:
        return len(self.cards) > 0

    def draw(self) -> Card:
        if len(self.cards) == 0:
            return EmptyDeck()
        return self.cards.pop(randrange(0, len(self.cards)))
