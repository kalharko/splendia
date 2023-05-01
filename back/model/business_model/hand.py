from dataclasses import dataclass

from model.business_model.card_stack import CardStack
from model.business_model.token_array import TokenArray
from model.utils.exception import CardIdNotFound
from model.business_model.card import Card
from typing import List


@dataclass
class Hand(CardStack):
    """This class represents the hand of a player. It contains the cards of the hand and the methods to interact with them.

    Attributes:
        cards (List[Card]): The cards of the hand.
        """

    cards: List[Card]

    def get_card_price(self, cardId: int) -> TokenArray or CardIdNotFound:
        """This method returns the price of a card with the given id.

        Args:
            cardId (int): The id of the card to check.

        Returns:
            TokenArray or CardIdNotFound: The price of the card if the hand has it, CardIdNotFound otherwise.
            """

        for card in self.cards:
            if card.card_id == cardId:
                return card.price
        return CardIdNotFound()

    def compute_hand_bonuses(self) -> TokenArray:
        """This method computes the bonuses of the cards in the hand.

        Returns:
            TokenArray: The bonuses of the cards in the hand.
            """
        out = TokenArray()
        for card in self.cards:
            out += card.bonus
        return out

    def compute_victory_points(self) -> int:
        """This method computes the victory points of the cards in the hand.

        Returns:
            int: The victory points of the cards in the hand.
            """
        out = 0
        for card in self.cards:
            out += card.victoryPoint
        return out

    def get_cards(self) -> list: 
        return self.cards
