"""Консольный интерфейс объектной системы учёта коллекции скинов."""

from pathlib import Path

from collection import Collection
from models import Skin, User
from skins import filter_skins_by_price, find_skins, sort_skins_by_price
from storage import (
    StorageError, load_collection, load_skins, save_collection, save_skins,
)
from utils import input_float, input_int


DATA_DIR = Path(__file__).parent / "data"
SKINS_FILE = DATA_DIR / "skins.json"
COLLECTION_FILE = DATA_DIR / "collection.json"


def show_skins(skins: list[Skin]) -> None:
    """Вывести каталог скинов."""
    print("\n".join(str(skin) for skin in skins) or "Скины не найдены")


def save_project_data(skins: list[Skin], collection: Collection) -> None:
    """Сохранить объектную модель в JSON-файлы."""
    save_skins(SKINS_FILE, skins)
    save_collection(COLLECTION_FILE, collection)


def run_menu(skins: list[Skin], collection: Collection) -> None:
    """Обрабатывать пункты пользовательского меню до команды выхода."""
    while True:
        print("\n=== Коллекция скинов Counter-Strike (ООП) ===")
        print("1. Показать каталог")
        print("2. Найти скин")
        print("3. Отобрать скины по цене")
        print("4. Купить скин")
        print("5. Удалить предмет из коллекции")
        print("6. Показать коллекцию")
        print("0. Выход")
        choice = input("Выберите действие: ").strip()
        try:
            if choice == "1":
                show_skins(sort_skins_by_price(skins))
            elif choice == "2":
                show_skins(find_skins(skins, input("Название или оружие: ")))
            elif choice == "3":
                limit = input_float("Максимальная цена: ", minimum=0)
                show_skins(filter_skins_by_price(skins, limit))
            elif choice == "4":
                user = User(
                    input("Имя владельца: "),
                    input_float("Баланс: ", minimum=0),
                )
                skin_id = input_int("ID скина: ", minimum=1)
                item = collection.purchase(skins, user, skin_id)
                save_project_data(skins, collection)
                print(f"Скин добавлен. {user}. ID записи: {item.id}")
            elif choice == "5":
                item_id = input_int("ID записи коллекции: ", minimum=1)
                collection.remove(skins, item_id)
                save_project_data(skins, collection)
                print("Предмет удалён из коллекции")
            elif choice == "6":
                print(collection)
            elif choice == "0":
                break
            else:
                print("Неизвестная команда")
        except (LookupError, ValueError, StorageError) as error:
            print(f"Ошибка: {error}")


def main() -> None:
    """Загрузить объекты и запустить консольное меню."""
    try:
        run_menu(load_skins(SKINS_FILE), load_collection(COLLECTION_FILE))
    except StorageError as error:
        print(f"Ошибка хранения данных: {error}")


if __name__ == "__main__":
    main()
