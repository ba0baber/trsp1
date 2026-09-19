"""Загрузка и сохранение объектов проекта в JSON."""

import json
from pathlib import Path
from typing import Any

from models import Event, Room, User, parse_datetime
from schedule import Schedule


class StorageError(Exception):
    """Ошибка чтения, записи или преобразования данных."""


def load_json(path: Path) -> list[dict[str, Any]]:
    """Загрузить список из JSON; для отсутствующего файла вернуть []."""
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError) as error:
        raise StorageError(f"Не удалось загрузить данные из {path}") from error
    if not isinstance(data, list):
        raise StorageError(f"В файле {path} должен находиться список")
    return data


def save_json(path: Path, data: list[dict[str, Any]]) -> None:
    """Сохранить список JSON-словарей."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except OSError as error:
        raise StorageError(f"Не удалось сохранить данные в {path}") from error


def load_rooms(path: Path) -> list[Room]:
    """Загрузить JSON и создать объекты Room."""
    try:
        return [Room.from_dict(item) for item in load_json(path)]
    except ValueError as error:
        raise StorageError("Некорректные данные помещений") from error


def load_users(path: Path) -> list[User]:
    """Загрузить JSON и создать объекты User."""
    try:
        return [User.from_dict(item) for item in load_json(path)]
    except ValueError as error:
        raise StorageError("Некорректные данные пользователей") from error


def load_schedule(
    path: Path, rooms: list[Room], users: list[User],
) -> Schedule:
    """Загрузить мероприятия и восстановить связи между объектами."""
    rooms_by_id = {room.id: room for room in rooms}
    users_by_id = {user.id: user for user in users}
    events: list[Event] = []
    try:
        for data in load_json(path):
            events.append(Event(
                int(data["id"]), str(data["title"]),
                users_by_id[int(data["organizer_id"])],
                rooms_by_id[int(data["room_id"])],
                int(data["participants"]),
                parse_datetime(str(data["start"])),
                parse_datetime(str(data["end"])),
            ))
    except (KeyError, TypeError, ValueError) as error:
        raise StorageError("Некорректные данные расписания") from error
    return Schedule(events)


def save_rooms(path: Path, rooms: list[Room]) -> None:
    """Сохранить объекты Room."""
    save_json(path, [room.to_dict() for room in rooms])


def save_users(path: Path, users: list[User]) -> None:
    """Сохранить объекты User."""
    save_json(path, [user.to_dict() for user in users])


def save_schedule(path: Path, schedule: Schedule) -> None:
    """Сохранить объекты Event из расписания."""
    save_json(path, [event.to_dict() for event in schedule.events])
