"""Сущность помещения."""

from dataclasses import dataclass
from typing import Any


@dataclass
class Room:
    """Помещение, доступное для проведения мероприятий."""

    id: int
    name: str
    capacity: int
    room_type: str

    def __post_init__(self) -> None:
        if not self.name.strip() or not self.room_type.strip():
            raise ValueError("Название и тип помещения не могут быть пустыми")
        if self.capacity <= 0:
            raise ValueError("Вместимость должна быть положительной")

    def can_host(self, participants: int) -> bool:
        """Проверить, поместятся ли участники."""
        return 0 < participants <= self.capacity

    def to_dict(self) -> dict[str, Any]:
        """Преобразовать помещение в JSON-словарь."""
        return {
            "id": self.id,
            "name": self.name,
            "capacity": self.capacity,
            "room_type": self.room_type,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Room":
        """Создать помещение из JSON-словаря."""
        try:
            return cls(
                int(data["id"]),
                str(data["name"]),
                int(data["capacity"]),
                str(data["room_type"]),
            )
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError("Некорректные данные помещения") from error

    def __str__(self) -> str:
        return (
            f"{self.id}. {self.name}; {self.room_type}; "
            f"{self.capacity} мест"
        )
