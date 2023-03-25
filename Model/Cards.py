from dataclasses import dataclass
from typing import List

from Model.Bank import TokenArray
from Model.VictoryPoint import VictoryPoint


@dataclass
class Card():
    price: TokenArray
    bonus: TokenArray
    victoryPoint: VictoryPoint

@dataclass
class Hand():
    cards: List[Card]

@dataclass
class Deck():
    cards: List[Card]

@dataclass
class Rank():
    hand: Hand
    deck: Deck

