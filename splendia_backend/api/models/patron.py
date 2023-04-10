from api.models import TokenArray
from api.models import VictoryPoint
from django.db import models


class Patron(models.Model):
    requirements: TokenArray() = models.OneToOneField(TokenArray, null=True, on_delete=models.CASCADE,)
    victoryPoints: VictoryPoint = models.OneToOneField(VictoryPoint, blank=True, on_delete=models.CASCADE,)
