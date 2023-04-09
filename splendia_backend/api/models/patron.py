from dataclasses import dataclass
from api.models import TokenArray
from api.models import VictoryPoint
from django.db import models


@dataclass
class Patron(models.Model):
    requirements: TokenArray() = models.OneToOneField(TokenArray, on_delete=models.CASCADE)
    victoryPoints: VictoryPoint = models.VictoryPoint(TokenArray, on_delete=models.CASCADE)
