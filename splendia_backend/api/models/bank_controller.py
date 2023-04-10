from logging import raiseExceptions
from api.models import TokenArray
from api.models.utils.singleton_model import SingletonModel
from django.db import models

        

class BankController(SingletonModel):
    bank: TokenArray = models.OneToOneField(TokenArray, on_delete=models.CASCADE, null=True)
    
    def reset_data(self, nbPlayer: int) -> None:
        if(self.bank is None):
            self.bank = TokenArray.objects.create()
        # number of tokens depends on the number of players
        if nbPlayer == 2:
            self.bank.set_tokens([4, 4, 4, 4, 4, 5])
        elif nbPlayer == 3:
            self.bank.deposit_tokens([5, 5, 5, 5, 5, 5])
        elif nbPlayer == 4:
            self.bank.deposit_tokens([7, 7, 7, 7, 7, 5])
        else:
            raiseExceptions("Number of players unsupported")
        self.bank.save()
        self.save()
    


    def deposit(self, tokens: TokenArray) -> None:
        pass

    def withdraw(self, token: TokenArray) -> None:
        pass
