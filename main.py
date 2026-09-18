"""Консольный интерфейс системы учёта коллекции скинов."""

from pathlib import Path

from collection import (
    add_to_collection,
    calculate_collection_value,
    remove_from_collection,
)
from skins import filter_skins_by_price, find_skins, sort_skins_by_price
from storage import StorageError, load_json, save_json
from utils import input_float, input_int


DATA_DIR = Path(__file__).parent / "data"
SKINS_FILE = DATA_DIR / "skins.json"
COLLECTION_FILE = DATA_DIR / "collection.json"


def show_skins(skins: list[dict[str, object]]) -> None:
    """Вывести каталог скинов в компактном виде."""
    if not skins:
        print("Скины не найдены")
        return
    for skin in skins:
        availability = "доступен" if skin["is_available"] else "в коллекции"
        print(
            f'{skin["id"]}. {skin["weapon"]} | {skin["name"]}; '
            f'{skin["condition"]}; {float(skin["price"]):.2f} руб.; '
            f"{availability}"
        )


def show_collection(collection: list[dict[str, object]]) -> None:
    """Вывести коллекцию и её общую стоимость."""
    if not collection:
        print("Коллекция пока пуста")
        return
    for item in collection:
        print(
            f'Запись {item["id"]}: владелец {item["owner"]}, '
            f'скин {item["skin_id"]}, цена покупки '
            f'{float(item["purchase_price"]):.2f} руб.'
        )
    value = calculate_collection_value(collection)
    print(f"Стоимость коллекции: {value:.2f} руб.")


def save_project_data(
    skins: list[dict[str, object]],
    collection: list[dict[str, object]],
) -> None:
    """Сохранить каталог и коллекцию в JSON-файлы."""
    save_json(SKINS_FILE, skins)
    save_json(COLLECTION_FILE, collection)


def run_menu(
    skins: list[dict[str, object]],
    collection: list[dict[str, object]],
) -> None:
    """Обрабатывать пункты пользовательского меню до команды выхода."""
    while True:
        print("\n=== Коллекция скинов Counter-Strike ===")
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
                owner = input("Имя владельца: ")
                skin_id = input_int("ID скина: ", minimum=1)
                balance = input_float("Баланс: ", minimum=0)
                item = add_to_collection(
                    collection,
                    skins,
                    owner,
                    skin_id,
                    balance,
                )
                save_project_data(skins, collection)
                print(f'Скин добавлен в коллекцию. ID записи: {item["id"]}')
            elif choice == "5":
                item_id = input_int("ID записи коллекции: ", minimum=1)
                remove_from_collection(collection, skins, item_id)
                save_project_data(skins, collection)
                print("Предмет удалён из коллекции")
            elif choice == "6":
                show_collection(collection)
            elif choice == "0":
                break
            else:
                print("Неизвестная команда")
        except (LookupError, ValueError, StorageError) as error:
            print(f"Ошибка: {error}")


def main() -> None:
    """Загрузить данные и запустить консольное меню."""
    try:
        skins = load_json(SKINS_FILE)
        collection = load_json(COLLECTION_FILE)
        run_menu(skins, collection)
    except StorageError as error:
        print(f"Ошибка хранения данных: {error}")


if __name__ == "__main__":
    main()
