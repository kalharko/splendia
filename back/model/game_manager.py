from dataclasses import dataclass

from model.bank_controller import BankController
from model.patron_controller import PatronController
from model.player_controller import PlayerController
from model.shop_controller import ShopController
from model.token_array import TokenArray
from utils.logger import Logger
from model.player import Player
from ai.model_ppo import PPO
import random
import numpy
import pickle
from utils.exception import InvalidNbPlayer


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
    logs: list[str]

    def __init__(self, nbPlayer=2) -> None:
        """This method initializes the game manager. It creates the controllers of the game.

        Args:
            nbPlayer (int): The number of players.
            """
        assert isinstance(nbPlayer, int)

        self.initialize_game(nbPlayer)

    def initialize_game(self, nbPlayer):
        """This method initializes the game manager. It creates the controllers of the game.

        Args:
            nbPlayer (int): The number of players.
            """
        assert isinstance(nbPlayer, int)

        self._bankController = BankController(nbPlayer)
        self._patronController = PatronController(nbPlayer)
        self._playerController = PlayerController(
            nbPlayer, observer=self._patronController)
        self._shopController = ShopController()
        self.currentPlayer = 0
        self.nbPlayer = nbPlayer
        self.userId = 0
        self.randomize_first_player()
        self.cpu_Id = 1
        self.initialize_cpu()
        self.logs = []

    def initialize_cpu(self):
        """This method initializes the cpu.
            """

        state_dim = 88

        # action space dimension

        action_dim = 66
        update_timestep = 1 * 10  # update policy every n timesteps
        K_epochs = 80  # update policy for K epochs in one PPO update

        eps_clip = 0.2  # clip parameter for PPO
        gamma = 0.99  # discount factor

        lr_actor = 0.0005  # learning rate for actor network
        lr_critic = 0.0002  # learning rate for critic network

        random_seed = 0  # set random seed if required (0 = no random seed)
        self.cpu = PPO(state_dim, action_dim, lr_actor, lr_critic, gamma, K_epochs, eps_clip,
                       False,
                       0, self.cpu_Id + 1)
        self.cpu.load('Champion/champion_0.pth')

    def randomize_first_player(self):
        """This method randomizes the first player."""
        # get a random number between 0 and nbPlayer
        self.firstPlayerId = random.randint(0, self.nbPlayer - 1)
        self.currentPlayer = self.firstPlayerId

    def gather_ia_board_state(self, nb_players=2) -> dict or None:
        """This method gathers the board state for the IA.

        Args:
            nb_players (int): The number of players.

        Returns:
            dict: The board state.
            """
        assert isinstance(nb_players, int)

        if nb_players == 2:
            dictionary = {
                'player1': {
                    'object': self._playerController.players[0],
                    # pad with none to have 20 reserved cards
                    'cards': self._playerController.players[0].hand.cards + [None] * (
                        20 - self._playerController.players[0].hand.get_size()),
                    'tokens': self._playerController.players[0].tokens.get_tokens(),
                    # pad with none to have 3 reserved cards
                    'reserved': self._playerController.players[0].reserved.cards + [None] * (
                        3 - self._playerController.players[0].reserved.get_size()),

                    'nobles': self._playerController.players[0].patrons
                },
                'player2': {
                    'object': self._playerController.players[1],
                    # pad with none to have 20 reserved cards
                    'cards': self._playerController.players[1].hand.cards + [None] * (
                        20 - self._playerController.players[1].hand.get_size()),
                    'tokens': self._playerController.players[1].tokens.get_tokens(),
                    # pad with none to have 3 reserved cards
                    'reserved': self._playerController.players[1].reserved.cards + [None] * (
                        3 - self._playerController.players[1].reserved.get_size()),
                    'nobles': self._playerController.players[1].patrons
                },
                'shop': {
                    'rank1_cards': self._shopController.ranks[0].hand.cards,
                    'rank2_cards': self._shopController.ranks[1].hand.cards,
                    'rank3_cards': self._shopController.ranks[2].hand.cards,
                    'rank1_size': self._shopController.ranks[0].deck.get_size(),
                    'rank2_size': self._shopController.ranks[1].deck.get_size(),
                    'rank3_size': self._shopController.ranks[2].deck.get_size(),
                    'nobles': self._patronController.patrons,
                    'tokens': self._bankController.bank,
                },

                'nobles': self._patronController.patrons,
                'tokens': self._bankController.bank
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
        board_state['logs'] = self.logs[::-1]

        return board_state

    def launch_game(self, nbPlayer: int) -> None:
        """This method launches the game.

        Args:
            nbPlayer (int): The number of players.
            """
        assert isinstance(nbPlayer, int)

        if (nbPlayer < 2 or nbPlayer > 4):
            raise InvalidNbPlayer(nbPlayer)
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
        assert isinstance(cardId, int)

        # print('bank token before', self.bankController.bank.get_tokens())
        if self._shopController.has_card(cardId):
            if err := self._playerController.buy_shop_card(self.currentPlayer, cardId, self._shopController,
                                                           self._bankController):
                Logger().log(0, err, 'GameManager buy_card')
                return err
        elif err := self._playerController.buy_reserved_card(self.currentPlayer, cardId, self._bankController):
            Logger().log(0, err, 'GameManager buy_card')
            return err
        # print('bank token after', self.bankController.bank.get_tokens())

        if err is None:
            self.append_log("buys card " + str(cardId))
            self.next_player()

    def reserve_card(self, cardId: int) -> None:
        """This method reserves a card.

        Args:
            cardId (int): The card id.
            """
        assert isinstance(cardId, int)

        if err := self._playerController.reserve_card(self.currentPlayer, cardId, self._shopController,
                                                      self._bankController):
            Logger().log(0, err, 'GameManager reserve_card')
            return err

        if err is None:
            self.append_log("reserves card " + str(cardId))
            self.next_player()

    def reserve_pile_card(self, pile_level: int) -> None:
        """This method reserves a card from the pile.

        Args:
            pile_level (int): The pile level.
            """
        assert isinstance(pile_level, int)

        if err := self._playerController.reserve_pile_card(self.currentPlayer, pile_level, self._shopController):
            Logger().log(0, err, 'GameManager reserve_pile_card')
            return err

        if err is None:
            self.append_log("reserves from pile " + str(pile_level))
            self.next_player()

    def take_token(self, tokens: TokenArray) -> None:
        """This method takes tokens.

        Args:
            tokens (TokenArray): The tokens.
            """
        assert isinstance(tokens, TokenArray)

        if err := self._playerController.take_tokens(self.currentPlayer, tokens, self._bankController):
            Logger().log(0, err, 'GameManager take_token')
            return err

        if err is None:
            self.append_log("takes tokens " + str(tokens))
            self.next_player()

    def append_log(self, line: str) -> None:
        if self.currentPlayer == self.userId:
            line = "Player " + line
        else:
            line = "CPU#" + str(self.currentPlayer) + " " + line
        self.logs.append(line)
        if len(self.logs) > 10:
            self.logs.pop(0)

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

    def cpu_turn(self) -> str:
        """This method plays the turn for the cpu.
            """

        playerId = self.cpu_Id
        state = self.gather_ia_board_state()
        player_string = 'player' + str(playerId + 1)
        player2 = (playerId + 1) % 3
        opponent_string = 'player' + str(player2)

        obs = self.from_board_state_to_obs(
            opponent_string, player_string, state)
        # save it as a pickle
        with open('obs.pkl', 'wb') as f:
            pickle.dump(state, f)
        obs = self.normalize_obs(obs)

        ai_action = self.cpu.select_action(obs)

        string_action = self.apply_action(ai_action)
        self.append_log(string_action)
        return string_action

    def from_board_state_to_obs(self, opponent_string, player_string, state):
        """TODO: documentation
            """

        obs = numpy.zeros(88)
        obs[0:6] = state[player_string]['tokens']
        # if the length of the list smaller than 20, we padd with 90
        list_of_cards = [
            card.cardId for card in state[player_string]['cards'] if card is not None]
        if len(list_of_cards) < 20:
            for i in range(20 - len(list_of_cards)):
                list_of_cards.append(90)
        obs[6:26] = list_of_cards
        # same for nobles, if the length of the list smaller than 5, we padd with 10
        list_of_nobles = [
            patron.patron_id for patron in state[player_string]['nobles']]
        if len(list_of_nobles) < 5:
            for i in range(5 - len(list_of_nobles)):
                list_of_nobles.append(10)
        obs[26:31] = list_of_nobles
        # we save the reserved cards in a list, if the card is None, we padd with 90
        self.reserved_cards = [
            card.cardId for card in state[player_string]['reserved'] if card is not None]
        if len(self.reserved_cards) < 3:
            for i in range(3 - len(self.reserved_cards)):
                self.reserved_cards.append(90)
        # same for reserved cards, if the length of the list smaller than 3, we padd with 90
        list_of_reserved = [
            card.cardId for card in state[player_string]['reserved'] if card is not None]
        if len(list_of_reserved) < 3:
            for i in range(3 - len(list_of_reserved)):
                list_of_reserved.append(90)
        obs[31:34] = list_of_reserved
        obs[34:40] = state[opponent_string]['tokens']
        # same for player 2
        list_of_cards = [
            card.cardId for card in state[opponent_string]['cards'] if card is not None]
        if len(list_of_cards) < 20:
            for i in range(20 - len(list_of_cards)):
                list_of_cards.append(90)
        obs[40:60] = list_of_cards
        list_of_nobles = [
            patron.patron_id for patron in state[opponent_string]['nobles']]
        if len(list_of_nobles) < 5:
            for i in range(5 - len(list_of_nobles)):
                list_of_nobles.append(10)
        obs[60:65] = list_of_nobles
        list_of_reserved = [
            card.cardId for card in state[opponent_string]['reserved'] if card is not None]
        if len(list_of_reserved) < 3:
            for i in range(3 - len(list_of_reserved)):
                list_of_reserved.append(90)
        obs[65:68] = list_of_reserved
        # same for shop
        self.shop1_cards = state['shop']['rank1_cards']
        list_of_cards_rank1 = [
            card.cardId for card in state['shop']['rank1_cards']]
        if len(list_of_cards_rank1) < 4:
            for i in range(4 - len(list_of_cards_rank1)):
                list_of_cards_rank1.append(90)
        obs[68:72] = list_of_cards_rank1
        self.shop2_cards = state['shop']['rank2_cards']
        list_of_cards_rank2 = [
            card.cardId for card in state['shop']['rank2_cards']]
        if len(list_of_cards_rank2) < 4:
            for i in range(4 - len(list_of_cards_rank2)):
                list_of_cards_rank2.append(90)
        obs[72:76] = list_of_cards_rank2
        self.shop3_cards = state['shop']['rank3_cards']
        list_of_cards_rank3 = [
            card.cardId for card in state['shop']['rank3_cards']]
        if len(list_of_cards_rank3) < 4:
            for i in range(4 - len(list_of_cards_rank3)):
                list_of_cards_rank3.append(90)
        obs[76:80] = list_of_cards_rank3
        list_of_nobles = [
            patron.patron_id for patron in state['shop']['nobles']]
        if len(list_of_nobles) < 5:
            for i in range(5 - len(list_of_nobles)):
                list_of_nobles.append(10)
        obs[80:85] = list_of_nobles
        obs[85] = state['shop']['rank1_size']
        obs[86] = state['shop']['rank2_size']
        obs[87] = state['shop']['rank3_size']
        return obs

    def normalize_obs(self, obs):
        """
                Player 1 state:
                5 tokens: 0-4
                1 gold token: 5
                20 player cards: 6-25
                5 noble cards: 26-30
                3 reserved cards: 31-33

                Player 2 state:
                5 tokens: 34-38
                1 gold token: 39
                20 player cards: 40-59
                5 noble cards: 60-64
                3 reserved cards: 65-67

                Shop state:
                12 cards: 68-79
                5 noble cards: 80-84
                1 tier 1 number of cards: 85
                1 tier 2 number of cards: 86
                1 tier 3 number of cards: 87

                """
        obs[0:6] = obs[0:6] / 10
        obs[6:26] = obs[6:26] / 90
        obs[26:31] = obs[26:31] / 10
        obs[31:34] = obs[31:34] / 90

        obs[34:40] = obs[34:40] / 10
        obs[40:60] = obs[40:60] / 90
        obs[60:65] = obs[60:65] / 10
        obs[65:68] = obs[65:68] / 90

        obs[68:80] = obs[68:80] / 90
        obs[80:85] = obs[80:85] / 10
        obs[85:88] = obs[85:88] / 30

        return obs

    def get_player_victory_point(self, playerId: int) -> int:
        """This method returns the victory points of a player.

        Args:
            playerId (int): The player id.

        Returns:
            int: The victory points of the player.
            """
        assert isinstance(playerId, int)

        return self._playerController.players[playerId].victoryPoints.value

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

    def apply_action(self, action):
        """TODO: Documentation
            """
        assert isinstance(action, int)

        string_action = ""
        # print the action done
        # print('action done : ', action)
        if action == 0:
            # take [1,1,1,0,0,0] tokens
            self.take_token(TokenArray([1, 1, 1, 0, 0, 0]))
            string_action = "The cpu took [1,1,1,0,0,0] tokens"
        elif action == 1:
            # take [1,1,0,1,0,0] tokens
            self.take_token(TokenArray([1, 1, 0, 1, 0, 0]))
            string_action = "The cpu took [1,1,0,1,0,0] tokens"
        elif action == 2:
            # take [1,1,0,0,1,0] tokens
            self.take_token(TokenArray([1, 1, 0, 0, 1, 0]))
            string_action = "The cpu took [1,1,0,0,1,0] tokens"
        elif action == 3:
            # take [1,0,1,1,0,0] tokens
            self.take_token(TokenArray([1, 0, 1, 1, 0, 0]))
            string_action = "The cpu took [1,0,1,1,0,0] tokens"
        elif action == 4:
            # take [1,0,1,0,1,0] tokens
            self.take_token(TokenArray([1, 0, 1, 0, 1, 0]))
            string_action = "The cpu took [1,0,1,0,1,0] tokens"
        elif action == 5:
            # take [1,0,0,1,1,0] tokens
            self.take_token(TokenArray([1, 0, 0, 1, 1, 0]))
            string_action = "The cpu took [1,0,0,1,1,0] tokens"
        elif action == 6:
            # take [0,1,1,1,0,0] tokens
            self.take_token(TokenArray([0, 1, 1, 1, 0, 0]))
            string_action = "The cpu took [0,1,1,1,0,0] tokens"
        elif action == 7:
            # take [0,1,1,0,1,0] tokens
            self.take_token(TokenArray([0, 1, 1, 0, 1, 0]))
            string_action = "The cpu took [0,1,1,0,1,0] tokens"
        elif action == 8:
            # take [0,1,0,1,1,0] tokens
            self.take_token(TokenArray([0, 1, 0, 1, 1, 0]))
            string_action = "The cpu took [0,1,0,1,1,0] tokens"
        elif action == 9:
            # take [0,0,1,1,1,0] tokens
            self.take_token(TokenArray([0, 0, 1, 1, 1, 0]))
            string_action = "The cpu took [0,0,1,1,1,0] tokens"
        elif action == 10:
            self.take_token(TokenArray([2, 0, 0, 0, 0, 0]))
            string_action = "The cpu took [2,0,0,0,0,0] tokens"
        elif action == 11:
            self.take_token(TokenArray([0, 2, 0, 0, 0, 0]))
            string_action = "The cpu took [0,2,0,0,0,0] tokens"
        elif action == 12:
            self.take_token(TokenArray([0, 0, 2, 0, 0, 0]))
            string_action = "The cpu took [0,0,2,0,0,0] tokens"
        elif action == 13:
            self.take_token(TokenArray([0, 0, 0, 2, 0, 0]))
            string_action = "The cpu took [0,0,0,2,0,0] tokens"
        elif action == 14:
            self.take_token(TokenArray([0, 0, 0, 0, 2, 0]))
            string_action = "The cpu took [0,0,0,0,2,0] tokens"
        elif action == 15:
            string_action = "The cpu bought a card from shop 1, id : " + \
                str(self.shop1_cards[0].cardId)
            self.buy_card(self.shop1_cards[0].cardId)
        elif action == 16:
            string_action = "The cpu bought a card from shop 1, id : " + \
                str(self.shop1_cards[1].cardId)
            self.buy_card(self.shop1_cards[1].cardId)
        elif action == 17:
            string_action = "The cpu bought a card from shop 1, id : " + \
                str(self.shop1_cards[2].cardId)
            self.buy_card(self.shop1_cards[2].cardId)
        elif action == 18:
            string_action = "The cpu bought a card from shop 1, id : " + \
                str(self.shop1_cards[3].cardId)
            self.buy_card(self.shop1_cards[3].cardId)
        elif action == 19:
            string_action = "The cpu bought a card from shop 2, id : " + \
                str(self.shop2_cards[0].cardId)
            self.buy_card(self.shop2_cards[0].cardId)
        elif action == 20:
            string_action = "The cpu bought a card from shop 2, id : " + \
                str(self.shop2_cards[1].cardId)
            self.buy_card(self.shop2_cards[1].cardId)
        elif action == 21:
            string_action = "The cpu bought a card from shop 2, id : " + \
                str(self.shop2_cards[2].cardId)
            self.buy_card(self.shop2_cards[2].cardId)
        elif action == 22:
            string_action = "The cpu bought a card from shop 2, id : " + \
                str(self.shop2_cards[3].cardId)
            self.buy_card(self.shop2_cards[3].cardId)
        elif action == 23:
            string_action = "The cpu bought a card from shop 3, id : " + \
                str(self.shop3_cards[0].cardId)
            self.buy_card(self.shop3_cards[0].cardId)
        elif action == 24:
            string_action = "The cpu bought a card from shop 3, id : " + \
                str(self.shop3_cards[1].cardId)
            self.buy_card(self.shop3_cards[1].cardId)
        elif action == 25:
            string_action = "The cpu bought a card from shop 3, id : " + \
                str(self.shop3_cards[2].cardId)
            self.buy_card(self.shop3_cards[2].cardId)
        elif action == 26:
            string_action = "The cpu bought a card from shop 3, id : " + \
                str(self.shop3_cards[3].cardId)
            self.buy_card(self.shop3_cards[3].cardId)
        elif action == 27:
            string_action = "The cpu bought reserved card, id : " + \
                str(self.reserved_cards[0])
            self.buy_card(self.reserved_cards[0])
        elif action == 28:
            string_action = "The cpu bought reserved card, id : " + \
                str(self.reserved_cards[1])
            self.buy_card(self.reserved_cards[1])

        elif action == 29:
            string_action = "The cpu bought reserved card , id : " + \
                str(self.reserved_cards[2])
            self.buy_card(self.reserved_cards[2])
        elif action == 30:
            string_action = "The cpu reserved a card from shop 1, id : " + \
                str(self.shop1_cards[0].cardId)
            self.reserve_card(self.shop1_cards[0].cardId)
        elif action == 31:
            string_action = "The cpu reserved a card from shop 1, id : " + \
                str(self.shop1_cards[1].cardId)
            self.reserve_card(self.shop1_cards[1].cardId)
        elif action == 32:
            string_action = "The cpu reserved a card from shop 1, id : " + \
                str(self.shop1_cards[2].cardId)
            self.reserve_card(self.shop1_cards[2].cardId)
        elif action == 33:
            string_action = "The cpu reserved a card from shop 1, id : " + \
                str(self.shop1_cards[3].cardId)
            self.reserve_card(self.shop1_cards[3].cardId)
        elif action == 34:
            string_action = "The cpu reserved a card from shop 2, id : " + \
                str(self.shop2_cards[0].cardId)
            self.reserve_card(self.shop2_cards[0].cardId)
        elif action == 35:
            string_action = "The cpu reserved a card from shop 2, id : " + \
                str(self.shop2_cards[1].cardId)
            self.reserve_card(self.shop2_cards[1].cardId)
        elif action == 36:
            string_action = "The cpu reserved a card from shop 2, id : " + \
                str(self.shop2_cards[2].cardId)
            self.reserve_card(self.shop2_cards[2].cardId)
        elif action == 37:
            string_action = "The cpu reserved a card from shop 2, id : " + \
                str(self.shop2_cards[3].cardId)
            self.reserve_card(self.shop2_cards[3].cardId)
        elif action == 38:
            string_action = "The cpu reserved a card from shop 3, id : " + \
                str(self.shop3_cards[0].cardId)
            self.reserve_card(self.shop3_cards[0].cardId)
        elif action == 39:
            string_action = "The cpu reserved a card from shop 3, id : " + \
                str(self.shop3_cards[1].cardId)
            self.reserve_card(self.shop3_cards[1].cardId)
        elif action == 40:
            string_action = "The cpu reserved a card from shop 3, id : " + \
                str(self.shop3_cards[2].cardId)
            self.reserve_card(self.shop3_cards[2].cardId)
        elif action == 41:
            string_action = "The cpu reserved a card from shop 3, id : " + \
                str(self.shop3_cards[3].cardId)
            self.reserve_card(self.shop3_cards[3].cardId)
        elif action == 42:
            self.reserve_pile_card(0)
            string_action = "The cpu reserved a card from pile 1"
        elif action == 43:
            self.reserve_pile_card(1)
            string_action = "The cpu reserved a card from pile 2"
        elif action == 44:
            self.reserve_pile_card(2)
            string_action = "The cpu reserved a card from pile 3"
        elif action == 45:
            self.take_token(TokenArray([1, 0, 0, 0, 0, 0]))
            string_action = "The cpu took a white token"
        elif action == 46:
            self.take_token(TokenArray([0, 1, 0, 0, 0, 0]))
            string_action = "The cpu took a blue token"
        elif action == 47:
            self.take_token(TokenArray([0, 0, 1, 0, 0, 0]))
            string_action = "The cpu took a green token"
        elif action == 48:
            self.take_token(TokenArray([0, 0, 0, 1, 0, 0]))
            string_action = "The cpu took a red token"
        elif action == 49:
            self.take_token(TokenArray([0, 0, 0, 0, 1, 0]))
            string_action = "The cpu took a black token"
        elif action == 50:
            self.take_token(TokenArray([1, 1, 0, 0, 0, 0]))
            string_action = "The cpu took [white, blue] tokens"
        elif action == 51:
            self.take_token(TokenArray([1, 0, 1, 0, 0, 0]))
            string_action = "The cpu took [white, green] tokens"
        elif action == 52:
            self.take_token(TokenArray([1, 0, 0, 1, 0, 0]))
            string_action = "The cpu took [white, red] tokens"
        elif action == 53:
            self.take_token(TokenArray([1, 0, 0, 0, 1, 0]))
            string_action = "The cpu took [white, black] tokens"
        elif action == 54:
            self.take_token(TokenArray([0, 1, 1, 0, 0, 0]))
            string_action = "The cpu took [blue, green] tokens"
        elif action == 55:
            self.take_token(TokenArray([0, 1, 0, 1, 0, 0]))
            string_action = "The cpu took [blue, red] tokens"
        elif action == 56:
            self.take_token(TokenArray([0, 1, 0, 0, 1, 0]))
            string_action = "The cpu took [blue, black] tokens"
        elif action == 57:
            self.take_token(TokenArray([0, 0, 1, 1, 0, 0]))
            string_action = "The cpu took [green, red] tokens"
        elif action == 58:
            self.take_token(TokenArray([0, 0, 1, 0, 1, 0]))
            string_action = "The cpu took [green, black] tokens"
        elif action == 59:
            self.take_token(TokenArray([0, 0, 0, 1, 1, 0]))
            string_action = "The cpu took [red, black] tokens"
        elif action == 60:
            self.take_token(TokenArray([2, 0, 0, 0, 0, 0]))
            string_action = "The cpu took 2 white tokens"
        elif action == 61:
            self.take_token(TokenArray([0, 2, 0, 0, 0, 0]))
            string_action = "The cpu took 2 blue tokens"
        elif action == 62:
            self.take_token(TokenArray([0, 0, 2, 0, 0, 0]))
            string_action = "The cpu took 2 green tokens"
        elif action == 63:
            self.take_token(TokenArray([0, 0, 0, 2, 0, 0]))
            string_action = "The cpu took 2 red tokens"
        elif action == 64:
            self.take_token(TokenArray([0, 0, 0, 0, 2, 0]))
            string_action = "The cpu took 2 black tokens"
        elif action == 65:
            self.pass_turn()
            string_action = "The cpu passed his turn"
        return string_action
