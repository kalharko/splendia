from dataclasses import dataclass
from typing import List

from model.business_model.rank import Card, Rank
from model.business_model.token_array import TokenArray
from model.utils.parsing import retrieve_and_parse_cards
from model.utils.exception import CardIdNotFound


@dataclass
class ShopController():
    """This class is a controller for the shop. It contains the 3 ranks of cards and the methods to interact with them.

    Attributes:
        ranks (List[Rank]): The 3 ranks of cards.
        """
    ranks: List[Rank]

    def __init__(self):
        """This method initializes the shop controller. It creates the 3 ranks of cards.
        """
        self.ranks: list[Rank] = []
        all_cards: list[Card] = retrieve_and_parse_cards()
        self.ranks.append(Rank([x for x in all_cards if x.card_id < 40], 1))
        self.ranks.append(
            Rank([x for x in all_cards if 40 <= x.card_id < 70], 2))
        self.ranks.append(Rank([x for x in all_cards if 70 <= x.card_id], 3))

    def has_card(self, cardId: int) -> bool:
        """This method checks if the shop has a card with the given id.

        Args:
            cardId (int): The id of the card to check.

        Returns:
            bool: True if the shop has the card, False otherwise.
            """
        for rank in self.ranks:
            if isinstance((price := rank.get_card_price(cardId)), TokenArray):
                return True
        return False

    def get_card_price(self, cardId: int) -> Card or None:
        """This method returns the price of a card with the given id.

        Args:
            cardId (int): The id of the card to check.

        Returns:
            Card or None: The price of the card if the shop has it, None otherwise.
            """

        for rank in self.ranks:
            if isinstance((price := rank.get_card_price(cardId)), TokenArray):
                return price
        return None

    def withdraw_card(self, cardId: int) -> Card or CardIdNotFound:
        """This method withdraws a card with the given id from the shop.

        Args:
            cardId (int): The id of the card to withdraw.

        Returns:
            Card or CardIdNotFound: The card if the shop has it, CardIdNotFound otherwise.
            """

        for rank in self.ranks:
            if isinstance((card := rank.withdraw_card(cardId)), Card):
                return card
        return CardIdNotFound()

    def can_withdraw_pile_card(self, pileLevel: int) -> bool:
        """This method checks if a card can be withdrawn from a pile.

        Args:
            pileLevel (int): The level of the pile to check.

        Returns:
            bool: True if a card can be withdrawn from the pile, False otherwise.

            """
        assert isinstance(pileLevel, int)
        assert 0 <= pileLevel <= 3
        return self.ranks[pileLevel].can_draw()

    def withdraw_pile_card(self, pileLevel: int) -> Card:
        """This method withdraws a card from a pile.

        Args:
            pileLevel (int): The level of the pile to check.

        Returns:
            Card: The card withdrawn from the pile.
            """
        assert isinstance(pileLevel, int)
        assert 0 <= pileLevel <= 3
        return self.ranks[pileLevel].withdraw_pile_card()
    
    def gather_shop_information_api_board_state(self) -> list:
        info = []
        for i in range(len(self.ranks)):
            info.append({
                'rank': {
                    'numberCardsDeck': self.ranks[i].get_number_of_cards_deck(),
                    'visibleCards': self.ranks[i].get_cards_hand()
                }
            })
        
        return info
