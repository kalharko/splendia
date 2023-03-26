from dataclasses import dataclass


@dataclass
class VictoryPoint():
    value: int

    def get_value(self) -> int:
        return self.value

    def set_value(self, value: int) -> None:
        self.value = value
