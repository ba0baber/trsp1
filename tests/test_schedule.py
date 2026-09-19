from datetime import datetime

import pytest

from models import Room, User
from schedule import Schedule


def objects():
    return Room(1, "301", 30, "Учебная"), User(
        1, "Варвара", "v@example.com",
    )


def test_add_event_creates_event_object():
    room, user = objects()
    schedule = Schedule()
    event = schedule.add_event(
        "Защита", user, room, 20,
        datetime(2026, 9, 21, 10), datetime(2026, 9, 21, 11),
    )
    assert event.id == 1
    assert schedule.events == [event]


def test_add_event_rejects_time_conflict():
    room, user = objects()
    schedule = Schedule()
    schedule.add_event(
        "Первое", user, room, 10,
        datetime(2026, 9, 21, 10), datetime(2026, 9, 21, 11),
    )
    with pytest.raises(ValueError, match="занято"):
        schedule.add_event(
            "Второе", user, room, 10,
            datetime(2026, 9, 21, 10, 30),
            datetime(2026, 9, 21, 11, 30),
        )


def test_remove_event():
    room, user = objects()
    schedule = Schedule()
    event = schedule.add_event(
        "Защита", user, room, 10,
        datetime(2026, 9, 21, 10), datetime(2026, 9, 21, 11),
    )
    assert schedule.remove_event(event.id) is event
    assert schedule.events == []


def test_find_by_organizer():
    room, user = objects()
    schedule = Schedule()
    schedule.add_event(
        "Защита", user, room, 10,
        datetime(2026, 9, 21, 10), datetime(2026, 9, 21, 11),
    )
    assert len(schedule.find_by_organizer("варвара")) == 1


def test_schedule_string_representation():
    assert str(Schedule()) == "Расписание пока пусто"
