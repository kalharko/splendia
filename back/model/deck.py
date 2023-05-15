from dataclasses import dataclass
from typing import List
from random import randrange

from model.card_stack import CardStack
from model.card import Card
from utils.exception import EmptyDeck


@dataclass
class Deck(CardStack):
    """This class represents a deck of cards. It contains the cards of the deck and the methods to interact with them.

    Attributes:
        cards (List[Card]): The cards of the deck.
        """

    def __init__(self, cards: list[Card]):
        """This method initializes the deck.

        Args:
            cards (List[Card]): The cards of the deck.
            """
        assert isinstance(cards, list)

        self.cards = cards

    def can_draw(self) -> bool:
        """This method checks if the deck can be drawn.

        Returns:
            bool: True if the deck can be drawn, False otherwise.
            """
        return len(self.cards) > 0

    def draw(self) -> Card or EmptyDeck:
        """This method draws a card from the deck.

        Returns:
            Card or EmptyDeck: The card drawn from the deck, EmptyDeck if the deck is empty.
            """

        if len(self.cards) == 0:
            return EmptyDeck()
        return self.cards.pop(randrange(0, len(self.cards)))

    def get_number_of_cards(self) -> int:
        """Get the number of cards contained in the deck

        Returns:
            int: the number of cards of the deck
            """

        return len(self.cards)
