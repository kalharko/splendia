import unittest

from model.player_controller import PlayerController
from model.patron_controller import PatronController
from model.bank_controller import BankController
from model.shop_controller import ShopController
from model.token_array import TokenArray, Color
from model.utils.logger import Logger
from model.player import Player


class Test_PlayerController(unittest.TestCase):
    def test_initialization(self):
        patronController = PatronController()
        patronController.load(4)
        pc = PlayerController()
        pc.load(4, patronController)
        self.assertEqual(len(pc.players), 4)
        self.assertIsInstance(pc.players[0], Player)

    def test_buy_reserved_card(self):
        patronController = PatronController()
        patronController.load(4)
        shopController = ShopController()
        shopController.load()
        pc = PlayerController()
        pc.load(4, patronController)
        cardId = shopController.ranks[0].hand.cards[0].card_id
        price = shopController.get_card_price(cardId)
        pc.reserve_card(0, cardId)
        pc.cheat_take_tokens(0, price)
        if err := pc.buy_reserved_card(0, cardId):
            Logger().log(0, err, 'test_buy_reserved_card')
        self.assertEqual(len(pc.players[0].reserved), 0)
        self.assertEqual(pc.players[0].hand.cards[0].card_id, cardId)

    def test_buy_shop_card(self):
        patronController = PatronController()
        patronController.load(4)
        shopController = ShopController()
        shopController.load()
        pc = PlayerController()
        pc.load(4, patronController)
        cardId = shopController.ranks[0].hand.cards[0].card_id
        price = shopController.ranks[0].hand.cards[0].price
        pc.players[0].tokens = TokenArray([7, 7, 7, 7, 7, 5])
        pc.buy_shop_card(0, cardId)
        self.assertEqual(pc.players[0].tokens.get_tokens(
        ), (TokenArray([7, 7, 7, 7, 7, 5]) - price).get_tokens())
        self.assertEqual(pc.players[0].hand.cards[0].card_id, cardId)

    def test_reserve_card(self):
        patronController = PatronController()
        patronController.load(4)
        shopController = ShopController()
        shopController.load()
        pc = PlayerController()
        pc.load(4, patronController)
        cardId = shopController.ranks[0].hand.cards[0].card_id
        if err := pc.reserve_card(0, cardId):
            Logger().log(0, err, 'test_reserve_card')
        self.assertEqual(pc.players[0].tokens.get_tokens()[
                         Color.GOLD.value], 1)
        self.assertEqual(pc.players[0].reserved.cards[0].card_id, cardId)

    def test_take_tokens(self):
        patronController = PatronController()
        patronController.load(4)
        bankController = BankController()
        bankController.load(nbPlayer=4)
        pc = PlayerController()
        pc.load(4, patronController)
        if err := pc.take_tokens(0, TokenArray([1, 1, 1, 0, 0, 0])):
            print(err)
        self.assertEqual(pc.players[0].tokens.get_tokens(), [1, 1, 1, 0, 0, 0])
        pc.take_tokens(0, TokenArray([0, 0, 0, 2, 0, 0]))
        self.assertEqual(pc.players[0].tokens.get_tokens(), [1, 1, 1, 2, 0, 0])


if __name__ == '__main__':
    unittest.main()
