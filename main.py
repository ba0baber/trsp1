"""Консольный интерфейс объектного сервиса планирования помещений."""

from pathlib import Path

from models import Room, User, parse_datetime
from rooms import filter_rooms_by_capacity, find_room_by_id, find_rooms
from rooms import sort_rooms_by_capacity
from schedule import Schedule
from storage import (
    StorageError, load_rooms, load_schedule, load_users, save_schedule,
)
from utils import input_int


DATA_DIR = Path(__file__).parent / "data"
ROOMS_FILE = DATA_DIR / "rooms.json"
USERS_FILE = DATA_DIR / "users.json"
SCHEDULE_FILE = DATA_DIR / "schedule.json"


def show_rooms(rooms: list[Room]) -> None:
    """Вывести объекты помещений."""
    print("\n".join(str(room) for room in rooms) or "Помещения не найдены")


def select_user(users: list[User], user_id: int) -> User:
    """Найти пользователя или сообщить об ошибке."""
    user = next((item for item in users if item.id == user_id), None)
    if user is None:
        raise LookupError("Пользователь не найден")
    return user


def run_menu(
    rooms: list[Room], users: list[User], schedule: Schedule,
) -> None:
    """Обрабатывать пункты меню до команды выхода."""
    while True:
        print("\n=== Планирование помещений (ООП) ===")
        print("1. Показать помещения")
        print("2. Найти помещение")
        print("3. Подобрать помещение по вместимости")
        print("4. Добавить мероприятие")
        print("5. Удалить мероприятие")
        print("6. Показать расписание")
        print("0. Выход")
        choice = input("Выберите действие: ").strip()
        try:
            if choice == "1":
                show_rooms(sort_rooms_by_capacity(rooms))
            elif choice == "2":
                show_rooms(find_rooms(rooms, input("Название или тип: ")))
            elif choice == "3":
                count = input_int("Количество участников: ", 1)
                show_rooms(filter_rooms_by_capacity(rooms, count))
            elif choice == "4":
                room = find_room_by_id(
                    rooms, input_int("ID помещения: ", 1),
                )
                if room is None:
                    raise LookupError("Помещение не найдено")
                event = schedule.add_event(
                    input("Название: "),
                    select_user(users, input_int("ID организатора: ", 1)),
                    room, input_int("Участников: ", 1),
                    parse_datetime(input("Начало: ")),
                    parse_datetime(input("Окончание: ")),
                )
                save_schedule(SCHEDULE_FILE, schedule)
                print(f"Мероприятие добавлено. ID: {event.id}")
            elif choice == "5":
                schedule.remove_event(input_int("ID мероприятия: ", 1))
                save_schedule(SCHEDULE_FILE, schedule)
                print("Мероприятие удалено")
            elif choice == "6":
                print(schedule)
            elif choice == "0":
                break
            else:
                print("Неизвестная команда")
        except (LookupError, ValueError, StorageError) as error:
            print(f"Ошибка: {error}")


def main() -> None:
    """Загрузить объектную модель и запустить меню."""
    try:
        rooms = load_rooms(ROOMS_FILE)
        users = load_users(USERS_FILE)
        run_menu(rooms, users, load_schedule(SCHEDULE_FILE, rooms, users))
    except StorageError as error:
        print(f"Ошибка хранения данных: {error}")


if __name__ == "__main__":
    main()
