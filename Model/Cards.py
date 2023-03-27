from dataclasses import dataclass
from random import random
from typing import List

from Model.TokenArray import TokenArray
from Model.Utils import retrieve_and_parse_cards
from Model.VictoryPoint import VictoryPoint
import pandas as pd
"""
This module contains the classes that represent the cards in the game.
"""
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


@dataclass
class CardStack():
    cards: List[Card]

    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    def pop_card(self, cardId: int) -> Card:
        pass


@dataclass
class Hand(CardStack):

    def compute_hand_bonuses(self) -> TokenArray:
        pass


@dataclass
class Deck(CardStack):

    def draw(self) -> Card:
        return self.cards.pop(random.range(0, len(self.cards)))


@dataclass
class Rank():
    hand: Hand
    deck: Deck

    def __init__(self, csv: List[str]) -> None:
        # load the deck with cards

        self.deck = retrieve_and_parse_cards()

        # load the hand with 3 random cards
        for i in range(3):
            self.hand.add_card(self.deck.draw())

    def get_card_price(self, cardId: int) -> TokenArray:
        pass

    def withdraw_card(self, cardId: int) -> Card:
        pass
