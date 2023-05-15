from dataclasses import dataclass
from logging import raiseExceptions
from utils.exception import TooMuchBankTokens, InvalidTakeTokenAction
from model.token_array import TokenArray, Color
from utils.logger import Logger


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
        assert isinstance(nb_player, int)
        assert 2 <= nb_player <= 4

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
        assert isinstance(tokens, TokenArray)

        if self.bank + tokens <= self.maxInBank:
            self.bank += tokens
        else:
            return TooMuchBankTokens()

    def withdraw_gold(self, tokens: TokenArray, player_token: TokenArray):
        """This method is used to withdraw one gold from the bank

        Args:
            tokens (TokenArray):
            """
        assert isinstance(tokens, TokenArray)
        assert isinstance(player_token, TokenArray)

        if tokens.get_tokens()[Color.GOLD.value] != 1 or self.bank.get_tokens()[Color.GOLD.value] == 0:
            return InvalidTakeTokenAction()
        if player_token.nb_of_tokens() >= 10:
            # the bank does not discard tokens
            pass
        else:
            self.bank.withdraw_token(Color.GOLD, 1)

    def withdraw(self, tokens: TokenArray, player_token: TokenArray) -> None or InvalidTakeTokenAction:
        """This method is used to withdraw tokens from the bank.

        Args:
            tokens (TokenArray): The tokens to withdraw.
            """
        assert isinstance(tokens, TokenArray)
        assert isinstance(player_token, TokenArray)

        non_empty_pile = 0
        for color in range(5):
            if self.bank.get_tokens()[color] > 0:
                non_empty_pile += 1

        if tokens.nb_of_tokens() == 1:
            wanted_tokens_index = tokens.get_tokens().index(1)
            if player_token.nb_of_tokens() != 9 or non_empty_pile < 3 or self.bank.get_tokens()[wanted_tokens_index] == 0:
                return InvalidTakeTokenAction()
            # if tokens.get_tokens()[Color.GOLD.value] != 1:
            # Logger().log(2, None, '1')
            # return InvalidTakeTokenAction() TODO: corriger ca
            pass
        elif tokens.nb_of_tokens() == 2:

            if sum([1 if x == 2 else 0 for x in tokens.get_tokens()]) == 1:
                wanted_tokens_index = tokens.get_tokens().index(2)
                if player_token.nb_of_tokens() >= 9 or self.bank.get_tokens()[wanted_tokens_index] < 4:
                    Logger().log(2, None, '2')
                    return InvalidTakeTokenAction()
                    pass

            elif sum([1 if x == 1 else 0 for x in tokens.get_tokens()]) == 2:
                wanted_colors = []
                for color in range(5):
                    if tokens.get_tokens()[color] == 1:
                        wanted_colors.append(color)
                if player_token.nb_of_tokens() != 8 or self.bank.get_tokens()[wanted_colors[0]] == 0 or self.bank.get_tokens()[wanted_colors[1]] == 0 or non_empty_pile < 3:
                    return InvalidTakeTokenAction()
                    pass

        elif tokens.nb_of_tokens() == 3:
            wanted_colors = []
            for color in range(5):
                if tokens.get_tokens()[color] == 1:
                    wanted_colors.append(color)
            if sum([1 if x == 1 else 0 for x in tokens.get_tokens()]) != 3:
                return InvalidTakeTokenAction()
            elif player_token.nb_of_tokens() >= 8 or non_empty_pile < 3 or self.bank.get_tokens()[wanted_colors[0]] == 0 or self.bank.get_tokens()[wanted_colors[1]] == 0 or self.bank.get_tokens()[wanted_colors[2]] == 0:
                return InvalidTakeTokenAction()
        else:
            return InvalidTakeTokenAction()

        if error := self.bank.withdraw_tokens(tokens):
            return error

    def cheat_withdraw(self, tokens: TokenArray()) -> None:
        """This method is used to withdraw tokens from the bank.

        Args:
            tokens (TokenArray): The tokens to withdraw.
            """
        assert isinstance(tokens, TokenArray)

        if error := self.bank.withdraw_tokens(tokens):
            return error

    def can_deposit(self, tokens: TokenArray) -> bool:
        """This method is used to check if the bank can deposit tokens.

        Args:
            tokens (TokenArray): The tokens to deposit.
            """
        assert isinstance(tokens, TokenArray)

        return self.bank + tokens <= self.maxInBank

    def can_withdraw(self, tokens: TokenArray) -> bool:
        """This method is used to check if the bank can withdraw tokens.

        Args:
            tokens (TokenArray): The tokens to withdraw.
            """
        assert isinstance(tokens, TokenArray)

        return self.bank.can_withdraw(tokens)

    def gather_bank_information_api_board_state(self) -> list[int]:
        """Gather the bank information needed for the api board state.
        This information is the list of tokens of the bank.

        Returns:
            list[int]: tokens of the bank
            """
        return self.bank.get_tokens()
