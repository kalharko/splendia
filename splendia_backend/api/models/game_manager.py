from dataclasses import dataclass

from api.models import BankController
from api.models import PatronController
from api.models import PlayerController
from api.models import ShopController
from django.db import models


@dataclass
class GameManager(models.Model):
    bankController: BankController = models.OneToOneField(BankController, on_delete=models.CASCADE)
    patronController: PatronController = models.OneToOneField(PatronController, on_delete=models.CASCADE)
    playerController: PlayerController = models.OneToOneField(PlayerController, on_delete=models.CASCADE)
    shopController: ShopController = models.OneToOneField(ShopController, on_delete=models.CASCADE)

    def __init__(self, nbPlayer: int) -> None:
        self.bankController.__init__(nbPlayer)

    def gather_board_state(self) -> None:
        # TODO: define what is a board state
        pass
