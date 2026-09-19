"""Класс пользовательской коллекции и взаимодействие объектов."""

from models import CollectionItem, Skin, User
from skins import find_skin_by_id


class Collection:
    """Коллекция, управляющая покупкой и удалением скинов."""

    def __init__(self, items: list[CollectionItem] | None = None) -> None:
        self.items = items if items is not None else []

    def purchase(
        self, skins: list[Skin], user: User, skin_id: int,
    ) -> CollectionItem:
        """Купить доступный скин и добавить запись в коллекцию."""
        skin = find_skin_by_id(skins, skin_id)
        if skin is None:
            raise LookupError("Скин с указанным идентификатором не найден")
        if not skin.is_available:
            raise ValueError("Скин сейчас недоступен")
        user.pay(skin.price)
        skin.mark_sold()
        item_id = max((item.id for item in self.items), default=0) + 1
        item = CollectionItem(item_id, user.name, skin.id, skin.price)
        self.items.append(item)
        return item

    def remove(self, skins: list[Skin], item_id: int) -> CollectionItem:
        """Удалить запись и вернуть соответствующий скин в каталог."""
        for index, item in enumerate(self.items):
            if item.id == item_id:
                removed = self.items.pop(index)
                skin = find_skin_by_id(skins, removed.skin_id)
                if skin is not None:
                    skin.mark_available()
                return removed
        raise LookupError(
            "Предмет коллекции с указанным идентификатором не найден"
        )

    def total_value(self) -> float:
        """Рассчитать общую стоимость коллекции."""
        return round(sum(item.purchase_price for item in self.items), 2)

    def find_by_owner(self, owner: str) -> list[CollectionItem]:
        """Вернуть все записи указанного владельца."""
        normalized = owner.strip().lower()
        return [
            item for item in self.items
            if item.owner.lower() == normalized
        ]

    def __str__(self) -> str:
        if not self.items:
            return "Коллекция пока пуста"
        rows = [str(item) for item in self.items]
        rows.append(f"Стоимость коллекции: {self.total_value():.2f} руб.")
        return "\n".join(rows)
