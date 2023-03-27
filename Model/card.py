from dataclasses import dataclass
from token_array import TokenArray
from victory_point import VictoryPoint


@dataclass
class Card():
    card_id: int
    price: TokenArray
    bonus: TokenArray
    victoryPoint: VictoryPoint

    def __init__(self, price: TokenArray, bonus: TokenArray,
                 victoryPoint: VictoryPoint, card_id: int) -> None:
        self.price = price
        self.bonus = bonus
        self.victoryPoint = victoryPoint
        self.card_id = card_id

