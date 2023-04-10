from api.models import BankController
from api.models import PatronController
from api.models import PlayerController
from api.models import ShopController
from django.db import models

from api.models.utils.singleton_model import SingletonModel


class GameManager(SingletonModel):
    bankController: BankController = models.OneToOneField(BankController, on_delete=models.CASCADE, default=BankController())
    patronController: PatronController = models.OneToOneField(PatronController, on_delete=models.CASCADE, blank=True)
    playerController: PlayerController = models.OneToOneField(PlayerController, on_delete=models.CASCADE, blank=True)
    shopController: ShopController = models.OneToOneField(ShopController, on_delete=models.CASCADE, blank=True)


    def gather_board_state(self) -> None:
        # TODO: define what is a board state
        pass
