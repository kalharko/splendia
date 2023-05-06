from dataclasses import dataclass

from model.bank_controller import BankController
from model.patron_controller import PatronController
from model.player_controller import PlayerController
from model.shop_controller import ShopController
from model.token_array import TokenArray
from utils.logger import Logger
from model.player import Player


@dataclass
class GameManager():
    """This class is used to manage the game.
    It contains the controllers of the game and methods to interact with them.

    Attributes:
        _bankController (BankController): The bank controller.
        _patronController (PatronController): The patron controller.
        _playerController (PlayerController): The player controller.
        _shopController (ShopController): The shop controller.
        nbPlayer (int): The number of players.
        currentPlayer (int): The id of the current player.
        firstPlayerId (int): The id of the first player.
        userId (int): The id of the user.
        """

    _bankController: BankController
    _patronController: PatronController
    _playerController: PlayerController
    _shopController: ShopController
    nbPlayer: int
    currentPlayer: int
    firstPlayerId: int
    userId: int

    def __init__(self, nbPlayer=2) -> None:
        """This method initializes the game manager. It creates the controllers of the game.

        Args:
            nbPlayer (int): The number of players.
            """
        self.initialize_game(nbPlayer)

    def initialize_game(self, nbPlayer):
        self._bankController = BankController(nbPlayer)
        self._patronController = PatronController(nbPlayer)
        self._playerController = PlayerController(
            nbPlayer, observer=self._patronController)
        self._shopController = ShopController()
        self.currentPlayer = 0
        self.nbPlayer = nbPlayer
        self.userId = 0
        self.firstPlayerId = 0

    def gather_ia_board_state(self, nb_players=2) -> dict or None:
        """This method gathers the board state for the IA.

        Args:
            nb_players (int): The number of players.

        Returns:
            dict: The board state.
            """
        if nb_players == 2:
            dictionary = {
                'player1': {
                    'object': self._playerController.players[0],
                    # pad with none to have 20 reserved cards
                    'cards': self._playerController.players[0].hand.cards + [None] * (20 - self._playerController.players[0].hand.get_size()),
                    'tokens': self._playerController.players[0].tokens.get_tokens(),
                    # pad with none to have 3 reserved cards
                    'reserved': self._playerController.players[0].reserved.cards + [None] * (3 - self._playerController.players[0].reserved.get_size()),

                    'nobles': self._playerController.players[0].patrons
                },
                'player2': {
                    'object': self._playerController.players[1],
                    # pad with none to have 20 reserved cards
                    'cards': self._playerController.players[1].hand.cards + [None] * (20 - self._playerController.players[1].hand.get_size()),
                    'tokens': self._playerController.players[1].tokens.get_tokens(),
                    # pad with none to have 3 reserved cards
                    'reserved': self._playerController.players[1].reserved.cards + [None] * (3 - self._playerController.players[1].reserved.get_size()),
                    'nobles': self._playerController.players[1].patrons
                },
                'shop': {
                    'rank1':{
                        'cards': self._shopController.ranks[0].hand.cards,
                        'size': self._shopController.ranks[0].deck.get_size()
                    },
                    'rank2':{
                        'cards': self._shopController.ranks[1].hand.cards,
                        'size': self._shopController.ranks[1].deck.get_size()
                    },
                    'rank3':{
                        'cards': self._shopController.ranks[2].hand.cards,
                        'size': self._shopController.ranks[2].deck.get_size()
                    },
                
                    'nobles': self._patronController.patrons,
                    'tokens': self._bankController.bank
                },
            }
            return dictionary
        else:
            return None

    def gather_cli_board_state(self) -> dict:
        """This method gathers the board state for the CLI.

        Returns:
            dict: The board state.
            """

        out = {}
        out['cpu1-vp'] = self._playerController.players[0].victoryPoints.value
        out['cpu1-bonus'] = self._playerController.players[0].hand.compute_hand_bonuses()
        out['cpu1-tokens'] = self._playerController.players[0].tokens
        out['cpu1-nbReserved'] = self._playerController.players[0].reserved.get_size()

        out['cpu2-vp'] = self._playerController.players[1].victoryPoints.value
        out['cpu2-bonus'] = self._playerController.players[1].hand.compute_hand_bonuses()
        out['cpu2-tokens'] = self._playerController.players[1].tokens
        out['cpu2-nbReserved'] = self._playerController.players[1].reserved.get_size()

        out['cpu3-vp'] = self._playerController.players[2].victoryPoints.value
        out['cpu3-bonus'] = self._playerController.players[2].hand.compute_hand_bonuses()
        out['cpu3-tokens'] = self._playerController.players[2].tokens
        out['cpu3-nbReserved'] = self._playerController.players[2].reserved.get_size()

        out['player-vp'] = self._playerController.players[3].victoryPoints.value
        out['player-bonus'] = self._playerController.players[3].hand.compute_hand_bonuses()
        out['player-tokens'] = self._playerController.players[3].tokens
        out['player-nbReserved'] = self._playerController.players[3].reserved.get_size()
        out['player-reserved'] = []
        for i in range(out['player-nbReserved']):
            out['player-reserved'].append([
                self._playerController.players[3].reserved.cards[i].price,
                self._playerController.players[3].reserved.cards[i].bonus,
                self._playerController.players[3].reserved.cards[i].victoryPoint])

        out['bank'] = self._bankController.bank.get_tokens()
        out['patrons'] = [x.requirements for x in self._patronController.patrons]

        for y, yy in zip(range(3), [2, 1, 0]):
            for x in range(4):
                out[f'shop{x}{y}-pv'] = self._shopController.ranks[yy].hand.cards[x].victoryPoint.value
                out[f'shop{x}{y}-bonus'] = self._shopController.ranks[yy].hand.cards[x].bonus
                out[f'shop{x}{y}-price'] = self._shopController.ranks[yy].hand.cards[x].price

        return out

    def gather_api_board_state(self) -> dict:
        """Returns the board state in a dictionnary that is in the following format:
        - shop: it corresponds to a list of "rank" objets. A rank contains visible cards and the number of cards in the deck associated to the rank
        - humainPlayer: it contains a token list, a bonus list, the victory points of the player and the reserved cards of the player
        - CPUS: it corresponds to a list of "CPU" objets. A CPU contains a token list, a bonus list, the victory points of the CPU and the number of reserved cards of the player
        - bank: it corresponds to a token list
        - patrons: it corresponds to a list of patrons
        - gameState: it contains a boolean stating if the player has to reject tokens and a list containing the id of the players who won (the list is empty if no one has won)
        This function is used for the responses of the API

        Returns:
            dict: board state used for the responses of the API
        """

        board_state = {}
        board_state['shop'] = self._shopController.gather_shop_information_api_board_state()
        board_state['humanPlayer'] = self._playerController.gather_human_player_information_api_board_state()
        board_state['CPUS'] = self._playerController.gather_cpu_players_information_api_board_state()
        board_state['bank'] = self._bankController.gather_bank_information_api_board_state()
        board_state['patrons'] = self._patronController.gather_patrons_information_api_board_state()
        board_state['gameState'] = {
            'humanPlayerTooManyTokens': self._playerController.check_human_player_too_many_tokens(),
            'winners': self._playerController.gather_winner_information_api_board_state()
        }

        return board_state

    def launch_game(self, nbPlayer: int) -> None:
        """This method launches the game.

        Args:
            nbPlayer (int): The number of players.
            """

        self.initialize_game(nbPlayer)

    def next_player(self) -> None:
        """This method changes the current player.

        """

        self.currentPlayer += 1

        if self.currentPlayer >= self.nbPlayer:
            self.currentPlayer = 0

    def buy_card(self, cardId: int) -> None:
        """This method buys a card.

        Args:
            cardId (int): The card id.
            """

        # print('bank token before', self.bankController.bank.get_tokens())
        if self._shopController.has_card(cardId):
            if err := self._playerController.buy_shop_card(self.currentPlayer, cardId, self._shopController, self._bankController):
                Logger().log(0, err, 'GameManager buy_card')
                return err
        elif err := self._playerController.buy_reserved_card(self.currentPlayer, cardId, self._bankController):
            Logger().log(0, err, 'GameManager buy_card')
            return err
        # print('bank token after', self.bankController.bank.get_tokens())

        if err is None:
            self.next_player()

    def reserve_card(self, cardId: int) -> None:
        """This method reserves a card.

        Args:
            cardId (int): The card id.
            """

        if err := self._playerController.reserve_card(self.currentPlayer, cardId, self._shopController, self._bankController):
            Logger().log(0, err, 'GameManager reserve_card')
            return err

        if err is None:
            self.next_player()

    def reserve_pile_card(self, pile_level: int) -> None:
        """This method reserves a card from the pile.

        Args:
            pile_level (int): The pile level.
            """
        if err := self._playerController.reserve_pile_card(self.currentPlayer, pile_level, self._shopController):
            Logger().log(0, err, 'GameManager reserve_pile_card')
            return err

        if err is None:
            self.next_player()

    def take_token(self, tokens: TokenArray) -> None:
        """This method takes tokens.

        Args:
            tokens (TokenArray): The tokens.
            """

        if err := self._playerController.take_tokens(self.currentPlayer, tokens, self._bankController):

            Logger().log(0, err, 'GameManager take_token')
            return err

        if err is None:
            self.next_player()

    def pass_turn(self):
        """This method passes the turn.

            """
        self.next_player()

    def is_last_turn(self) -> bool:
        """This method checks if it is the last turn.

        Returns:
            bool: True if it is the last turn, False otherwise.
            """
        for player in self._playerController.players:
            if player.victoryPoints.value >= 15:
                return True
        return False

    def cpu_turn(self) -> None:
        """This method plays the turn for the cpu.

        """
        # TODO: call ai
        pass

    def get_player_victory_point(self, player_id: int) -> int:
        """This method returns the victory points of a player.

        Args:
            player_id (int): The player id.

        Returns:
            int: The victory points of the player.
            """
        return self._playerController.players[player_id].victoryPoints.value

    def get_current_player(self) -> Player:
        """This method returns the current player.

        Returns:
            Player: The current player.
            """

        return self._playerController.players[self.currentPlayer]

    def get_patron_controller(self) -> PatronController:
        """Getter for the game manager's patron controller

        Returns:
            PatronController: The game manager's patron controller
            """
        return self._patronController

    def get_player_controller(self) -> PlayerController:
        """Getter for the game manager's player controller

        Returns:
            PlayerController: The game manager's player controller
            """
        return self._playerController

    def get_shop_controller(self) -> ShopController:
        """Getter for the game manager's shop controller

        Returns:
            ShopController: The game manager's shop controller
            """
        return self._shopController

    def get_bank_controller(self) -> BankController:
        """Getter for the game manager's bank controller

        Returns:
            BankController: The game manager's bank controller
            """
        return self._bankController
