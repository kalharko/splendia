from dataclasses import dataclass
from typing import List

from model.utils.exception import PlayerCanNotPay
from model.victory_point import VictoryPoint
from model.token_array import TokenArray
from model.patron import Patron
from model.rank import Hand
from model.card import Card
from model.patron_controller import PatronController

@dataclass
class Player():
    player_id: int
    hand: Hand
    reserved: Hand
    tokens: TokenArray
    victoryPoints: VictoryPoint
    patrons: List[Patron]
    observer: PatronController

    def __init__(self, player_id: int, observer: PatronController) -> None:
        self.player_id = player_id
        self.hand = Hand([])
        self.reserved = Hand([])
        self.tokens = TokenArray()
        self.victoryPoints = VictoryPoint(0)
        self.patrons = []
        self.observer = observer

    def get_card_price(self, cardId: int) -> TokenArray:
        return self.reserved.get_card_price(cardId)

    def pay(self, price: TokenArray) -> None:
        assert isinstance(price, TokenArray)

        if self.tokens.can_pay(price):
            self.tokens -= price
        else:
            return PlayerCanNotPay()

    def withdraw_reserved_card(self, cardId: int) -> Card:
        return self.reserved.pop_card(cardId)

    def deposit_card(self, card: Card) -> None:
        self.hand.add_card(card)
        patron_get = self.notify_observers()
        if patron_get is not None:
            self.patrons.append(patron_get)

    def notify_observers(self) -> Patron:
        return self.observer.update(self.hand)

    def deposit_reserved_card(self, card: Card) -> None:
        self.reserved.add_card(card)

    def deposit_tokens(self, tokens: TokenArray) -> None:
        if err := self.tokens.deposit_tokens(tokens):
            return err

    def nb_reserved_cards(self):
        return self.reserved.get_size()

    def update_victory_points(self):
        out = 0
        out += self.hand.compute_victory_points()
        for patron in self.patrons:
            out += patron.victoryPoints.get_value()
        self.victoryPoints.set_value(out)
