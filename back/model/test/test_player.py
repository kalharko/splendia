import unittest
from typing import List

from model.business_model.player import Player
from model.business_model.patron_controller import PatronController
from model.business_model.hand import Hand
from model.business_model.token_array import TokenArray
from model.business_model.victory_point import VictoryPoint


class Test_PlayerController(unittest.TestCase):
    def test_initialization(self):
        patronController = PatronController()
        patronController.load(4)
        player = Player(player_id, observer)
        self.assertIsInstance(player.player_id, int)
        self.assertIsInstance(player.hand, Hand)
        self.assertIsInstance(player.reserved, Hand)
        self.assertIsInstance(player.tokens, TokenArray)
        self.assertIsInstance(player.victoryPoints, VictoryPoint)
        self.assertIsInstance(player.patrons, List[Patron])
        self.assertIsInstance(player.observer, PatronController)

    def test_get_card_price(self):
        pass  # TODO: write test

    def test_pay(self):
        pass  # TODO: write test

    def test_withdraw_reserved_card(self):
        pass  # TODO: write test

    def test_deposit_card(self):
        pass  # TODO: write test

    def test_notify_observer(self):
        pass  # TODO: write test

    def test_deposit_reserved_card(self):
        pass  # TODO: write test

    def test_deposit_tokens(self):
        pass  # TODO: write test

    def test_nb_reserved_cards(self):
        pass  # TODO: write test

    def test_update_victory_points(self):
        pass  # TODO: write test


if __name__ == '__main__':
    unittest.main()
