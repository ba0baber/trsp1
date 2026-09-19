"""Функции для управления расписанием мероприятий."""

from datetime import datetime

from rooms import Room, find_room_by_id


ScheduleItem = dict[str, object]
DATE_FORMAT = "%Y-%m-%d %H:%M"


def parse_datetime(value: str) -> datetime:
    """Преобразовать строку в дату и время."""
    try:
        return datetime.strptime(value.strip(), DATE_FORMAT)
    except ValueError as error:
        raise ValueError("Используйте формат ГГГГ-ММ-ДД ЧЧ:ММ") from error


def intervals_overlap(
    start_a: datetime, end_a: datetime,
    start_b: datetime, end_b: datetime,
) -> bool:
    """Проверить пересечение двух временных интервалов."""
    return start_a < end_b and start_b < end_a


def add_event(
    schedule: list[ScheduleItem], rooms: list[Room], title: str,
    organizer: str, room_id: int, participants: int,
    start_text: str, end_text: str,
) -> ScheduleItem:
    """Добавить мероприятие после проверки помещения и времени."""
    room = find_room_by_id(rooms, room_id)
    if room is None:
        raise LookupError("Помещение не найдено")
    if not title.strip() or not organizer.strip():
        raise ValueError("Название и организатор не могут быть пустыми")
    if participants <= 0:
        raise ValueError("Количество участников должно быть положительным")
    if participants > int(room["capacity"]):
        raise ValueError("В помещении недостаточно мест")
    start = parse_datetime(start_text)
    end = parse_datetime(end_text)
    if end <= start:
        raise ValueError("Окончание должно быть позже начала")
    for item in schedule:
        if item["room_id"] == room_id and intervals_overlap(
            start, end,
            parse_datetime(str(item["start"])),
            parse_datetime(str(item["end"])),
        ):
            raise ValueError("Помещение занято в указанное время")
    event: ScheduleItem = {
        "id": max((int(item["id"]) for item in schedule), default=0) + 1,
        "title": title.strip(),
        "organizer": organizer.strip(),
        "room_id": room_id,
        "participants": participants,
        "start": start.strftime(DATE_FORMAT),
        "end": end.strftime(DATE_FORMAT),
    }
    schedule.append(event)
    return event


def remove_event(schedule: list[ScheduleItem], event_id: int) -> ScheduleItem:
    """Удалить мероприятие из расписания."""
    for index, item in enumerate(schedule):
        if item["id"] == event_id:
            return schedule.pop(index)
    raise LookupError("Мероприятие не найдено")


def find_events_by_organizer(
    schedule: list[ScheduleItem], organizer: str,
) -> list[ScheduleItem]:
    """Вернуть мероприятия указанного пользователя."""
    normalized = organizer.strip().lower()
    return [
        item for item in schedule
        if str(item["organizer"]).lower() == normalized
    ]
