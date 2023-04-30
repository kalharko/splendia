from dataclasses import dataclass
from typing import List
from model.utils.exception import TooMuchReservedCards
from model.patron_controller import PatronController
from model.bank_controller import BankController
from model.shop_controller import ShopController
from model.token_array import TokenArray
from model.player import Player
from model.card import Card


@dataclass
class PlayerController():
    players: List[Player]

    def __init__(self, nbPlayer: int, observer: PatronController):
        self.players = [Player(i, observer) for i in range(nbPlayer)]

    def buy_reserved_card(self, playerId: int, cardId: int, bank_controller :BankController) -> None:
        if not isinstance(price := self.players[playerId].get_card_price(cardId), TokenArray):
            return price
        to_deposit, _ = self.players[playerId].pay(price)
        """ if error := self.players[playerId].pay(price):
            print('aaa\n')
            return error"""

        bank_controller.deposit(to_deposit)
        if not isinstance(card := self.players[playerId].withdraw_reserved_card(cardId), Card):
            return card
        self.players[playerId].deposit_card(card)

    def buy_shop_card(self, playerId: int, cardId: int, shop_controller : ShopController,
                      bank_controller : BankController) -> None:
        player = self.players[playerId]
        if not isinstance(price := shop_controller.get_card_price(cardId), TokenArray):
            return price
        to_deposit, _ = player.pay(price)
        """if error := player.pay(price):
            return error"""
        bank_controller.deposit(to_deposit)
        card = shop_controller.withdraw_card(cardId)
        player.deposit_card(card)

    def reserve_card(self, playerId: int, cardId: int, shop_controller : ShopController,
                     bank_controller : BankController) -> None:
        if self.players[playerId].nb_reserved_cards() >= 3:
            return TooMuchReservedCards()
        if not isinstance(card := shop_controller.withdraw_card(cardId), Card):
            return card
        if bank_controller.bank.get_tokens()[5] != 0:
            if error := bank_controller.withdraw(TokenArray([0, 0, 0, 0, 0, 1])):
                return error
            if err := self.players[playerId].deposit_tokens(TokenArray([0, 0, 0, 0, 0, 1])):
                return err
        self.players[playerId].deposit_reserved_card(card)

    def reserve_pile_card(self, playerId: int, pileLevel: int, shop_controller :ShopController) -> None:
        if self.players[playerId].nb_reserved_cards() >= 3:
            return TooMuchReservedCards()
        if shop_controller.can_withdraw_pile_card(pileLevel):
            self.players[playerId].deposit_reserved_card(shop_controller.withdraw_pile_card(pileLevel))

    def take_tokens(self, playerId: int, tokens: TokenArray, bank_controller : BankController) -> None:
        if (error := bank_controller.withdraw(tokens)) is not None:
            with open('log.txt', 'a') as file:
                file.write('err' + str(type(error)) + '\n')
            return error
        self.players[playerId].deposit_tokens(tokens)

    def cheat_take_tokens(self, playerId: int, tokens: TokenArray, bank_controller : BankController) -> None:
        bank_controller.cheat_withdraw(tokens)
        self.players[playerId].deposit_tokens(tokens)
