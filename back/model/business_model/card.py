from dataclasses import dataclass

from back.model.business_model.token_array import TokenArray
from back.model.business_model.victory_point import VictoryPoint


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
