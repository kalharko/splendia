from django.db import models


class VictoryPoint(models.Model):
    value: int = models.IntegerField(null=True)

    def get_value(self) -> int:
        return self.value

    def set_value(self, value: int) -> None:
        self.value = value
