from dataclasses import dataclass


@dataclass
class VictoryPoint():
    """VictoryPoint class is used to store the number of victory points of a player

    Attributes:
        value (int): the number of victory points of a player
    """
    value: int

    def get_value(self) -> int:
        """Return the number of victory points of a player

        Returns:
            int: the number of victory points of a player
            """

        return self.value

    def set_value(self, value: int) -> None:
        """Set the number of victory points of a player

        Args:
            value (int): the number of victory points of a player
            """

        self.value = value
