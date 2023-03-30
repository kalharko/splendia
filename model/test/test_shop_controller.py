import unittest

from model.shop_controller import ShopController
from model.rank import Rank
from model.hand import Hand
from model.deck import Deck

class Test_ShopController(unittest.TestCase):
    def test_initialization(self):
        sc = ShopController()
        self.assertEqual(len(sc.ranks), 3)
        for i, o in enumerate([40, 30, 20]):
            self.assertIsInstance(sc.ranks[i], Rank)
            self.assertIsInstance(sc.ranks[i].hand, Hand)
            self.assertIsInstance(sc.ranks[i].deck, Deck)
            self.assertEqual(len(sc.ranks[i].hand.cards), 3)
            self.assertEqual(len(sc.ranks[i].deck.cards), o-3)


if __name__ == '__main__':
    unittest.main()
