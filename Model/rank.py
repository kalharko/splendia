from dataclasses import dataclass
from typing import List
import pandas as pd

from model.card import Card
from model.token_array import TokenArray
from model.utils import retrieve_and_parse_cards
"""
This module contains the classes that represent the cards in the game.
"""
from model.deck import Deck
from model.hand import Hand


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
