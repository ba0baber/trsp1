from models import Room
from rooms import (
    add_room, filter_rooms_by_capacity, find_rooms,
    iter_rooms_by_type, sort_rooms_by_capacity,
)


def sample_rooms():
    return [
        Room(1, "Аудитория 301", 30, "Учебная аудитория"),
        Room(2, "Конференц-зал", 120, "Конференц-зал"),
    ]


def test_add_room_creates_object_and_assigns_id():
    rooms = sample_rooms()
    room = add_room(rooms, "205", 10, "Переговорная")
    assert isinstance(room, Room)
    assert room.id == 3


def test_find_rooms_is_case_insensitive():
    assert find_rooms(sample_rooms(), "аудитория")[0].id == 1


def test_filter_rooms_by_capacity():
    assert [room.id for room in filter_rooms_by_capacity(
        sample_rooms(), 50,
    )] == [2]


def test_sort_rooms_by_capacity():
    result = sort_rooms_by_capacity(sample_rooms())
    assert [room.id for room in result] == [1, 2]


def test_generator_filters_by_type():
    result = list(iter_rooms_by_type(sample_rooms(), "конференц-зал"))
    assert [room.id for room in result] == [2]
