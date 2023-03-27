from dataclasses import dataclass
from typing import List

from model.token_array import TokenArray
from model.player import Player


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
