from dataclasses import dataclass
from model.token_array import TokenArray
from model.victory_point import VictoryPoint


@dataclass
class Patron():
    """This class is used to manage the patrons of the game.

    Attributes:
        patron_id (int): The id of the patron.
        requirements (TokenArray): The requirements of the patron.
        victoryPoints (VictoryPoint): The victory points of the patron.
        """

    patron_id: int
    requirements: TokenArray()
    victoryPoints: VictoryPoint
