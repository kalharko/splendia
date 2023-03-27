from dataclasses import dataclass

from model.card_stack import CardStack
from model.token_array import TokenArray


@dataclass
class Hand(CardStack):

    def compute_hand_bonuses(self) -> TokenArray:
        pass
