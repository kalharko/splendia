from logging import raiseExceptions
from api.models import TokenArray
from api.models.utils.singleton_model import SingletonModel
from django.db import models


class BankControllerManager(models.Manager):
    
    def create_bank_controller(self, nbPlayer: int):
        bank_controller = self.create(bank = TokenArray.objects.create_token_array())
        # number of tokens depends on the number of players
        if nbPlayer == 2:
            bank_controller.bank.deposit_tokens([4, 4, 4, 4, 4, 5])
        elif nbPlayer == 3:
            bank_controller.bank.deposit_tokens([5, 5, 5, 5, 5, 5])
        elif nbPlayer == 4:
            bank_controller.bank.deposit_tokens([7, 7, 7, 7, 7, 5])
        else:
            raiseExceptions("Number of players unsupported")
        
            
        return bank_controller
    

class BankController(SingletonModel):
    bank: TokenArray = models.OneToOneField(TokenArray, on_delete=models.CASCADE, blank=True)
    objects = BankControllerManager()


    def deposit(self, tokens: TokenArray) -> None:
        pass

    def withdraw(self, token: TokenArray) -> None:
        pass
