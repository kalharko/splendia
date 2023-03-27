from dataclasses import dataclass
from random import random
from typing import List
from Model.card import Card
from Model.token_array import TokenArray
from Model.Utils import retrieve_and_parse_cards
from Model.victory_point import VictoryPoint
import pandas as pd
"""
This module contains the classes that represent the cards in the game.
"""
from Model.deck import Deck
from Model.hand import Hand






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
