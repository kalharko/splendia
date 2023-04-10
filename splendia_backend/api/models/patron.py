from api.models import TokenArray
from api.models import VictoryPoint
from django.db import models


class Patron(models.Model):
    requirements: TokenArray() = models.OneToOneField(TokenArray, on_delete=models.CASCADE, blank=True)
    victoryPoints: VictoryPoint = models.OneToOneField(VictoryPoint, on_delete=models.CASCADE, blank=True)
