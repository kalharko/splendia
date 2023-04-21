import unittest

from model.patron_controller import PatronController
from model.player_controller import PlayerController


class Test_PatronController(unittest.TestCase):
    def test_adding_patron(self):
        patron_controller = PatronController(1)
        player_controller = PlayerController(1, patron_controller)


if __name__ == '__main__':
    unittest.main()
