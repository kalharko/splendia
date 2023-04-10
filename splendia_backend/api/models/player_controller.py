from typing import List

from .utils.exception import TooManyReservedCardsException
from api.models import BankController
from api.models import ShopController
from api.models.utils.singleton_model import SingletonModel
from api.models import TokenArray
from api.models import Player
from api.models import Card
from api.models import PatronController
from django.db import models


class PlayerController(SingletonModel):
    players: List[Player] = models.ForeignKey(Player, on_delete=models.CASCADE)

    def __init__(self, nbPlayer: int, observers: PatronController) -> None:
        self.players = [Player(i, observers) for i in range(nbPlayer)]

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
            return TooManyReservedCardsException()
        if not isinstance(card := ShopController().withdraw_card(cardId), Card):
            return card
        if not isinstance(error := BankController().withdraw(TokenArray([0, 0, 0, 0, 0, 1])), TokenArray):
            return error
        player.deposit_reserved_card(card)
        player.deposit_tokens(TokenArray([0, 0, 0, 0, 0, 1]))

    def take_tokens(self, playerId: int, tokens: TokenArray) -> None:
        player = self.players[playerId]
        if not isinstance(error := BankController().withdraw(tokens), TokenArray):
            return error
        player.deposit_tokens(tokens)
