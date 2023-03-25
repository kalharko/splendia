from dataclasses import dataclass
from Model.Controllers import BankController, PatronController, PlayerController, ShopController


@dataclass
class GameManager():
    bankController: BankController
    patronController: PatronController
    playerController: PlayerController
    shopController: ShopController


