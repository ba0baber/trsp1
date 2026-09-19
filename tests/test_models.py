from datetime import datetime

import pytest

from models import Event, Room, User


def test_room_validates_capacity_and_can_host():
    room = Room(1, "Аудитория 301", 30, "Учебная")
    assert room.can_host(25)
    with pytest.raises(ValueError):
        Room(2, "205", 0, "Переговорная")


def test_room_string_representation():
    assert "30 мест" in str(Room(1, "301", 30, "Учебная"))


def test_user_encapsulates_and_validates_email():
    user = User(1, "Варвара", "VARVARA@example.com")
    assert user.email == "varvara@example.com"
    with pytest.raises(ValueError, match="почты"):
        User(2, "Иван", "wrong")


def test_event_connects_room_and_user():
    room = Room(1, "301", 30, "Учебная")
    user = User(1, "Варвара", "v@example.com")
    event = Event(
        1, "Защита", user, room, 20,
        datetime(2026, 9, 21, 10), datetime(2026, 9, 21, 11, 30),
    )
    assert event.room is room
    assert event.organizer is user
    assert event.duration_minutes == 90


def test_event_rejects_excess_participants():
    with pytest.raises(ValueError, match="недостаточно"):
        Event(
            1, "Защита", User(1, "Варя", "v@example.com"),
            Room(1, "301", 10, "Учебная"), 20,
            datetime(2026, 9, 21, 10), datetime(2026, 9, 21, 11),
        )
