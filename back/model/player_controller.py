from dataclasses import dataclass
from typing import List
from utils.exception import TooMuchReservedCards, PlayerCanNotPay
from model.patron_controller import PatronController
from model.bank_controller import BankController
from model.shop_controller import ShopController
from model.token_array import TokenArray
from model.player import Player
from model.card import Card
from utils.logger import Logger


@dataclass
class PlayerController():
    """This class is used to manage the players of the game.
    It contains a list of players and methods to interact with them.

    Attributes:
        players (List[Player]): The list of players.
        idHumanPlayer: id of the humain player
        """
    players: List[Player]
    idHumanPlayer: int

    def __init__(self, nbPlayer: int, observer: PatronController):
        """This method initializes the player controller. It creates the list of players.

        Args:
            nbPlayer (int): The number of players.
            observer (PatronController): The patron controller.
            """
        assert isinstance(nbPlayer, int)
        assert isinstance(observer, PatronController)

        self.players = [Player(i, observer) for i in range(nbPlayer)]
        self.idHumanPlayer = 0

    def buy_reserved_card(self, playerId: int, cardId: int, bank_controller: BankController) -> TokenArray or None:
        """This method buys a reserved card from a player.

        Args:
            playerId (int): The id of the player.
            cardId (int): The id of the card.
            bank_controller (BankController): The bank controller.

        Returns:
            TokenArray or None: The price of the card if the player has it, None otherwise.
            """
        assert isinstance(playerId, int)
        assert isinstance(cardId, int)
        assert isinstance(bank_controller, BankController)

        # TODO: check the return types
        if not isinstance(price := self.players[playerId].get_card_price_reserved_card(cardId), TokenArray):
            return price
        to_deposit, _ = self.players[playerId].pay(price)
        if not isinstance(to_deposit, TokenArray):
            return to_deposit

        bank_controller.deposit(to_deposit)
        if not isinstance(card := self.players[playerId].withdraw_reserved_card(cardId), Card):
            return card
        self.players[playerId].deposit_card(card)

    def buy_shop_card(self, playerId: int, cardId: int, shop_controller: ShopController,
                      bank_controller: BankController) -> None or TokenArray:
        """This method buys a card from the shop.

        Args:
            playerId (int): The id of the player.
            cardId (int): The id of the card.
            shop_controller (ShopController): The shop controller.
            bank_controller (BankController): The bank controller.

        Returns:
            None or TokenArray: None if the player has not enough tokens, the price of the card otherwise.
            """
        assert isinstance(playerId, int)
        assert isinstance(cardId, int)
        assert isinstance(shop_controller, ShopController)
        assert isinstance(bank_controller, BankController)

        player = self.players[playerId]
        if not isinstance(price := shop_controller.get_card_price(cardId), TokenArray):
            return price
        to_deposit, _ = player.pay(price)
        if not isinstance(to_deposit, TokenArray):
            return to_deposit

        bank_controller.deposit(to_deposit)
        card = shop_controller.withdraw_card(cardId)
        player.deposit_card(card)

    def reserve_card(self, playerId: int, cardId: int, shop_controller: ShopController,
                     bank_controller: BankController) -> Card or None:
        """This method reserves a card from the shop.

        Args:
            playerId (int): The id of the player.
            cardId (int): The id of the card.
            shop_controller (ShopController): The shop controller.
            bank_controller (BankController): The bank controller.

        Returns:
            Card or None: The card if the player has it, None otherwise.
            """
        assert isinstance(playerId, int)
        assert isinstance(cardId, int)
        assert isinstance(shop_controller, ShopController)
        assert isinstance(bank_controller, BankController)

        if self.players[playerId].nb_reserved_cards() >= 3:
            return TooMuchReservedCards()
        if not isinstance(card := shop_controller.withdraw_card(cardId), Card):
            Logger().log(0, card, '0')
            return card
        if bank_controller.bank.get_tokens()[5] != 0:
            if error := bank_controller.withdraw_gold(TokenArray([0, 0, 0, 0, 0, 1]), self.players[playerId].tokens):
                return error
            if self.players[playerId].tokens.nb_of_tokens() < 10:

                if err := self.players[playerId].deposit_tokens(TokenArray([0, 0, 0, 0, 0, 1])):
                    return err
        self.players[playerId].deposit_reserved_card(card)

    def reserve_pile_card(self, playerId: int, pileLevel: int, shop_controller: ShopController) -> None or TooMuchReservedCards:
        """This method reserves a card from a pile.

        Args:
            playerId (int): The id of the player.
            pileLevel (int): The level of the pile.
            shop_controller (ShopController): The shop controller.

        Returns:
            None or TooMuchReservedCards: None if the player has not too much reserved cards, TooMuchReservedCards otherwise.
            """
        assert isinstance(playerId, int)
        assert isinstance(pileLevel, int)
        assert isinstance(shop_controller, ShopController)

        if self.players[playerId].nb_reserved_cards() >= 3:
            return TooMuchReservedCards()
        if shop_controller.can_withdraw_pile_card(pileLevel):
            self.players[playerId].deposit_reserved_card(
                shop_controller.withdraw_pile_card(pileLevel))

    def take_tokens(self, playerId: int, tokens: TokenArray, bank_controller: BankController) -> None:
        """This method takes tokens from the bank.

        Args:
            playerId (int): The id of the player.
            tokens (TokenArray): The tokens to take.
            bank_controller (BankController): The bank controller.

        Returns:
            None or TokenArray: None if the player has not enough tokens, the price of the card otherwise.
            """
        assert isinstance(playerId, int)
        assert isinstance(tokens, TokenArray)
        assert isinstance(bank_controller, BankController)

        if (error := bank_controller.withdraw(tokens, self.players[playerId].tokens)) is not None:
            with open('log.txt', 'a') as file:
                file.write('err' + str(type(error)) + '\n')
            return error
        self.players[playerId].deposit_tokens(tokens)

    def cheat_take_tokens(self, playerId: int, tokens: TokenArray, bank_controller: BankController) -> None:
        """This method takes tokens from the bank without checking if the player has enough tokens.

        Args:
            playerId (int): The id of the player.
            tokens (TokenArray): The tokens to take.
            bank_controller (BankController): The bank controller.
            """
        assert isinstance(playerId, int)
        assert isinstance(tokens, TokenArray)
        assert isinstance(bank_controller, BankController)

        bank_controller.cheat_withdraw(tokens)
        self.players[playerId].deposit_tokens(tokens)

    def get_human_player(self) -> Player:
        """Get the human player

        Returns:
            Player: the human player
            """

        return self.players[self.idHumanPlayer]

    def get_cpu_players(self) -> list[Player]:
        """Get the CPU players

        Returns:
            list[Player]: list of the CPU players
            """

        human_player = self.get_human_player()
        return filter(lambda player: player != human_player, self.players)

    def gather_human_player_information_api_board_state(self, currentPlayer: int) -> dict:
        """Gather the human player information needed for the api board state in a dictionnary.

        Returns:
            dict: human player information for the api board state
            """

        return self.get_human_player().gather_human_player_information_api_board_state(currentPlayer)

    def gather_cpu_players_information_api_board_state(self, currentPlayer: int) -> list:
        """Gather the information of the CPU players needed for the api board state in a list

        Returns:
            list: contains information of each CPU player for the api board state
            """

        return [cpu_player.gather_cpu_player_information_api_board_state(currentPlayer) for cpu_player in self.get_cpu_players()]

    def check_human_player_too_many_tokens(self) -> bool:
        """Check if the human player has too many tokens

        Returns:
            bool: true if the human player has too many tokens
            """

        return self.get_human_player().check_too_many_tokens()

    def get_winners(self) -> list[Player]:
        """Get the winners of the game

        Returns:
            list[Player]: winners of the game. The list can be empty if there are no winners
            """

        # Find the maximum amount of points of the players
        maxPoints = 0
        for player in self.players:
            playerVictoryPoints = player.get_victory_points().get_value()
            if (playerVictoryPoints > maxPoints):
                maxPoints = playerVictoryPoints

        # if the maximum amount of points is less than 15, then there are no winners
        if (maxPoints < 15):
            return []

        # return the players who's points are equal to the maximum amount of points found
        return [player for player in self.players if player.get_victory_points().get_value() == maxPoints]

    def gather_winner_information_api_board_state(self) -> list[int]:
        """Gather the ids of the winners for the api board state

        Returns:
            list[int]: ids of the winners. The list is empty if there are no winners
            """

        return [winner.get_id() for winner in self.get_winners()]
