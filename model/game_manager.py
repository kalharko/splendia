from dataclasses import dataclass
from random import randint

from model.bank_controller import BankController
from model.patron_controller import PatronController
from model.player_controller import PlayerController
from model.shop_controller import ShopController
from model.token_array import TokenArray


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

    def __init__(self, nbPlayer: int) -> None:
        self.bankController = BankController()
        self.patronController = PatronController()
        self.playerController = PlayerController()
        self.shopController = ShopController()
        self.currentPlayer = 0
        self.userId = 0
        self.firstPlayerId = 0
        self.nbPlayer = 4

    def gather_board_state(self) -> None:
        # TODO: define what is a board state
        pass

    def gather_cli_board_state(self) -> dict:
        out = {}
        out['cpu1-vp'] = self.playerController.players[0].victoryPoints.value
        out['cpu1-bonus'] = self.playerController.players[0].hand.compute_hand_bonuses()
        out['cpu1-tokens'] = self.playerController.players[0].get_tokens()
        out['cpu1-nbReserved'] = self.playerController.players[0].reserved.get_size()

        out['cpu2-vp'] = self.playerController.players[1].victoryPoints.value
        out['cpu2-bonus'] = self.playerController.players[1].hand.compute_hand_bonuses()
        out['cpu2-tokens'] = self.playerController.players[1].get_tokens()
        out['cpu2-nbReserved'] = self.playerController.players[1].reserved.get_size()

        out['cpu3-vp'] = self.playerController.players[2].victoryPoints.value
        out['cpu3-bonus'] = self.playerController.players[2].hand.compute_hand_bonuses()
        out['cpu3-tokens'] = self.playerController.players[2].get_tokens()
        out['cpu3-nbReserved'] = self.playerController.players[2].reserved.get_size()

        out['player-vp'] = self.playerController.players[3].victoryPoints.value
        out['player-bonus'] = self.playerController.players[3].hand.compute_hand_bonuses()
        out['player-tokens'] = self.playerController.players[3].get_tokens()
        out['player-nbReserved'] = self.playerController.players[3].reserved.get_size()
        out['player-reserved'] = []
        for i in range(out['player-nbReserved']):
            out['player-reserved'].append([
                self.playerController.players[3].reserved.cards[i].price,
                self.playerController.players[3].reserved.cards[i].bonus,
                self.playerController.players[3].reserved.cards[i].victoryPoint])

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

    def buy_card(self, cardId: int) -> None:
        # TODO: return err si current player != userId
        pass

    def reserve_card(self, cardId: int) -> None:
        # TODO: return err si current player != userId
        pass

    def reserve_card_on_pile(self, pile_level: int) -> None:
        # TODO: return err si current player != userId
        pass

    def take_token(self, tokens: TokenArray) -> None:
        # TODO: return err si current player != userId
        pass

    def cpu_turn(self) -> None:
        # TODO: return err si current player != userId
        pass
