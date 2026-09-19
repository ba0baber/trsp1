"""Операции с коллекцией объектов каталога скинов."""

from collections.abc import Iterator

from models import Skin, get_skin_condition


def add_skin(
    skins: list[Skin], name: str, weapon: str, price: float,
    wear: float, rarity: str, is_available: bool = True,
) -> Skin:
    """Добавить новый объект Skin в каталог."""
    skin_id = max((skin.id for skin in skins), default=0) + 1
    skin = Skin(
        skin_id, name.strip(), weapon.strip(), round(price, 2), wear,
        rarity.strip(), is_available,
    )
    skins.append(skin)
    return skin


def find_skin_by_id(skins: list[Skin], skin_id: int) -> Skin | None:
    """Найти скин по идентификатору."""
    return next((skin for skin in skins if skin.id == skin_id), None)


def find_skins(skins: list[Skin], query: str) -> list[Skin]:
    """Найти скины по фрагменту названия или оружия."""
    normalized = query.strip().lower()
    return [
        skin for skin in skins
        if normalized in skin.name.lower() or normalized in skin.weapon.lower()
    ]


def filter_skins_by_price(skins: list[Skin], max_price: float) -> list[Skin]:
    """Вернуть доступные скины не дороже указанной суммы."""
    return [
        skin for skin in skins
        if skin.is_available and skin.price <= max_price
    ]


def sort_skins_by_price(
    skins: list[Skin], descending: bool = False,
) -> list[Skin]:
    """Вернуть новый список скинов, отсортированный по цене."""
    return sorted(skins, key=lambda skin: skin.price, reverse=descending)


def iter_skins_by_rarity(
    skins: list[Skin], rarity: str,
) -> Iterator[Skin]:
    """Последовательно выдавать скины указанной редкости."""
    normalized = rarity.strip().lower()
    for skin in skins:
        if skin.rarity.lower() == normalized:
            yield skin


__all__ = ["Skin", "get_skin_condition"]
