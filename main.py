"""Начальный сценарий проекта «Система бронирования помещений»."""

from datetime import date


ROOM_NAME = "Аудитория 301"
ROOM_CAPACITY = 30
HOURLY_RATE = 1500.0
BOOKING_DATE = date(2026, 10, 10)
IS_AVAILABLE = True


def has_enough_capacity(capacity: int, participants: int) -> bool:
    """Проверить, помещаются ли все участники в выбранном помещении."""
    return participants > 0 and participants <= capacity


def get_booking_status(is_available: bool, capacity_ok: bool) -> str:
    """Вернуть пояснение о возможности забронировать помещение."""
    if not is_available:
        return "Помещение уже занято на выбранную дату"
    if not capacity_ok:
        return "Помещение не подходит по вместимости"
    return "Помещение можно забронировать"


def calculate_booking_cost(hourly_rate: float, duration_hours: float) -> float:
    """Рассчитать стоимость аренды с учётом продолжительности мероприятия."""
    if duration_hours <= 0:
        return 0.0
    return hourly_rate * duration_hours


def main() -> None:
    """Запустить демонстрационный сценарий бронирования."""
    print("Система бронирования помещений")
    print(f"Помещение: {ROOM_NAME}")
    print(f"Вместимость: {ROOM_CAPACITY} человек")
    print(f"Дата: {BOOKING_DATE.strftime('%d.%m.%Y')}")

    participants = int(input("Количество участников: "))
    duration_hours = float(input("Продолжительность мероприятия в часах: "))

    capacity_ok = has_enough_capacity(ROOM_CAPACITY, participants)
    status = get_booking_status(IS_AVAILABLE, capacity_ok)
    cost = calculate_booking_cost(HOURLY_RATE, duration_hours)

    print(f"Статус: {status}")
    if IS_AVAILABLE and capacity_ok and cost > 0:
        print(f"Предварительная стоимость: {cost:.2f} руб.")
    else:
        print("Стоимость не рассчитывается, пока бронирование невозможно")


if __name__ == "__main__":
    main()
