from dataclasses import dataclass
from typing import List
from back.model.utils.exception import TooMuchReservedCards
from back.model.business_model.patron_controller import PatronController
from back.model.business_model.bank_controller import BankController
from back.model.business_model.shop_controller import ShopController
from back.model.business_model.token_array import TokenArray
from back.model.business_model.player import Player
from back.model.business_model.card import Card


@dataclass
class PlayerController():
    """This class is used to manage the players of the game.
    It contains a list of players and methods to interact with them.

    Attributes:
        players (List[Player]): The list of players.
        """
    players: List[Player]

    def __init__(self, nbPlayer: int, observer: PatronController):
        """This method initializes the player controller. It creates the list of players.

        Args:
            nbPlayer (int): The number of players.
            observer (PatronController): The patron controller.
            """
        self.players = [Player(i, observer) for i in range(nbPlayer)]

    def buy_reserved_card(self, playerId: int, cardId: int, bank_controller: BankController) -> TokenArray or None:
        """This method buys a reserved card from a player.

        Args:
            playerId (int): The id of the player.
            cardId (int): The id of the card.
            bank_controller (BankController): The bank controller.

        Returns:
            TokenArray or None: The price of the card if the player has it, None otherwise.

            """
        # TODO: check the return types
        if not isinstance(price := self.players[playerId].get_card_price_reserved_card(cardId), TokenArray):
            return price
        to_deposit, _ = self.players[playerId].pay(price)

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

        player = self.players[playerId]
        if not isinstance(price := shop_controller.get_card_price(cardId), TokenArray):
            return price
        to_deposit, _ = player.pay(price)
        """if error := player.pay(price):
            return error"""
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

        if self.players[playerId].nb_reserved_cards() >= 3:
            return TooMuchReservedCards()
        if not isinstance(card := shop_controller.withdraw_card(cardId), Card):
            return card
        if bank_controller.bank.get_tokens()[5] != 0:
            if error := bank_controller.withdraw(TokenArray([0, 0, 0, 0, 0, 1])):
                return error
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
        if (error := bank_controller.withdraw(tokens)) is not None:
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
        bank_controller.cheat_withdraw(tokens)
        self.players[playerId].deposit_tokens(tokens)
