import unittest

from model.shop_controller import ShopController
from model.rank import Rank
from model.hand import Hand
from model.deck import Deck


class Test_ShopController(unittest.TestCase):
    def test_initialisation(self):
        sc = ShopController()
        self.assertEqual(sc.ranks[0].level, 1)
        self.assertIsInstance(sc.ranks[0], Rank)
        self.assertIsInstance(sc.ranks[0].deck, Deck)
        self.assertIsInstance(sc.ranks[0].hand, Hand)
        self.assertIsInstance(sc.ranks[0].level, int)
        self.assertEqual(sc.ranks[0].hand.get_size, 4)
        self.assertEqual(sc.ranks[0].deck.get_size, 36)

        self.assertEqual(sc.ranks[0].level, 2)
        self.assertEqual(sc.ranks[1].hand.get_size(), 4)
        self.assertEqual(sc.ranks[1].deck.get_size(), 26)

        self.assertEqual(sc.ranks[0].level, 3)
        self.assertEqual(sc.ranks[2].hand.get_size(), 4)
        self.assertEqual(sc.ranks[2].deck.get_size(), 16)

    def test_card_price(self):
        pass

    def test_withdraw(self):
        pass


if __name__ == '__main__':
    unittest.main()
