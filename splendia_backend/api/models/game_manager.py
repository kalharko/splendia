from api.models import BankController
from api.models import PatronController
from api.models import PlayerController
from api.models import ShopController
from django.db import models

from api.models.utils.singleton_model import SingletonModel


class GameManagerManager(models.Manager):
    
    def get_game_manager(self):
        return self.first()


class GameManager(SingletonModel):
    bankController: BankController = models.OneToOneField(BankController, on_delete=models.CASCADE, null=True)
    patronController: PatronController = models.OneToOneField(PatronController, on_delete=models.CASCADE, null=True)
    playerController: PlayerController = models.OneToOneField(PlayerController, on_delete=models.CASCADE, null=True)
    shopController: ShopController = models.OneToOneField(ShopController, on_delete=models.CASCADE, null=True)
    objects = GameManagerManager()
    
    def start_new_game(self, nbPlayer: int) -> None:
        self.bankController.reset_data(nbPlayer) 
        self.patronController.reset_data(nbPlayer)
    


    def gather_board_state(self) -> None:
        # TODO: define what is a board state
        pass
