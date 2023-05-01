from dataclasses import dataclass
from typing import List

from model.business_model.card import Card
from model.business_model.token_array import TokenArray
from model.business_model.deck import Deck
from model.business_model.hand import Hand


@dataclass
class Rank():
    """This class represents a rank of cards. It contains the cards of the rank, the level of the rank and the methods to interact with them.

    Attributes:
        level (int): The level of the rank.
        hand (Hand): The hand of the rank.
        deck (Deck): The deck of the rank.
        """
    level: int
    hand: Hand
    deck: Deck

    def __init__(self, cards: List[Card], level: int) -> None:
        """This method initializes the rank. It creates the hand and the deck of the rank.

        Args:
            cards (List[Card]): The cards of the rank.
            level (int): The level of the rank.
            """
        self.level = level
        self.hand = Hand([])
        self.deck = Deck(cards)

        for i in range(4):
            self.hand.add_card(self.deck.draw())

    def get_card_price(self, cardId: int) -> TokenArray or None:
        """This method returns the price of a card with the given id.

        Args:
            cardId (int): The id of the card to check.

        Returns:
            TokenArray or None: The price of the card if the rank has it, None otherwise.
            """

        for card in self.hand.cards:
            if card.card_id == cardId:
                return card.price
        return None

    def withdraw_card(self, cardId: int) -> Card or None:
        """This method withdraws a card with the given id from the rank.

        Args:
            cardId (int): The id of the card to withdraw.

        Returns:
            Card or None: The card if the rank has it, None otherwise.
            """
        if isinstance((card := self.hand.pop_card(cardId)), Card):
            draw_card = self.deck.draw()
            if isinstance(card, Card):
                self.hand.add_card(draw_card)
            return card
        return None

    def can_draw(self) -> bool:
        """This method checks if the rank can draw a card.

        Returns:
            bool: True if the rank can draw a card, False otherwise.
            """

        return self.deck.can_draw()

    def withdraw_pile_card(self) -> Card:
        """This method withdraws a card from the rank's deck.

        Returns:
            Card: The card withdrawn.
            """
        return self.deck.draw()

    def get_number_of_cards_deck(self) -> int:
         return self.hand.get_number_of_cards()