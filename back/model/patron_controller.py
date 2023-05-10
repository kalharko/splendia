from dataclasses import dataclass
from typing import List
import random

from model.rank import Hand
from model.patron import Patron
from utils.parsing import retrieve_and_parse_patrons


@dataclass
class PatronController():
    """This class is a controller for the patrons. It contains the patrons and the methods to interact with them.

    Attributes:
        patrons (List[Patron]): The patrons of the game.

        """

    patrons: List[Patron]

    def __init__(self, nbPlayer: int):
        """This method initializes the patron controller. It creates the patrons.

        Args:
            nbPlayer (int): The number of players.

            """
        assert isinstance(nbPlayer, int)

        patrons = retrieve_and_parse_patrons()
        random.shuffle(patrons)
        self.patrons = patrons[:nbPlayer + 1]

    def update(self, hand: Hand) -> Patron:
        """This method updates the patrons. It withdraws a patron if the player can pay it.

        Args:
            hand (Hand): The hand of the player.

        Returns:
            Patron: The patron withdrawn.
                """
        assert isinstance(hand, Hand)

        return self.withdraw(hand)

    def withdraw(self, hand: Hand) -> Patron or None:
        """This method withdraws a patron if the player can pay it.

        Args:
            hand (Hand): The hand of the player.

        Returns:
            Patron: The patron withdrawn.

            """
        assert isinstance(hand, Hand)

        token_player = hand.compute_hand_bonuses()
        for patron in self.patrons:
            if token_player.can_pay(patron.requirements):
                patron_temp = patron
                self.patrons.remove(patron)
                return patron_temp
        return None

    def gather_patrons_information_api_board_state(self) -> list:
        """Gather the information of the CPU players needed for the api board state in a list

        Returns:
            list: contains information of patron for the api board state
        """

        return [patron.gather_patron_information_api_board_state() for patron in self.patrons]
