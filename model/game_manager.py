from dataclasses import dataclass
from random import randint

from model.bank_controller import BankController
from model.patron_controller import PatronController
from model.player_controller import PlayerController
from model.shop_controller import ShopController
from model.token_array import TokenArray
from model.utils.logger import Logger
from model.player import Player


@dataclass
class GameManager():
    _bankController: BankController
    _patronController: PatronController
    _playerController: PlayerController
    _shopController: ShopController
    nbPlayer: int
    currentPlayer: int
    firstPlayerId: int
    userId: int

    def __init__(self, nbPlayer=2) -> None:
        self._bankController = BankController(nbPlayer)
        self._patronController = PatronController(nbPlayer)
        self._playerController = PlayerController(nbPlayer, observer=self._patronController)
        self._shopController = ShopController()
        self.currentPlayer = 0
        self.nbPlayer = nbPlayer
        self.userId = 0
        self.firstPlayerId = 0

    def gather_ia_board_state(self, nb_players=2) -> None:
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
                    'rank1_cards': self._shopController.ranks[0].hand.cards,
                    'rank2_cards': self._shopController.ranks[1].hand.cards,
                    'rank3_cards': self._shopController.ranks[2].hand.cards,
                    'rank1_size': self._shopController.ranks[0].deck.get_size(),
                    'rank2_size': self._shopController.ranks[1].deck.get_size(),
                    'rank3_size': self._shopController.ranks[2].deck.get_size(),
                    'nobles': self._patronController.patrons,
                    'tokens': self._bankController.bank,
                },
                }
            return dictionary

    def gather_cli_board_state(self) -> dict:
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

    def launch_game(self, nbPlayer: int) -> None:


        self.nbPlayer = nbPlayer
        # self.firstPlayerId = randint(0, nbPlayer-1)
        self.firstPlayerId = 0
        self.currentPlayer = self.firstPlayerId
        self.userId = 0

    def next_player(self) -> None:
        self.currentPlayer += 1

        if self.currentPlayer >= self.nbPlayer:
            self.currentPlayer = 0

    def buy_card(self, cardId: int) -> None:
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
        if err := self._playerController.reserve_card(self.currentPlayer, cardId, self._shopController, self._bankController):
            Logger().log(0, err, 'GameManager reserve_card')
            return err

        if err is None:
            self.next_player()

    def reserve_pile_card(self, pile_level: int) -> None:
        if err := self._playerController.reserve_pile_card(self.currentPlayer, pile_level,self._shopController):
            Logger().log(0, err, 'GameManager reserve_pile_card')
            return err

        if err is None:
            self.next_player()

    def take_token(self, tokens: TokenArray) -> None:
        if err := self._playerController.take_tokens(self.currentPlayer, tokens, self._bankController):

            Logger().log(0, err, 'GameManager take_token')
            return err

        if err is None:
            self.next_player()

    def pass_turn(self):
        self.next_player()

    def is_last_turn(self) -> bool:
        finished = False
        for player in self._playerController.players:
            if player.victoryPoints.value >= 15:
                finished = True
            return finished
        return finished

    def cpu_turn(self) -> None:
        # TODO: call ai
        pass

    def get_player_victory_point(self, player_id : int) -> int:
        return self._playerController.players[player_id].victoryPoints.value
    def get_current_player(self) -> Player:
        return self._playerController.players[self.currentPlayer]
