import pytest

from rooms import (
    add_room, filter_rooms_by_capacity, find_rooms,
    iter_rooms_by_type, sort_rooms_by_capacity,
)


def sample_rooms():
    return [
        {"id": 1, "name": "Аудитория 301", "capacity": 30,
         "room_type": "Учебная аудитория"},
        {"id": 2, "name": "Конференц-зал", "capacity": 120,
         "room_type": "Конференц-зал"},
    ]


def test_add_room_assigns_next_id():
    rooms = sample_rooms()
    assert add_room(rooms, "205", 10, "Переговорная")["id"] == 3


def test_add_room_rejects_invalid_capacity():
    with pytest.raises(ValueError):
        add_room([], "205", 0, "Переговорная")


def test_find_rooms_is_case_insensitive():
    assert find_rooms(sample_rooms(), "аудитория")[0]["id"] == 1


def test_filter_rooms_by_capacity():
    result = filter_rooms_by_capacity(sample_rooms(), 50)
    assert [room["id"] for room in result] == [2]


def test_sort_rooms_by_capacity():
    result = sort_rooms_by_capacity(sample_rooms())
    assert [room["id"] for room in result] == [1, 2]


def test_generator_filters_by_type():
    result = list(iter_rooms_by_type(sample_rooms(), "конференц-зал"))
    assert [room["id"] for room in result] == [2]
