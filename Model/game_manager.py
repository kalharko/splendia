from dataclasses import dataclass

from model.bank_controller import BankController
from model.patron_controller import PatronController
from model.player_controller import PlayerController
from model.shop_controller import ShopController


@dataclass
class GameManager():
    bankController: BankController
    patronController: PatronController
    playerController: PlayerController
    shopController: ShopController

    def __init__(self, nbPlayer: int) -> None:
        pass

    def gather_board_state(self) -> None:
        # TODO: define what is a board state
        pass
