from dataclasses import dataclass
from typing import List, Tuple

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
    bonus_tokens: TokenArray
    tokens: TokenArray
    victoryPoints: VictoryPoint
    patrons: List[Patron]
    observer: PatronController

    def __init__(self, player_id: int, observer: PatronController) -> None:
        self.player_id = player_id
        self.hand = Hand([])
        self.reserved = Hand([])
        self.tokens = TokenArray()
        self.bonus_tokens = TokenArray()
        self.victoryPoints = VictoryPoint(0)
        self.patrons = []
        self.observer = observer

    def get_card_price(self, cardId: int) -> TokenArray:
        return self.reserved.get_card_price(cardId)

    def pay(self, price: TokenArray) -> int or PlayerCanNotPay:
        assert isinstance(price, TokenArray)
        #tokens = self.tokens.get_tokens()
        can_pay, reduced_price = self.can_pay_with_reduced_price(price)

        if can_pay:
            to_deposit = self.tokens.pay(reduced_price)

            return to_deposit, None

        else:
            return PlayerCanNotPay()

    def can_pay_with_reduced_price(self, price: TokenArray) -> tuple[bool, TokenArray]:
        assert isinstance(price, TokenArray)
        reduced_price = price - self.bonus_tokens
        for i in range(len(reduced_price.get_tokens())):
            if reduced_price.get_tokens()[i] < 0:
                reduced_price.get_tokens()[i] = 0
        return self.tokens.can_pay(reduced_price) , reduced_price


    def withdraw_reserved_card(self, cardId: int) -> Card:
        return self.reserved.pop_card(cardId)

    def deposit_card(self, card: Card) -> None:
        self.hand.add_card(card)
        self.victoryPoints.set_value(self.victoryPoints.get_value() + card.victoryPoint.value)
        self.bonus_tokens.deposit_tokens(card.bonus)

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
