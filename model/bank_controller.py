from dataclasses import dataclass
from logging import raiseExceptions
from model.token_array import TokenArray
from model.utils.singleton import SingletonMeta


@dataclass
class BankController(metaclass=SingletonMeta):
    bank: TokenArray

    def __init__(self, nbPlayer: int) -> None:
        # number of tokens depends on the number of players
        if nbPlayer == 2:
            self.bank.deposit_tokens([4, 4, 4, 4, 4, 5])
        elif nbPlayer == 3:
            self.bank.deposit_tokens([5, 5, 5, 5, 5, 5])
        elif nbPlayer == 4:
            self.bank.deposit_tokens([7, 7, 7, 7, 7, 5])
        else:
            raiseExceptions("Number of players unsupported")

    def deposit(self, tokens: TokenArray) -> None:
        pass

    def withdraw(self, token: TokenArray) -> None:
        pass
