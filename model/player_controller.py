from dataclasses import dataclass
from typing import List
from model.utils.exception import TooMuchReservedCards
from model.patron_controller import PatronController
from model.bank_controller import BankController
from model.shop_controller import ShopController
from model.utils.singleton import SingletonMeta
from model.game_manager import GameManager
from model.token_array import TokenArray
from model.player import Player
from model.card import Card


@dataclass
class PlayerController():
    players: List[Player]
    gameManager: GameMAnager

    def __init__(self, nbPlayer: int, observer: PatronController, gameManager: GameManager):
        self.players = [Player(i, observer) for i in range(nbPlayer)]
        self.gameManager = gameManager

    def buy_reserved_card(self, playerId: int, cardId: int) -> None:
        if not isinstance(price := self.players[playerId].get_card_price(cardId), TokenArray):
            return price
        to_deposit, _ = self.players[playerId].pay(price)
        """ if error := self.players[playerId].pay(price):
            print('aaa\n')
            return error"""

        self.gameManager.bankController.deposit(to_deposit)
        if not isinstance(card := self.players[playerId].withdraw_reserved_card(cardId), Card):
            return card
        self.players[playerId].deposit_card(card)

    def buy_shop_card(self, playerId: int, cardId: int) -> None:
        player = self.players[playerId]
        if not isinstance(price := self.gameManager.shopController.get_card_price(cardId), TokenArray):
            return price
        to_deposit, _ = player.pay(price)
        """if error := player.pay(price):
            return error"""
        self.gameManager.bankController.deposit(to_deposit)
        card = self.gameManager.shopController.withdraw_card(cardId)
        player.deposit_card(card)

    def reserve_card(self, playerId: int, cardId: int) -> None:
        if self.players[playerId].nb_reserved_cards() >= 3:
            return TooMuchReservedCards()
        if not isinstance(card := self.gameManager.shopController.withdraw_card(cardId), Card):
            return card
        if self.gameManager.bankController.bank.get_tokens()[5] != 0:
            if error := self.gameManager.bankController.withdraw(TokenArray([0, 0, 0, 0, 0, 1])):
                return error
            if err := self.players[playerId].deposit_tokens(TokenArray([0, 0, 0, 0, 0, 1])):
                return err
        self.players[playerId].deposit_reserved_card(card)

    def reserve_pile_card(self, playerId: int, pileLevel: int) -> None:
        if self.players[playerId].nb_reserved_cards() >= 3:
            return TooMuchReservedCards()
        if self.gameManager.shopController.can_withdraw_pile_card(pileLevel):
            self.players[playerId].deposit_reserved_card(self.gameManager.shopController.withdraw_pile_card(pileLevel))

    def take_tokens(self, playerId: int, tokens: TokenArray) -> None:
        if (error := self.gameManager.bankController.withdraw(tokens)) is not None:
            with open('log.txt', 'a') as file:
                file.write('err' + str(type(error)) + '\n')
            return error
        self.players[playerId].deposit_tokens(tokens)

    def cheat_take_tokens(self, playerId: int, tokens: TokenArray) -> None:
        self.gameManager.bankController.cheat_withdraw(tokens)
        self.players[playerId].deposit_tokens(tokens)
