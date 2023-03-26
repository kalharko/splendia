from dataclasses import dataclass
from random import random
from typing import List

from Model.TokenArray import TokenArray
from Model.VictoryPoint import VictoryPoint


@dataclass
class Card():
    price: TokenArray
    bonus: TokenArray
    victoryPoint: VictoryPoint

    def __init__(self, price: TokenArray, bonus: TokenArray,
                 victoryPoint: VictoryPoint) -> None:
        self.price = price
        self.bonus = bonus
        self.victoryPoint = victoryPoint


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
        for line in csv:
            line = line.rstrip('\n').split(',')
            line = [x if x != '' else '0' for x in line]
            price = [int(x) for x in line[6:11]] + [0]
            bonus = [0 for x in range(6)]
            bonus[int(line[2])] = 1
            self.deck.append(Card(
                TokenArray(price),
                TokenArray(bonus),
                VictoryPoint(int(line[3]))
            ))

        # load the hand with 3 random cards
        for i in range(3):
            self.hand.add_card(self.deck.draw())

    def get_card_price(self, cardId: int) -> TokenArray:
        pass

    def withdraw_card(self, cardId: int) -> Card:
        pass
