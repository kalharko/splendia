from dataclasses import dataclass



@dataclass
class GameManager():
    bankController: BankController
    patronController: PatronController
    playerController: PlayerController
    shopController: ShopController



@dataclass
class BankController():
    bankModel: BankModel

