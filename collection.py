"""Функции для управления пользовательской коллекцией скинов."""

from skins import Skin, find_skin_by_id


CollectionItem = dict[str, object]


def calculate_balance_after_purchase(balance: float, price: float) -> float:
    """Рассчитать остаток средств после покупки скина."""
    return round(balance - price, 2)


def get_purchase_status(
    is_available: bool,
    balance_after_purchase: float,
) -> str:
    """Вернуть результат проверки возможности покупки."""
    if not is_available:
        return "Скин сейчас недоступен"
    if balance_after_purchase < 0:
        return "Недостаточно средств для покупки"
    return "Скин можно добавить в коллекцию"


def add_to_collection(
    collection: list[CollectionItem],
    skins: list[Skin],
    owner: str,
    skin_id: int,
    balance: float,
) -> CollectionItem:
    """Купить доступный скин и добавить его в коллекцию пользователя."""
    skin = find_skin_by_id(skins, skin_id)
    if skin is None:
        raise LookupError("Скин с указанным идентификатором не найден")
    if not owner.strip():
        raise ValueError("Имя владельца не может быть пустым")

    remaining_balance = calculate_balance_after_purchase(
        balance,
        float(skin["price"]),
    )
    status = get_purchase_status(
        bool(skin["is_available"]),
        remaining_balance,
    )
    if status != "Скин можно добавить в коллекцию":
        raise ValueError(status)

    item_id = max((int(item["id"]) for item in collection), default=0) + 1
    item: CollectionItem = {
        "id": item_id,
        "owner": owner.strip(),
        "skin_id": skin_id,
        "purchase_price": float(skin["price"]),
    }
    collection.append(item)
    skin["is_available"] = False
    return item


def remove_from_collection(
    collection: list[CollectionItem],
    skins: list[Skin],
    item_id: int,
) -> CollectionItem:
    """Удалить предмет из коллекции и снова сделать скин доступным."""
    for index, item in enumerate(collection):
        if item["id"] == item_id:
            removed_item = collection.pop(index)
            skin = find_skin_by_id(skins, int(removed_item["skin_id"]))
            if skin is not None:
                skin["is_available"] = True
            return removed_item
    raise LookupError(
        "Предмет коллекции с указанным идентификатором не найден"
    )


def calculate_collection_value(
    collection: list[CollectionItem],
) -> float:
    """Рассчитать общую стоимость предметов коллекции."""
    return round(
        sum(float(item["purchase_price"]) for item in collection),
        2,
    )


def find_owner_items(
    collection: list[CollectionItem],
    owner: str,
) -> list[CollectionItem]:
    """Вернуть все предметы указанного владельца."""
    normalized_owner = owner.strip().lower()
    return [
        item
        for item in collection
        if str(item["owner"]).lower() == normalized_owner
    ]
