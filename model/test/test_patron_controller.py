import unittest

from model.business_model.patron_controller import PatronController
from model.business_model.player_controller import PlayerController


class Test_PatronController(unittest.TestCase):
    def test_adding_patron(self):
        patron_controller = PatronController()
        patron_controller.load(4)
        player_controller = PlayerController()
        player_controller.load(4, patron_controller)


if __name__ == '__main__':
    unittest.main()
