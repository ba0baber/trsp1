"""Функции для работы с каталогом скинов."""

from collections.abc import Iterator


Skin = dict[str, object]


def get_skin_condition(wear: float) -> str:
    """Определить состояние скина по значению износа."""
    if not 0 <= wear <= 1:
        raise ValueError("Износ должен находиться в диапазоне от 0 до 1")
    if wear < 0.07:
        return "Прямо с завода"
    if wear < 0.15:
        return "Немного поношенное"
    if wear < 0.38:
        return "После полевых испытаний"
    if wear < 0.45:
        return "Поношенное"
    return "Закалённое в боях"


def add_skin(
    skins: list[Skin],
    name: str,
    weapon: str,
    price: float,
    wear: float,
    rarity: str,
    is_available: bool = True,
) -> Skin:
    """Добавить новый скин в каталог и вернуть созданную запись."""
    if not name.strip() or not weapon.strip() or not rarity.strip():
        raise ValueError("Название, оружие и редкость не могут быть пустыми")
    if price < 0:
        raise ValueError("Цена не может быть отрицательной")

    condition = get_skin_condition(wear)
    skin_id = max((int(skin["id"]) for skin in skins), default=0) + 1
    skin: Skin = {
        "id": skin_id,
        "name": name.strip(),
        "weapon": weapon.strip(),
        "price": round(price, 2),
        "wear": wear,
        "condition": condition,
        "rarity": rarity.strip(),
        "is_available": is_available,
    }
    skins.append(skin)
    return skin


def find_skin_by_id(skins: list[Skin], skin_id: int) -> Skin | None:
    """Найти скин по идентификатору."""
    for skin in skins:
        if skin["id"] == skin_id:
            return skin
    return None


def find_skins(skins: list[Skin], query: str) -> list[Skin]:
    """Найти скины по фрагменту названия или оружия."""
    normalized_query = query.strip().lower()
    return [
        skin
        for skin in skins
        if normalized_query in str(skin["name"]).lower()
        or normalized_query in str(skin["weapon"]).lower()
    ]


def filter_skins_by_price(
    skins: list[Skin],
    max_price: float,
) -> list[Skin]:
    """Вернуть доступные скины не дороже указанной суммы."""
    return [
        skin
        for skin in skins
        if bool(skin["is_available"]) and float(skin["price"]) <= max_price
    ]


def sort_skins_by_price(
    skins: list[Skin],
    descending: bool = False,
) -> list[Skin]:
    """Вернуть новый список скинов, отсортированный по цене."""
    return sorted(
        skins,
        key=lambda skin: float(skin["price"]),
        reverse=descending,
    )


def iter_skins_by_rarity(
    skins: list[Skin],
    rarity: str,
) -> Iterator[Skin]:
    """Последовательно выдавать скины указанной редкости."""
    normalized_rarity = rarity.strip().lower()
    for skin in skins:
        if str(skin["rarity"]).lower() == normalized_rarity:
            yield skin
