"""Консольный интерфейс сервиса планирования помещений."""

from pathlib import Path

from rooms import filter_rooms_by_capacity, find_rooms, sort_rooms_by_capacity
from schedule import add_event, remove_event
from storage import StorageError, load_json, save_json
from utils import input_int


DATA_DIR = Path(__file__).parent / "data"
ROOMS_FILE = DATA_DIR / "rooms.json"
SCHEDULE_FILE = DATA_DIR / "schedule.json"


def show_rooms(rooms: list[dict[str, object]]) -> None:
    """Вывести список помещений."""
    if not rooms:
        print("Помещения не найдены")
    for room in rooms:
        print(
            f'{room["id"]}. {room["name"]}; {room["room_type"]}; '
            f'{room["capacity"]} мест'
        )


def show_schedule(schedule: list[dict[str, object]]) -> None:
    """Вывести расписание мероприятий."""
    if not schedule:
        print("Расписание пока пусто")
    for event in schedule:
        print(
            f'{event["id"]}. {event["title"]}; помещение {event["room_id"]}; '
            f'{event["start"]} — {event["end"]}; '
            f'организатор: {event["organizer"]}'
        )


def run_menu(
    rooms: list[dict[str, object]],
    schedule: list[dict[str, object]],
) -> None:
    """Обрабатывать пункты меню до команды выхода."""
    while True:
        print("\n=== Планирование помещений ===")
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
                event = add_event(
                    schedule, rooms, input("Название: "),
                    input("Организатор: "), input_int("ID помещения: ", 1),
                    input_int("Участников: ", 1), input("Начало: "),
                    input("Окончание: "),
                )
                save_json(SCHEDULE_FILE, schedule)
                print(f'Мероприятие добавлено. ID: {event["id"]}')
            elif choice == "5":
                remove_event(schedule, input_int("ID мероприятия: ", 1))
                save_json(SCHEDULE_FILE, schedule)
                print("Мероприятие удалено")
            elif choice == "6":
                show_schedule(schedule)
            elif choice == "0":
                break
            else:
                print("Неизвестная команда")
        except (LookupError, ValueError, StorageError) as error:
            print(f"Ошибка: {error}")


def main() -> None:
    """Загрузить данные и запустить меню."""
    try:
        run_menu(load_json(ROOMS_FILE), load_json(SCHEDULE_FILE))
    except StorageError as error:
        print(f"Ошибка хранения данных: {error}")


if __name__ == "__main__":
    main()
