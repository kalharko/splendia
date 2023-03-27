from dataclasses import dataclass
from typing import List

from Model.rank import Card, Hand, Rank
from Model.token_array import TokenArray
from Model.Patron import Patron
from Model.Player import Player


@dataclass
class BankController():
    bank: TokenArray

    def __init__(self, nbPlayer: int) -> None:
        pass

    def deposit(self, tokens: TokenArray) -> None:
        pass

    def withdraw(self, token: TokenArray) -> None:
        pass


@dataclass
class PatronController():
    patrons: List[Patron]

    def __init__(self, nbPlayer: int) -> None:
        pass

    def withdraw(self, hand: Hand) -> Patron:
        pass


@dataclass
class PlayerController():
    players: List[Player]

    def __init__(self, nbPlayer: int) -> None:
        pass

    def buy_reserved_card(self, playerId: int, cardId: int) -> None:
        pass

    def buy_shop_card(self, playerId: int, cardId: int) -> None:
        pass

    def reserve_card(self, playerId: int, cardId: int) -> None:
        pass

    def take_tokens(self, playerId: int, tokens: TokenArray) -> None:
        pass


@dataclass
class ShopController():
    ranks: List[Rank]

    def __init__(self) -> None:
        with open("Model/data/cards.csv", 'r') as file:
            file = file.readlines()
        self.ranks[0].load(file[3:43])
        self.ranks[1].load(file[43:73])
        self.ranks[2].load(file[73:-1])

    def get_card_price(self, cardId: int) -> Card:
        pass

    def withdraw_card(self, cardId: int) -> Card:
        pass
