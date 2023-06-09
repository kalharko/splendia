from dataclasses import dataclass
from typing import List

from utils.exception import PlayerCanNotPay
from model.victory_point import VictoryPoint
from model.token_array import TokenArray
from model.patron import Patron
from model.rank import Hand
from model.card import Card
from model.patron_controller import PatronController


@dataclass
class Player():
    """This class is used to manage the players of the game.
    It contains a list of players and methods to interact with them.

    Attributes:
        playerId (int): The id of the player.
        hand (Hand): The hand of the player.
        reserved (Hand): The reserved cards of the player.
        bonus_tokens (TokenArray): The bonus tokens of the player.
        tokens (TokenArray): The tokens of the player.
        victoryPoints (VictoryPoint): The victory points of the player.
        patrons (List[Patron]): The patrons of the player.
        observer (PatronController): The patron controller.

        """
    playerId: int
    hand: Hand
    reserved: Hand
    bonus_tokens: TokenArray
    tokens: TokenArray
    victoryPoints: VictoryPoint
    patrons: List[Patron]
    observer: PatronController

    def __init__(self, playerId: int, observer: PatronController) -> None:
        """This method initializes the player.

        Args:
            playerId (int): The id of the player.
            observer (PatronController): The patron controller.

            """
        self.playerId = playerId
        self.hand = Hand([])
        self.reserved = Hand([])
        self.tokens = TokenArray()
        self.bonus_tokens = TokenArray()
        self.victoryPoints = VictoryPoint(0)
        self.patrons = []
        self.observer = observer

    def get_card_price_reserved_card(self, cardId: int) -> TokenArray:
        """This method returns the price of a reserved card.

        Args:
            cardId (int): The id of the card.

        Returns:
            TokenArray: The price of the card.
            """
        assert isinstance(cardId, int)

        return self.reserved.get_card_price(cardId)

    def pay(self, price: TokenArray) -> int or PlayerCanNotPay:
        """This method pays a price.

        Args:
            price (TokenArray): The price to pay.

        Returns:
            int or PlayerCanNotPay: The number of tokens to deposit if the player can pay, PlayerCanNotPay otherwise.
            """
        assert isinstance(price, TokenArray)

        # tokens = self.tokens.get_tokens()
        can_pay, reduced_price = self.can_pay_with_reduced_price(price)

        if can_pay:
            to_deposit = self.tokens.pay(reduced_price)

            return to_deposit, None

        else:
            return PlayerCanNotPay(), None

    def can_pay_with_reduced_price(self, price: TokenArray) -> tuple[bool, TokenArray]:
        """This method checks if the player can pay a price.

        Args:
            price (TokenArray): The price to pay.

        Returns:
            tuple[bool, TokenArray]: True if the player can pay, False otherwise. The reduced price.
            """
        assert isinstance(price, TokenArray)

        reduced_price = price - self.bonus_tokens
        for i in range(len(reduced_price.get_tokens())):
            if reduced_price.get_tokens()[i] < 0:
                reduced_price.get_tokens()[i] = 0
        return self.tokens.can_pay(reduced_price), reduced_price

    def withdraw_reserved_card(self, cardId: int) -> Card:
        """This method withdraws a reserved card.

        Args:
            cardId (int): The id of the card.

        Returns:
            Card: The card withdrawn.
            """
        assert isinstance(cardId, int)

        return self.reserved.pop_card(cardId)

    def deposit_card(self, card: Card) -> None:
        """This method deposits a card.

        Args:
            card (Card): The card to deposit.
            """
        assert isinstance(card, Card)

        self.hand.add_card(card)
        self.victoryPoints.set_value(
            self.victoryPoints.get_value() + card.victoryPoint.value)
        self.bonus_tokens.deposit_tokens(card.bonus)

        patron_get = self.notify_observers()
        if patron_get is not None:
            self.patrons.append(patron_get)
            self.victoryPoints.set_value(
                self.victoryPoints.get_value() + patron_get.victoryPoints.get_value())

    def notify_observers(self) -> Patron:
        """This method notifies the observers.

        Returns:
            Patron: The patron if the player has one, None otherwise.
            """

        return self.observer.update(self.hand)

    def deposit_reserved_card(self, card: Card) -> None:
        """This method deposits a reserved card.

        Args:
            card (Card): The card to deposit.
            """
        assert isinstance(card, Card)

        self.reserved.add_card(card)

    def deposit_tokens(self, tokens: TokenArray) -> None:
        """This method deposits tokens.

        Args:
            tokens (TokenArray): The tokens to deposit.
                """
        assert isinstance(tokens, TokenArray)

        if err := self.tokens.deposit_tokens(tokens):
            return err

    def nb_reserved_cards(self) -> int:
        """This method returns the number of reserved cards.

        Returns:
            int: The number of reserved cards.
            """

        return self.reserved.get_size()

    def update_victory_points(self):
        """This method updates the victory points of the player.
            """

        out = 0
        out += self.hand.compute_victory_points()
        for patron in self.patrons:
            out += patron.victoryPoints.get_value()
        self.victoryPoints.set_value(out)

    def gather_human_player_information_api_board_state(self, currentPlayer: int) -> dict:
        """Gather the human player information needed for the api board state in a dictionnary.
        The dictionnary contains:
        - the tokens of the player
        - the bonuses of the player in the form of a list of tokens
        - the victory points of the player
        - the reserved cards of the player
        - if the human player is current player

        Returns:
            dict: human player information for the api board state
            """

        return {
            'tokenList': self.tokens.get_tokens(),
            'bonusList': self.bonus_tokens.get_tokens(),
            'victoryPoints': self.victoryPoints.get_value(),
            'reservedCards': self.reserved.gather_cards_information_api_board_state(self),
            'currentPlayer': (self.playerId == currentPlayer),
            'id': self.get_id()
        }

    def gather_cpu_player_information_api_board_state(self, currentPlayer: int) -> dict:
        """Gather the CPU player information needed for the api board state in a dictionnary.
        The dictionnary contains:
        - the tokens of the player
        - the bonuses of the player in the form of a list of tokens
        - the victory points of the player
        - the number of the reserved cards of the player

        Returns:
            dict: shop information for the api board state
            """

        return {
            'tokenList': self.tokens.get_tokens(),
            'bonusList': self.bonus_tokens.get_tokens(),
            'victoryPoints': self.victoryPoints.get_value(),
            'numberReservedCards': self.reserved.get_number_cards(),
            'currentPlayer': (self.playerId == currentPlayer),
            'id': self.get_id()
        }

    def check_too_many_tokens(self) -> bool:
        """Check if the player has too many tokens.
        The maximum of tokens a player can keep is 10

        Returns:
            bool: true if the player has too many tokens
            """

        return sum(self.tokens.get_tokens()) > 10

    def get_id(self) -> int:
        """Get the id of the player

        Returns:
            int: player id
            """

        return self.playerId

    def get_victory_points(self) -> VictoryPoint:
        """Get the victory points of the player

        Returns:
            VictoryPoint: victory points of the player
            """

        return self.victoryPoints
