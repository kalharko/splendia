from dataclasses import dataclass

from model.token_array import TokenArray
from model.victory_point import VictoryPoint


@dataclass
class Card():
    """This class is used to manage the cards of the game.

    Attributes:
        card_id (int): The id of the card.
        price (TokenArray): The price of the card.
        bonus (TokenArray): The bonus of the card.
        victoryPoint (VictoryPoint): The victory points of the card.
        """

    card_id: int
    price: TokenArray
    bonus: TokenArray
    victoryPoint: VictoryPoint

    def __init__(self, price: TokenArray, bonus: TokenArray,
                 victoryPoint: VictoryPoint, card_id: int) -> None:
        """The constructor of the class.

        Args:
            price (TokenArray): The price of the card.
            bonus (TokenArray): The bonus of the card.
            victoryPoint (VictoryPoint): The victory points of the card.
            card_id (int): The id of the card.

            """
        self.price = price
        self.bonus = bonus
        self.victoryPoint = victoryPoint
        self.card_id = card_id

    def gather_card_information_api_board_state(self) -> dict:
        """Gather the card information needed for the api board state in a dictionnary.
        The dictionnary contains!
        - the id of the card
        - the price of the card
        - the bonus of the card
        - the victory points of the card 

        Returns:
            dict: _description_
        """
        return {
            "card_id": self.card_id,
            "price": self.price.get_tokens(),
            "bonus": self.bonus.get_tokens(),
            "victoryPoint": self.victoryPoint.get_value()
        }