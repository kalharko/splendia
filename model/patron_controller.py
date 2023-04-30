from dataclasses import dataclass
from typing import List
import random

from model.rank import Hand
from model.patron import Patron
from model.utils.parsing import retrieve_and_parse_patrons


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

        token_player = hand.compute_hand_bonuses()
        for patron in self.patrons:
            if token_player.can_pay(patron.requirements):
                patron_temp = patron
                self.patrons.remove(patron)
                return patron_temp
        return None
