"""Практическая работа 1: проверка возможности запланировать мероприятие."""

from datetime import datetime


ROOM_NAME = "Аудитория 301"
ROOM_CAPACITY = 30
EVENT_NAME = "Защита практической работы"
EVENT_PARTICIPANTS = 25
START_TIME = "2026-09-21 10:00"
END_TIME = "2026-09-21 11:30"
ROOM_IS_AVAILABLE = True


def parse_datetime(value: str) -> datetime:
    """Преобразовать строку формата ГГГГ-ММ-ДД ЧЧ:ММ в дату и время."""
    return datetime.strptime(value, "%Y-%m-%d %H:%M")


def has_enough_capacity(capacity: int, participants: int) -> bool:
    """Проверить, достаточно ли мест в помещении."""
    return capacity >= participants


def calculate_duration_minutes(start: datetime, end: datetime) -> int:
    """Вычислить продолжительность мероприятия в минутах."""
    if end <= start:
        raise ValueError("Время окончания должно быть позже времени начала")
    return int((end - start).total_seconds() // 60)


def get_planning_status(
    is_available: bool,
    capacity_is_enough: bool,
) -> str:
    """Вернуть результат проверки возможности планирования."""
    if not is_available:
        return "Помещение занято"
    if not capacity_is_enough:
        return "В помещении недостаточно мест"
    return "Мероприятие можно добавить в расписание"


def main() -> None:
    """Запустить демонстрационный сценарий практической работы 1."""
    print("Сервис планирования использования помещений")
    print(f"Помещение: {ROOM_NAME}, вместимость: {ROOM_CAPACITY}")
    print(f"Мероприятие: {EVENT_NAME}")
    print(f"Количество участников: {EVENT_PARTICIPANTS}")

    start = parse_datetime(START_TIME)
    end = parse_datetime(END_TIME)
    duration = calculate_duration_minutes(start, end)
    capacity_is_enough = has_enough_capacity(
        ROOM_CAPACITY,
        EVENT_PARTICIPANTS,
    )
    status = get_planning_status(ROOM_IS_AVAILABLE, capacity_is_enough)

    print(f"Начало: {start:%d.%m.%Y %H:%M}")
    print(f"Окончание: {end:%d.%m.%Y %H:%M}")
    print(f"Продолжительность: {duration} мин.")
    print(f"Результат: {status}")


if __name__ == "__main__":
    main()
