from api.models import TokenArray
from api.models import VictoryPoint
from django.db import models



class Card(models.Model):
    card_id: int = models.IntegerField()
    price: TokenArray = models.ManyToManyField(TokenArray, related_name='price')
    bonus: TokenArray = models.ManyToManyField(TokenArray, related_name='bonus')
    victoryPoint: VictoryPoint = models.OneToOneField(VictoryPoint, on_delete=models.CASCADE, null=True)

    # def __init__(self, price: TokenArray, bonus: TokenArray,
    #              victoryPoint: VictoryPoint, card_id: int) -> None:
    #     self.price = price
    #     self.bonus = bonus
    #     self.victoryPoint = victoryPoint
    #     self.card_id = card_id
