from dataclasses import dataclass
from model.token_array import TokenArray


@dataclass
class BankController():
    bank: TokenArray

    def __init__(self, nbPlayer: int) -> None:
        pass

    def deposit(self, tokens: TokenArray) -> None:
        pass

    def withdraw(self, token: TokenArray) -> None:
        pass
