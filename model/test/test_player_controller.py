import unittest

from model.player_controller import PlayerController


class Test_PlayerController(unittest.TestCase):
    def test_initialisation(self):
        pc = PlayerController(4)
        pc.__init__(4, [])
        self.assertEqual(len(pc.players), 4)

    def test_buy_reserved_card(self):
        pc = PlayerController(4)
        pass


if __name__ == '__main__':
    unittest.main()
