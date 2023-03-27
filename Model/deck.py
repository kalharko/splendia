from dataclasses import dataclass
from card_stack import CardStack
from Model.card import Card
import random
@dataclass
class Deck(CardStack):

    def draw(self) -> Card:
        return self.cards.pop(random.range(0, len(self.cards)))
