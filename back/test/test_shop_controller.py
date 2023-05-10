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
        self.assertEqual(sc.ranks[0].hand.get_size(), 4)
        self.assertEqual(sc.ranks[0].deck.get_size(), 36)

        self.assertEqual(sc.ranks[1].level, 2)
        self.assertEqual(sc.ranks[1].hand.get_size(), 4)
        self.assertEqual(sc.ranks[1].deck.get_size(), 26)

        self.assertEqual(sc.ranks[2].level, 3)
        self.assertEqual(sc.ranks[2].hand.get_size(), 4)
        self.assertEqual(sc.ranks[2].deck.get_size(), 16)

    def test_card_price(self):
        sc = ShopController()

        for i in range(3):
            cardId = sc.ranks[i].hand.cards[i].cardId
            cardPrice = sc.ranks[i].hand.cards[i].price
            self.assertEqual(sc.get_card_price(cardId), cardPrice)

    def test_withdraw(self):
        sc = ShopController()

        for i in range(3):
            card = sc.ranks[i].hand.cards[i]
            self.assertEqual(sc.withdraw_card(card.cardId), card)


if __name__ == '__main__':
    unittest.main()
