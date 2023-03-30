from dataclasses import dataclass
from typing import List
from random import randrange

from model.card_stack import CardStack
from model.card import Card


@dataclass
class Deck(CardStack):

    def __init__(self, cards: List[Card]):
        self.cards = cards

    def draw(self) -> Card:
        return self.cards.pop(randrange(0, len(self.cards)))
