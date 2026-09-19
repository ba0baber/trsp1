import json

import pytest

from models import Room, User
from schedule import Schedule
from storage import (
    StorageError, load_json, load_rooms, load_schedule, load_users,
    save_rooms, save_schedule, save_users,
)


def test_load_invalid_json_raises_storage_error(tmp_path):
    path = tmp_path / "broken.json"
    path.write_text("{broken", encoding="utf-8")
    with pytest.raises(StorageError):
        load_json(path)


def test_load_rejects_non_list_json(tmp_path):
    path = tmp_path / "object.json"
    path.write_text(json.dumps({"id": 1}), encoding="utf-8")
    with pytest.raises(StorageError, match="список"):
        load_json(path)


def test_room_and_user_objects_round_trip(tmp_path):
    rooms_path = tmp_path / "rooms.json"
    users_path = tmp_path / "users.json"
    save_rooms(rooms_path, [Room(1, "301", 30, "Учебная")])
    save_users(users_path, [User(1, "Варвара", "v@example.com")])
    assert isinstance(load_rooms(rooms_path)[0], Room)
    assert isinstance(load_users(users_path)[0], User)


def test_schedule_restores_object_links(tmp_path):
    rooms = [Room(1, "301", 30, "Учебная")]
    users = [User(1, "Варвара", "v@example.com")]
    schedule = Schedule()
    schedule.add_event(
        "Защита", users[0], rooms[0], 20,
        __import__("datetime").datetime(2026, 9, 21, 10),
        __import__("datetime").datetime(2026, 9, 21, 11),
    )
    path = tmp_path / "schedule.json"
    save_schedule(path, schedule)
    loaded = load_schedule(path, rooms, users)
    assert loaded.events[0].room is rooms[0]
    assert loaded.events[0].organizer is users[0]
