"""Сущность мероприятия."""

from datetime import datetime
from typing import Any

from room import Room
from user import User
from utils import DATE_FORMAT


class Event:
    """Мероприятие, связанное с помещением и организатором."""

    def __init__(
        self,
        event_id: int,
        title: str,
        organizer: User,
        room: Room,
        participants: int,
        start: datetime,
        end: datetime,
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
            "id": self.id,
            "title": self.title,
            "organizer_id": self.organizer.id,
            "room_id": self.room.id,
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
