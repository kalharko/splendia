from dataclasses import dataclass

from api.models import TokenArray
from api.models import VictoryPoint
from django.db import models


@dataclass
class Card(models.Model):
    card_id: int = models.IntegerField()
    price: TokenArray = models.OneToOneField(TokenArray, on_delete=models.CASCADE)
    bonus: TokenArray = models.OneToOneField(TokenArray, on_delete=models.CASCADE)
    victoryPoint: VictoryPoint = models.OneToOneField(VictoryPoint, on_delete=models.CASCADE)

    # def __init__(self, price: TokenArray, bonus: TokenArray,
    #              victoryPoint: VictoryPoint, card_id: int) -> None:
    #     self.price = price
    #     self.bonus = bonus
    #     self.victoryPoint = victoryPoint
    #     self.card_id = card_id
