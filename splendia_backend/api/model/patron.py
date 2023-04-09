from dataclasses import dataclass
from model.token_array import TokenArray
from model.victory_point import VictoryPoint
from django.db import models


@dataclass
class Patron(models.Model):
    requirements: TokenArray() = models.OneToOneField(TokenArray, on_delete=models.CASCADE)
    victoryPoints: VictoryPoint = models.VictoryPoint(TokenArray, on_delete=models.CASCADE)
