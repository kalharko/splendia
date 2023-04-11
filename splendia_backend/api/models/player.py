from typing import List

from .utils.exception import PlayerCanNotPayException
from api.models import VictoryPoint
from api.models import TokenArray
from api.models import Patron
from api.models import Hand
from api.models import Card
from api.models import PatronController
from django.db import models


class Player(models.Model):
    player_id: int = models.IntegerField()
    hand: Hand = models.OneToOneField(Hand, on_delete=models.CASCADE, related_name='hand', null=True)
    reserved: Hand = models.OneToOneField(Hand, on_delete=models.CASCADE, related_name='reserved', null=True)
    tokens: TokenArray = models.OneToOneField(TokenArray, on_delete=models.CASCADE, null=True)
    victoryPoints: VictoryPoint = models.OneToOneField(VictoryPoint, on_delete=models.CASCADE, null=True)
    patrons: List[Patron] = models.ManyToManyField(Patron, blank=True)
    observers: PatronController = models.OneToOneField(PatronController, on_delete=models.CASCADE, null=True)

    def __init__(self, player_id: int, observer: PatronController) -> None:
        self.player_id = player_id
        self.hand = Hand([])
        self.reserved = Hand([])
        self.tokens = TokenArray()
        self.victoryPoints = VictoryPoint(0)
        self.patrons = []
        self.observers = observer

    def get_card_price(self, cardId: int) -> TokenArray:
        return self.reserved.get_card_price(cardId)

    def pay(self, price: TokenArray) -> None:
        if self.tokens.can_pay(price):
            self.tokens -= price
        else:
            return PlayerCanNotPayException()

    def withdraw_reserved_card(self, cardId: int) -> Card:
        return self.reserved.pop_card(cardId)

    def deposit_card(self, card: Card) -> None:
        self.hand.add_card(card)
        patron_get = self.notify_observers()
        if patron_get is not None:
            self.patrons.append(patron_get)

    def notify_observers(self) -> Patron:
        return self.observers.update(self.hand)

    def deposit_reserved_card(self, card: Card) -> None:
        self.reserved.add_card(card)

    def deposit_tokens(self, tokens: TokenArray) -> None:
        self.tokens.deposit_tokens(tokens)

    def nb_reserved_cards(self):
        return self.reserved.get_size()
