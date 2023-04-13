from dataclasses import dataclass
from typing import List

from model.utils.exception import TooMuchReservedCards
from model.bank_controller import BankController
from model.shop_controller import ShopController
from model.utils.singleton import SingletonMeta
from model.token_array import TokenArray
from model.player import Player
from model.card import Card
from model.patron_controller import PatronController


@dataclass
class PlayerController(metaclass=SingletonMeta):
    players: List[Player]

    def __init__(self, nbPlayer: int, observer: PatronController) -> None:
        self.players = [Player(i, observer) for i in range(nbPlayer)]

    def buy_reserved_card(self, playerId: int, cardId: int) -> None:
        player = self.players[playerId]
        if not isinstance(price := player.get_card_price(cardId), TokenArray):
            return price
        if error := player.pay(price):
            return error

        BankController().deposit(price)
        card = player.withdraw_reserved_card(cardId)
        player.deposit_card(card)

    def buy_shop_card(self, playerId: int, cardId: int) -> None:
        player = self.players[playerId]
        if not isinstance(price := ShopController().get_card_price(cardId), TokenArray):
            return price
        if error := player.pay(price):
            return error
        BankController().deposit(price)
        card = ShopController().withdraw_card(cardId)
        player.deposit_card(card)

    def reserve_card(self, playerId: int, cardId: int) -> None:
        player = self.players[playerId]
        if player.nb_reserved_cards() >= 3:
            return TooMuchReservedCards()
        if not isinstance(card := ShopController().withdraw_card(cardId), Card):
            return card
        if not isinstance(error := BankController().withdraw(TokenArray([0, 0, 0, 0, 0, 1])), TokenArray):
            return error
        player.deposit_reserved_card(card)
        player.deposit_tokens(TokenArray([0, 0, 0, 0, 0, 1]))

    def take_tokens(self, playerId: int, tokens: TokenArray) -> None:
        if (error := BankController().withdraw(tokens)) != None:
            return error
        self.players[playerId].deposit_tokens(tokens)
