from dataclasses import dataclass
from typing import List
from model.card import Card
from model.utils.exception import CardIdNotFound


@dataclass
class CardStack():
    cards: List[Card]

    def add_card(self, card: Card) -> None:
        #assert isinstance(card, Card)
        if isinstance(card, Card):

            self.cards.append(card)

    def pop_card(self, cardId: int) -> Card:
        assert isinstance(cardId, int)
        assert 0 <= cardId < 90

        for i in range(len(self.cards)):
            if self.cards[i].card_id == cardId:
                return self.cards.pop(i)
        return CardIdNotFound

    def get_size(self): #deprecated
        return len(self.cards)

    def __len__(self):
        return len(self.cards)
