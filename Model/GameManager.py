from dataclasses import dataclass
from Model.Controllers import BankController, PatronController
from Model.Controllers import PlayerController, ShopController


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
