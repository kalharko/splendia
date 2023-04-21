from dataclasses import dataclass

from model.utils.exception import NotEnoughTokens, TooMuchBankTokens,InvalidTakeTokenAction
from model.utils.singleton import SingletonMeta
from model.token_array import TokenArray, Color
from model.utils.logger import Logger


@dataclass
class BankController(metaclass=SingletonMeta):
    bank: TokenArray = None
    maxInBank: TokenArray = None

    def __init__(self):
        if not self.bank:
            Logger().log(1, self, 'BankController not loaded')
            self.load(4)

    def load(self, nbPlayer: int) -> None:
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
        if tokens.nb_of_tokens() == 1:
            if tokens.get_tokens()[Color.GOLD.value] != 1:
                Logger().log(2, None, '1')
                return InvalidTakeTokenAction()
        elif tokens.nb_of_tokens() == 2:
            if sum([1 if x == 2 else 0 for x in tokens.get_tokens()]) != 1:
                Logger().log(2, None, '2')
                return InvalidTakeTokenAction()
            elif self.bank.get_tokens()[tokens.get_tokens().index(2)] < 4:
                Logger().log(2, None, '3')
                return InvalidTakeTokenAction()
        elif tokens.nb_of_tokens() == 3:
            if sum([1 if x == 1 else 0 for x in tokens.get_tokens()]) != 3:
                Logger().log(2, None, '4')
                return InvalidTakeTokenAction()
        else:
            return InvalidTakeTokenAction()

        if error := self.bank.withdraw_tokens(tokens):
            return error

    def cheat_withdraw(self, tokens: TokenArray()) -> None:
        if error := self.bank.withdraw_tokens(tokens):
            return error

    def can_deposit(self, tokens: TokenArray) -> bool:
        return self.bank + tokens <= self.maxInBank

    def can_withdraw(self, tokens: TokenArray) -> bool:
        return self.bank.can_withdraw(tokens)
