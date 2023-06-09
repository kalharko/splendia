from dataclasses import dataclass

from model.token_array import TokenArray
from model.victory_point import VictoryPoint


@dataclass
class Card():
    """This class is used to manage the cards of the game.

    Attributes:
        cardId (int): The id of the card.
        price (TokenArray): The price of the card.
        bonus (TokenArray): The bonus of the card.
        victoryPoint (VictoryPoint): The victory points of the card.
        """

    cardId: int
    price: TokenArray
    bonus: TokenArray
    victoryPoint: VictoryPoint

    def __init__(self, price: TokenArray, bonus: TokenArray,
                 victoryPoint: VictoryPoint, cardId: int) -> None:
        """The constructor of the class.

        Args:
            price (TokenArray): The price of the card.
            bonus (TokenArray): The bonus of the card.
            victoryPoint (VictoryPoint): The victory points of the card.
            cardId (int): The id of the card.

            """
        assert isinstance(price, TokenArray)
        assert isinstance(bonus, TokenArray)
        assert isinstance(victoryPoint, VictoryPoint)
        assert isinstance(cardId, int)

        self.price = price
        self.bonus = bonus
        self.victoryPoint = victoryPoint
        self.cardId = cardId

    def gather_card_information_api_board_state(self, player) -> dict:
        """Gather the card information needed for the api board state in a dictionnary.
        The dictionnary contains!
        - the id of the card
        - the price of the card
        - the bonus of the card
        - the victory points of the card

        Returns:
            dict: _description_
        """
        canPay, reducedPrice = player.can_pay_with_reduced_price(self.price)
        if canPay:
            print(self.cardId)
        return {
            "cardId": self.cardId,
            "buyable": canPay
        }
