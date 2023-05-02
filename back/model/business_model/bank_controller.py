from dataclasses import dataclass
from logging import raiseExceptions
from model.utils.exception import TooMuchBankTokens, InvalidTakeTokenAction
from model.business_model.token_array import TokenArray


@dataclass
class BankController():
    """This class is used to manage the bank of the game.

    Attributes:
        bank (TokenArray): The tokens in the bank.
        maxInBank (TokenArray): The maximum number of tokens in the bank.
        """
    bank: TokenArray = None
    maxInBank: TokenArray = None

    def __init__(self, nb_player=4) -> None:
        """The constructor of the class.

        Args:
            nb_player (int): The number of players in the game.

            """

        if nb_player == 2:
            self.bank = TokenArray([4, 4, 4, 4, 4, 5])
            self.maxInBank = TokenArray([4, 4, 4, 4, 4, 5])
        elif nb_player == 3:
            self.bank = TokenArray([5, 5, 5, 5, 5, 5])
            self.maxInBank = TokenArray([5, 5, 5, 5, 5, 5])
        elif nb_player == 4:
            self.bank = TokenArray([7, 7, 7, 7, 7, 5])
            self.maxInBank = TokenArray([7, 7, 7, 7, 7, 5])
        else:
            raiseExceptions("Number of players unsupported")

    def deposit(self, tokens: TokenArray) -> None or TooMuchBankTokens:
        """This method is used to deposit tokens in the bank.

        Args:
            tokens (TokenArray): The tokens to deposit.

            """
        if self.bank + tokens <= self.maxInBank:
            self.bank += tokens
        else:
            return TooMuchBankTokens()

    def withdraw(self, tokens: TokenArray) -> None or InvalidTakeTokenAction:
        """This method is used to withdraw tokens from the bank.

        Args:
            tokens (TokenArray): The tokens to withdraw.

            """
        assert isinstance(tokens, TokenArray)
        if tokens.nb_of_tokens() == 1:
            # if tokens.get_tokens()[Color.GOLD.value] != 1:
            # Logger().log(2, None, '1')
            # return InvalidTakeTokenAction() TODO: corriger ca
            pass
        elif tokens.nb_of_tokens() == 2:
            if sum([1 if x == 2 else 0 for x in tokens.get_tokens()]) != 1:
                """Logger().log(2, None, '2')
                return InvalidTakeTokenAction()"""
                pass
            elif self.bank.get_tokens()[tokens.get_tokens().index(2)] < 4:
                """Logger().log(2, None, '3')
                return InvalidTakeTokenAction()"""
                pass
        elif tokens.nb_of_tokens() == 3:
            if sum([1 if x == 1 else 0 for x in tokens.get_tokens()]) != 3:
                """Logger().log(2, None, '4')
                return InvalidTakeTokenAction()"""
                pass
        else:
            return InvalidTakeTokenAction()

        if error := self.bank.withdraw_tokens(tokens):
            return error

    def cheat_withdraw(self, tokens: TokenArray()) -> None:
        """This method is used to withdraw tokens from the bank.

        Args:
        tokens (TokenArray): The tokens to withdraw.

        """

        if error := self.bank.withdraw_tokens(tokens):
            return error

    def can_deposit(self, tokens: TokenArray) -> bool:
        """This method is used to check if the bank can deposit tokens.

        Args:
            tokens (TokenArray): The tokens to deposit.
            """
        return self.bank + tokens <= self.maxInBank

    def can_withdraw(self, tokens: TokenArray) -> bool:
        """This method is used to check if the bank can withdraw tokens.

        Args:
            tokens (TokenArray): The tokens to withdraw.
            """

        return self.bank.can_withdraw(tokens)
    
    def gather_bank_information_api_board_state(self) -> list[int]:
        """Gather the bank information needed for the api board state. 
        This information is the list of tokens of the bank.

        Returns:
            list[int]: tokens of the bank
        """
        return self.bank.get_tokens()
