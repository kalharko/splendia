from dataclasses import dataclass
from logging import raiseExceptions
from model.token_array import TokenArray
from model.utils.singleton import SingletonMeta
from model.utils.exception import NotEnoughTokens, TooMuchBankTokens


@dataclass
class BankController(metaclass=SingletonMeta):
    bank: TokenArray
    maxInBank: TokenArray

    def __init__(self, nbPlayer: int) -> None:
        # number of tokens depends on the number of players
        if nbPlayer == 2:
            self.bank = TokenArray([4, 4, 4, 4, 4, 5])
            self.maxInBank = TokenArray([4, 4, 4, 4, 4, 5])
        elif nbPlayer == 3:
            self.bank = TokenArray([5, 5, 5, 5, 5, 5])
            self.maxInBank = TokenArray([5, 5, 5, 5, 5, 5])
        elif nbPlayer == 4:
            self.bank = TokenArray([7, 7, 7, 7, 7, 5])
            self.maxInBank = TokenArray([7, 7, 7, 7, 7, 5])
        else:
            raiseExceptions("Number of players unsupported")

    def deposit(self, tokens: TokenArray) -> None:
        if self.bank + tokens <= self.maxInBank:
            self.bank += tokens
        else:
            return TooMuchBankTokens()

    def withdraw(self, tokens: TokenArray) -> None:
        if error := self.bank.withdraw_tokens(tokens):
            return error

    def can_deposit(self, tokens: TokenArray) -> bool:
        return self.bank + tokens <= self.maxInBank

    def can_withdraw(self, tokens: TokenArray) -> bool:
        return self.bank.can_withdraw(tokens)
