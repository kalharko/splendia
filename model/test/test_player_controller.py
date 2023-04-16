import unittest

from model.player_controller import PlayerController
from model.player import Player
from model.patron_controller import PatronController
from model.shop_controller import ShopController
from model.token_array import TokenArray, Color
from model.bank_controller import BankController


class Test_PlayerController(unittest.TestCase):
    def test_initialization(self):
        patronController = PatronController(4)
        pc = PlayerController(4, patronController)
        pc.__init__(4, patronController)
        self.assertEqual(len(pc.players), 4)
        self.assertIsInstance(pc.players[0], Player)

    def test_buy_reserved_card(self):
        patronController = PatronController(4)
        shopController = ShopController()
        pc = PlayerController(4, patronController)
        pc.__init__(4, patronController)
        cardId = shopController.ranks[0].hand.cards[0].card_id
        pc.reserve_card(0, cardId)
        pc.buy_reserved_card(0, cardId)
        self.assertEqual(len(pc.players[0].reserved), 0)
        self.assertEqual(pc.players[0].hand.cards[0].card_id, cardId)


    def test_buy_shop_card(self):
        patronController = PatronController(4)
        patronController.__init__(4)
        shopController = ShopController()
        shopController.__init__()
        pc = PlayerController(4, patronController)
        pc.__init__(4, patronController)
        cardId = shopController.ranks[0].hand.cards[0].card_id
        price = shopController.ranks[0].hand.cards[0].price
        pc.players[0].tokens = TokenArray([7, 7, 7, 7, 7, 5])
        pc.buy_shop_card(0, cardId)
        self.assertEqual(pc.players[0].tokens.get_tokens(), (TokenArray([7, 7, 7, 7, 7, 5]) - price).get_tokens())
        self.assertEqual(pc.players[0].hand.cards[0].card_id, cardId)

    def test_reserve_card(self):
        patronController = PatronController(4)
        shopController = ShopController()
        pc = PlayerController(4, patronController)
        pc.__init__(4, patronController)
        cardId = shopController.ranks[0].hand.cards[0].card_id
        pc.reserve_card(0, cardId)
        self.assertEqual(pc.players[0].tokens.get_tokens()[Color.GOLD.value], 1)
        self.assertEqual(pc.players[0].reserved[0].card_id, cardId)

    def test_take_tokens(self):
        patronController = PatronController(4)
        pc = PlayerController(4, patronController)
        pc.__init__(4, patronController)
        bankController = BankController(nbPlayer=4)
        if err := pc.take_tokens(0, TokenArray([1, 1, 1, 0, 0, 0])):
            print(err)
        self.assertEqual(pc.players[0].tokens.get_tokens(), [1, 1, 1, 0, 0, 0])
        pc.take_tokens(0, TokenArray([0, 0, 0, 2, 0, 0]))
        self.assertEqual(pc.players[0].tokens.get_tokens(), [1, 1, 1, 2, 0, 0])



if __name__ == '__main__':
    unittest.main()
