import pytest

from schedule import add_event, find_events_by_organizer, remove_event


def sample_rooms():
    return [{"id": 1, "name": "301", "capacity": 30,
             "room_type": "Учебная"}]


def test_add_event():
    schedule = []
    event = add_event(
        schedule, sample_rooms(), "Защита", "Варвара", 1, 20,
        "2026-09-21 10:00", "2026-09-21 11:00",
    )
    assert event["id"] == 1
    assert len(schedule) == 1


def test_add_event_rejects_capacity():
    with pytest.raises(ValueError, match="недостаточно"):
        add_event(
            [], sample_rooms(), "Защита", "Варвара", 1, 50,
            "2026-09-21 10:00", "2026-09-21 11:00",
        )


def test_add_event_rejects_time_conflict():
    schedule = []
    add_event(
        schedule, sample_rooms(), "Первое", "Варвара", 1, 10,
        "2026-09-21 10:00", "2026-09-21 11:00",
    )
    with pytest.raises(ValueError, match="занято"):
        add_event(
            schedule, sample_rooms(), "Второе", "Иван", 1, 10,
            "2026-09-21 10:30", "2026-09-21 11:30",
        )


def test_remove_event():
    schedule = [{"id": 1, "title": "Защита"}]
    assert remove_event(schedule, 1)["title"] == "Защита"
    assert schedule == []


def test_find_events_by_organizer():
    schedule = [
        {"organizer": "Варвара"},
        {"organizer": "Иван"},
    ]
    assert len(find_events_by_organizer(schedule, "варвара")) == 1
