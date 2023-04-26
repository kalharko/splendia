from dataclasses import dataclass
from random import randint

from model.bank_controller import BankController
from model.patron_controller import PatronController
from model.player_controller import PlayerController
from model.shop_controller import ShopController
from model.token_array import TokenArray
from model.utils.logger import Logger


@dataclass
class GameManager():
    bankController: BankController
    patronController: PatronController
    playerController: PlayerController
    shopController: ShopController
    nbPlayer: int
    currentPlayer: int
    firstPlayerId: int
    userId: int

    def __init__(self, nbPlayer=2) -> None:
        self.bankController = BankController(nbPlayer)
        self.patronController = PatronController()
        self.playerController = PlayerController()
        self.shopController = ShopController()
        self.currentPlayer = 0
        self.userId = 0
        self.firstPlayerId = 0

    def gather_ia_board_state(self, nb_players=2) -> None:
        if nb_players == 2:

            dictionnary = {
                'player1': {
                    'cards': self.playerController.players[0].hand.cards,
                    'tokens': self.playerController.players[0].tokens.get_tokens(),
                    'reserved': self.playerController.players[0].reserved.cards,
                    'nobles': self.playerController.players[0].patrons
                },
                'player2': {
                    'cards': self.playerController.players[1].hand.cards,
                    'tokens': self.playerController.players[1].tokens.get_tokens(),
                    'reserved': self.playerController.players[1].reserved.cards,
                    'nobles': self.playerController.players[1].patrons
                },
                'shop': {
                    'rank1_cards': self.shopController.ranks[0].hand.cards,
                    'rank2_cards': self.shopController.ranks[1].hand.cards,
                    'rank3_cards': self.shopController.ranks[2].hand.cards,
                    'rank1_size': self.shopController.ranks[0].deck.get_size(),
                    'rank2_size': self.shopController.ranks[1].deck.get_size(),
                    'rank3_size': self.shopController.ranks[2].deck.get_size(),
                    'nobles': self.patronController.patrons,
                    'tokens': self.bankController.bank,
                },
            }
            return dictionnary

    def gather_cli_board_state(self) -> dict:
        out = {}
        out['cpu1-vp'] = self.playerController.players[0].victoryPoints.value
        out['cpu1-bonus'] = self.playerController.players[0].hand.compute_hand_bonuses()
        out['cpu1-tokens'] = self.playerController.players[0].tokens
        out['cpu1-nbReserved'] = self.playerController.players[0].reserved.get_size()

        out['cpu2-vp'] = self.playerController.players[1].victoryPoints.value
        out['cpu2-bonus'] = self.playerController.players[1].hand.compute_hand_bonuses()
        out['cpu2-tokens'] = self.playerController.players[1].tokens
        out['cpu2-nbReserved'] = self.playerController.players[1].reserved.get_size()

        """out['cpu3-vp'] = self.playerController.players[2].victoryPoints.value
        out['cpu3-bonus'] = self.playerController.players[2].hand.compute_hand_bonuses()
        out['cpu3-tokens'] = self.playerController.players[2].tokens
        out['cpu3-nbReserved'] = self.playerController.players[2].reserved.get_size()

        out['player-vp'] = self.playerController.players[3].victoryPoints.value
        out['player-bonus'] = self.playerController.players[3].hand.compute_hand_bonuses()
        out['player-tokens'] = self.playerController.players[3].tokens
        out['player-nbReserved'] = self.playerController.players[3].reserved.get_size()"""
        """out['player-reserved'] = []
        for i in range(out['player-nbReserved']):
            out['player-reserved'].append([
                self.playerController.players[3].reserved.cards[i].price,
                self.playerController.players[3].reserved.cards[i].bonus,
                self.playerController.players[3].reserved.cards[i].victoryPoint])"""

        out['bank'] = self.bankController.bank.get_tokens()
        out['patrons'] = [x.requirements for x in self.patronController.patrons]

        for y, yy in zip(range(3), [2, 1, 0]):
            for x in range(4):
                out[f'shop{x}{y}-pv'] = self.shopController.ranks[yy].hand.cards[x].victoryPoint.value
                out[f'shop{x}{y}-bonus'] = self.shopController.ranks[yy].hand.cards[x].bonus
                out[f'shop{x}{y}-price'] = self.shopController.ranks[yy].hand.cards[x].price

        return out

    def launch_game(self, nbPlayer: int) -> None:
        self.bankController.load(nbPlayer)
        self.patronController.load(nbPlayer)
        self.playerController.load(nbPlayer, self.patronController)
        self.shopController.load()

        self.nbPlayer = nbPlayer
        self.firstPlayerId = randint(0, nbPlayer)
        self.currentPlayer = self.firstPlayerId
        self.userId = 0

    def next_player(self) -> None:
        self.currentPlayer += 1
        if self.currentPlayer >= self.nbPlayer:
            self.currentPlayer = 0

    def buy_card(self, cardId: int) -> None:
        if self.shopController.has_card(cardId):
            if err := self.playerController.buy_shop_card(self.currentPlayer, cardId):
                Logger().log(0, err, 'GameManager buy_card')
                return err
        elif err := self.playerController.buy_reserved_card(self.currentPlayer, cardId):

        if err is None:
            self.next_player()

    def reserve_card(self, cardId: int) -> None:
        if err := self.playerController.reserve_card(self.currentPlayer, cardId):
            Logger().log(0, err, 'GameManager reserve_card')
            return err

        if err is None:
            self.next_player()

    def reserve_pile_card(self, pile_level: int) -> None:
        if err := self.playerController.reserve_pile_card(self.currentPlayer, pile_level):
            Logger().log(0, err, 'GameManager reserve_pile_card')
            return err

        if err is None:
            self.next_player()

    def take_token(self, tokens: TokenArray) -> None:
        if err := self.playerController.take_tokens(self.currentPlayer, tokens):
            Logger().log(0, err, 'GameManager take_token')
            return err

        if err is None:
            self.next_player()
            self.next_player()

    def cpu_turn(self) -> None:
        # TODO: call ai
        pass
