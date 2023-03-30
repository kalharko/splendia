from dataclasses import dataclass
from typing import List

from model.utils.exception import PlayerCanNotPay
from model.victory_point import VictoryPoint
from model.token_array import TokenArray
from model.patron import Patron
from model.rank import Hand
from model.card import Card


@dataclass
class Player():
    player_id: int
    hand: Hand
    reserved: Hand
    tokens: TokenArray
    victoryPoints: VictoryPoint
    patrons: List[Patron]

    def __init__(self, player_id: int) -> None:
        self.player_id = player_id
        self.hand = Hand()
        self.reserved = Hand()
        self.tokens = TokenArray()
        self.victoryPoints = VictoryPoint()
        self.patrons = []

    def get_card_price(self, cardId: int) -> TokenArray:
        return self.reserved.get_card_price(cardId)

    def pay(self, price: TokenArray) -> None:
        if self.tokens >= price:
            self.tokens -= price
        else:
            return PlayerCanNotPay()

    def withdraw_reserved_card(self, cardId: int) -> Card:
        return self.reserved.pop_card(cardId)

    def deposit_card(self, card: Card) -> None:
        self.hand.add_card(card)

    def deposit_reserved_card(self, card: Card) -> None:
        self.reserved.add_card(card)

    def deposit_tokens(self, tokens: TokenArray) -> None:
        self.tokens.deposit_tokens(tokens)

    def nb_reserved_cards(self):
        return self.reserved.get_size()
