from dataclasses import dataclass
from random import randrange

from model.card_stack import CardStack
from model.card import Card


@dataclass
class Deck(CardStack):

    def draw(self) -> Card:
        return self.cards.pop(randrange(0, len(self.cards)))
