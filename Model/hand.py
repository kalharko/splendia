from dataclasses import dataclass
from card_stack import CardStack
from token_array import TokenArray


@dataclass
class Hand(CardStack):

    def compute_hand_bonuses(self) -> TokenArray:
        pass

