from dataclasses import dataclass
from logging import raiseExceptions
from model.token_array import TokenArray, Color
from model.utils.singleton import SingletonMeta
from model.utils.exception import NotEnoughTokens, TooMuchBankTokens,InvalidTakeTokenAction


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
        if tokens.tokens[Color.GOLD.value] != 0:
            return InvalidTakeTokenAction()
        if 2 < tokens.nb_of_tokens() > 3:
            return InvalidTakeTokenAction()
        if tokens.nb_of_tokens() == 2:
            if sum([1 if x == 2 else 0 for x in tokens.tokens]) != 1:
                return InvalidTakeTokenAction()
            elif self.bank.tokens[tokens.tokens.index(2)] < 4:
                return InvalidTakeTokenAction()
        elif sum([1 if x == 1 else 0 for x in tokens.tokens]) != 3:
            return InvalidTakeTokenAction()

        if error := self.bank.withdraw_tokens(tokens):
            return error

    def can_deposit(self, tokens: TokenArray) -> bool:
        return self.bank + tokens <= self.maxInBank

    def can_withdraw(self, tokens: TokenArray) -> bool:
        return self.bank.can_withdraw(tokens)
