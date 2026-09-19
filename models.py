"""Классы предметной области сервиса планирования помещений."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any


DATE_FORMAT = "%Y-%m-%d %H:%M"


def parse_datetime(value: str) -> datetime:
    """Преобразовать строку в дату и время."""
    try:
        return datetime.strptime(value.strip(), DATE_FORMAT)
    except ValueError as error:
        raise ValueError("Используйте формат ГГГГ-ММ-ДД ЧЧ:ММ") from error


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
            "id": self.id, "name": self.name,
            "capacity": self.capacity, "room_type": self.room_type,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Room":
        """Создать помещение из JSON-словаря."""
        try:
            return cls(
                int(data["id"]), str(data["name"]),
                int(data["capacity"]), str(data["room_type"]),
            )
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError("Некорректные данные помещения") from error

    def __str__(self) -> str:
        return (
            f"{self.id}. {self.name}; {self.room_type}; "
            f"{self.capacity} мест"
        )


class User:
    """Пользователь, который организует мероприятия."""

    def __init__(self, user_id: int, name: str, email: str) -> None:
        if not name.strip():
            raise ValueError("Имя пользователя не может быть пустым")
        self.id = user_id
        self.name = name.strip()
        self.email = email

    @property
    def email(self) -> str:
        """Вернуть адрес электронной почты."""
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        if "@" not in value or "." not in value.split("@")[-1]:
            raise ValueError("Некорректный адрес электронной почты")
        self._email = value.strip().lower()

    def to_dict(self) -> dict[str, Any]:
        """Преобразовать пользователя в JSON-словарь."""
        return {"id": self.id, "name": self.name, "email": self.email}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "User":
        """Создать пользователя из JSON-словаря."""
        try:
            return cls(int(data["id"]), str(data["name"]), str(data["email"]))
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError("Некорректные данные пользователя") from error

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"


class Event:
    """Мероприятие, связанное с помещением и организатором."""

    def __init__(
        self, event_id: int, title: str, organizer: User, room: Room,
        participants: int, start: datetime, end: datetime,
    ) -> None:
        if not title.strip():
            raise ValueError("Название мероприятия не может быть пустым")
        if not room.can_host(participants):
            raise ValueError("В помещении недостаточно мест")
        if end <= start:
            raise ValueError("Окончание должно быть позже начала")
        self.id = event_id
        self.title = title.strip()
        self.organizer = organizer
        self.room = room
        self.participants = participants
        self.start = start
        self.end = end

    @property
    def duration_minutes(self) -> int:
        """Вернуть продолжительность мероприятия в минутах."""
        return int((self.end - self.start).total_seconds() // 60)

    def overlaps(self, other: "Event") -> bool:
        """Проверить конфликт времени с другим мероприятием."""
        return (
            self.room.id == other.room.id
            and self.start < other.end
            and other.start < self.end
        )

    def to_dict(self) -> dict[str, Any]:
        """Преобразовать мероприятие в JSON-словарь."""
        return {
            "id": self.id, "title": self.title,
            "organizer_id": self.organizer.id, "room_id": self.room.id,
            "participants": self.participants,
            "start": self.start.strftime(DATE_FORMAT),
            "end": self.end.strftime(DATE_FORMAT),
        }

    def __str__(self) -> str:
        return (
            f"{self.id}. {self.title}; {self.room.name}; "
            f"{self.start:%d.%m.%Y %H:%M}–{self.end:%H:%M}; "
            f"организатор: {self.organizer.name}"
        )
