from api.models import BankController
from api.models import PatronController
from api.models import PlayerController
from api.models import ShopController
from django.db import models

class GameManagerManager(models.Manager):
    def create_game_manager(self, nbPlayer: int):
        return self.create(bankController = BankController.objects.create_bank_controller(nbPlayer=nbPlayer))


class GameManager(models.Model):
    bankController: BankController = models.OneToOneField(BankController, on_delete=models.CASCADE)
    patronController: PatronController = models.OneToOneField(PatronController, on_delete=models.CASCADE)
    playerController: PlayerController = models.OneToOneField(PlayerController, on_delete=models.CASCADE)
    shopController: ShopController = models.OneToOneField(ShopController, on_delete=models.CASCADE)
    objects = GameManagerManager()

    def gather_board_state(self) -> None:
        # TODO: define what is a board state
        pass
