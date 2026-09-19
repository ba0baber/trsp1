"""Класс расписания и взаимодействие объектов предметной области."""

from datetime import datetime

from models import Event, Room, User


class Schedule:
    """Расписание, содержащее объекты Event."""

    def __init__(self, events: list[Event] | None = None) -> None:
        self.events = events if events is not None else []

    def add_event(
        self, title: str, organizer: User, room: Room,
        participants: int, start: datetime, end: datetime,
    ) -> Event:
        """Создать мероприятие при отсутствии временного конфликта."""
        event = Event(
            max((item.id for item in self.events), default=0) + 1,
            title, organizer, room, participants, start, end,
        )
        if any(event.overlaps(item) for item in self.events):
            raise ValueError("Помещение занято в указанное время")
        self.events.append(event)
        return event

    def remove_event(self, event_id: int) -> Event:
        """Удалить мероприятие из расписания."""
        for index, event in enumerate(self.events):
            if event.id == event_id:
                return self.events.pop(index)
        raise LookupError("Мероприятие не найдено")

    def find_by_organizer(self, organizer: str) -> list[Event]:
        """Вернуть мероприятия указанного организатора."""
        normalized = organizer.strip().lower()
        return [
            event for event in self.events
            if event.organizer.name.lower() == normalized
        ]

    def __str__(self) -> str:
        return "\n".join(str(event) for event in self.events) or (
            "Расписание пока пусто"
        )
