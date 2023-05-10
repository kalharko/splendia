from dataclasses import dataclass
from typing import List
from model.card import Card
from utils.exception import CardIdNotFound


@dataclass
class CardStack():
    """This class represents a stack of cards. It contains the cards of the stack and the methods to interact with them.

    Attributes:
        cards (List[Card]): The cards of the stack.
        """

    cards: List[Card]

    def add_card(self, card: Card) -> None:
        assert isinstance(card, Card)
        if isinstance(card, Card):

            self.cards.append(card)

    def pop_card(self, cardId: int) -> Card or CardIdNotFound:
        """This method pops a card from the stack.

        Args:
            cardId (int): The id of the card to pop.

        Returns:
            Card or CardIdNotFound: The card popped from the stack, CardIdNotFound if the card is not in the stack.

            """
        assert isinstance(cardId, int)
        assert 0 <= cardId < 90

        for i in range(len(self.cards)):
            if self.cards[i].cardId == cardId:
                return self.cards.pop(i)
        return CardIdNotFound(cardId)

    def get_size(self):  # deprecated
        return len(self.cards)

    def __len__(self):
        return len(self.cards)
