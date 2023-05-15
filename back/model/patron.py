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
    requirements: TokenArray
    victoryPoints: VictoryPoint

    def gather_patron_information_api_board_state(self) -> dict:
        """Gather the patron information needed for the api board state in a dictionnary.
        The dictionnary contains:
        - the id of the patron
        - the requirements of the patron
        - the victory points of the patron

        Returns:
            dict: shop information for the api board state
        """

        return {
            "patronId": self.patron_id,
            "requirements": self.requirements.get_tokens(),
            "victoryPoints": self.victoryPoints.get_value()
        }
