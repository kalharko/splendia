from dataclasses import dataclass
from Model.Controllers import BankController, PatronController
from Model.Controllers import PlayerController, ShopController


@dataclass
class GameManager():
    bankController: BankController
    patronController: PatronController
    playerController: PlayerController
    shopController: ShopController

    def __init__(self) -> None:
        pass
