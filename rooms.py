"""Функции для работы со списком помещений."""

from collections.abc import Iterator


Room = dict[str, object]


def add_room(
    rooms: list[Room], name: str, capacity: int, room_type: str,
) -> Room:
    """Добавить помещение и вернуть созданную запись."""
    if not name.strip() or not room_type.strip():
        raise ValueError("Название и тип помещения не могут быть пустыми")
    if capacity <= 0:
        raise ValueError("Вместимость должна быть положительной")
    room: Room = {
        "id": max((int(item["id"]) for item in rooms), default=0) + 1,
        "name": name.strip(),
        "capacity": capacity,
        "room_type": room_type.strip(),
    }
    rooms.append(room)
    return room


def find_room_by_id(rooms: list[Room], room_id: int) -> Room | None:
    """Найти помещение по идентификатору."""
    return next((room for room in rooms if room["id"] == room_id), None)


def find_rooms(rooms: list[Room], query: str) -> list[Room]:
    """Найти помещения по названию или типу."""
    normalized = query.strip().lower()
    return [
        room for room in rooms
        if normalized in str(room["name"]).lower()
        or normalized in str(room["room_type"]).lower()
    ]


def filter_rooms_by_capacity(
    rooms: list[Room], participants: int,
) -> list[Room]:
    """Вернуть помещения с достаточной вместимостью."""
    return [room for room in rooms if int(room["capacity"]) >= participants]


def sort_rooms_by_capacity(rooms: list[Room]) -> list[Room]:
    """Вернуть помещения по возрастанию вместимости."""
    return sorted(rooms, key=lambda room: int(room["capacity"]))


def iter_rooms_by_type(rooms: list[Room], room_type: str) -> Iterator[Room]:
    """Последовательно выдавать помещения указанного типа."""
    normalized = room_type.strip().lower()
    for room in rooms:
        if str(room["room_type"]).lower() == normalized:
            yield room
