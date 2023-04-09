from dataclasses import dataclass
from django.db import models


@dataclass
class VictoryPoint(models.Model):
    value: int = models.IntegerField()

    def get_value(self) -> int:
        return self.value

    def set_value(self, value: int) -> None:
        self.value = value
