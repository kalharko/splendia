from typing import List
from random import randrange

from api.models import CardStack
from api.models import Card


class Deck(CardStack):

    def __init__(self, cards: List[Card]):
        self.cards = cards

    def draw(self) -> Card:
        return self.cards.pop(randrange(0, len(self.cards)))
